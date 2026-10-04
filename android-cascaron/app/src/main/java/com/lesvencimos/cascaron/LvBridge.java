package com.lesvencimos.cascaron;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.util.Base64;
import android.os.Looper;
import android.util.Log;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Puente JS → nativo. Expone window.LvBridge en la mesa y en módulos.
 */
public class LvBridge {
    private static final String TAG = "LvBridge";

    private final WeakReference<MainActivity> activityRef;
    private final ModuleStore store;
    private LvTts tts;
    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private final Handler main = new Handler(Looper.getMainLooper());

    public LvBridge(MainActivity activity, ModuleStore store) {
        this.activityRef = new WeakReference<>(activity);
        this.store = store;
    }

    public void setTts(LvTts tts) {
        this.tts = tts;
        if (tts != null) {
            tts.setOnEndUi(() -> emit("tts-end", "{}"));
        }
    }

    private MainActivity act() {
        return activityRef.get();
    }

    private void toast(String msg) {
        MainActivity a = act();
        if (a == null) return;
        main.post(() -> Toast.makeText(a, msg, Toast.LENGTH_SHORT).show());
    }

    private void evalJs(String script) {
        MainActivity a = act();
        if (a == null) return;
        main.post(() -> {
            WebView wv = a.getWebView();
            if (wv != null) wv.evaluateJavascript(script, null);
        });
    }

    private void emit(String event, String jsonPayload) {
        String safe = jsonPayload == null ? "null" : jsonPayload;
        evalJs("(function(){try{window.dispatchEvent(new CustomEvent('lv:" + event
                + "',{detail:" + safe + "}));}catch(e){console.error(e);}})()");
    }

    /** Wizard: modo completo (todos los iconos/packs). */
    @JavascriptInterface
    public String saveSetupCompleto() {
        try {
            MainActivity a = act();
            if (a == null) return jsonErr("no activity");
            a.getPrefs().saveWizardCompleto();
            emit("setup", a.getPrefs().toJson().toString());
            main.post(a::onWizardFinished);
            return "{\"ok\":true,\"mode\":\"completo\"}";
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    /**
     * Wizard: selección custom.
     * visibleCsv = "pack-1eso,pack-casa,…" (ids de catalogo-embed).
     */
    @JavascriptInterface
    public String saveSetupCustom(String visibleCsv) {
        try {
            MainActivity a = act();
            if (a == null) return jsonErr("no activity");
            java.util.ArrayList<String> ids = new java.util.ArrayList<>();
            if (visibleCsv != null) {
                for (String part : visibleCsv.split(",")) {
                    String id = part.trim();
                    if (!id.isEmpty()) ids.add(id);
                }
            }
            a.getPrefs().saveWizardCustom(ids);
            emit("setup", a.getPrefs().toJson().toString());
            main.post(a::onWizardFinished);
            return "{\"ok\":true,\"mode\":\"custom\"}";
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    @JavascriptInterface
    public String getAppPrefs() {
        try {
            MainActivity a = act();
            if (a == null) return "{}";
            return a.getPrefs().toJson().toString();
        } catch (Exception e) {
            return "{}";
        }
    }

    /** True only for the full offline APK; flaco installs packs on demand. */
    @JavascriptInterface
    public boolean isFatOffline() {
        return !BuildConfig.FLACO_MODE;
    }

    @JavascriptInterface
    public void openEstanteria() {
        MainActivity a = act();
        if (a == null) return;
        main.post(a::openEstanteria);
    }

    @JavascriptInterface
    public String listModules() {
        try {
            return store.listModules().toString();
        } catch (Exception e) {
            Log.e(TAG, "listModules", e);
            return "[]";
        }
    }

    @JavascriptInterface
    public String fetchCatalog() {
        try {
            // Fat Completo: sin catálogo de descarga (todo embebido).
            if (!BuildConfig.FLACO_MODE) {
                return store.loadEmbeddedCatalog().toString();
            }
            // Flaco: preferente lesvencimos.com; fallback embebido. Solo consulta.
            try {
                JSONObject remote = store.fetchCatalogRemote();
                return remote.toString();
            } catch (Exception e) {
                Log.w(TAG, "catálogo remoto, uso embebido", e);
                return store.loadEmbeddedCatalog().toString();
            }
        } catch (Exception e) {
            Log.e(TAG, "fetchCatalog", e);
            return "{\"modulos\":[],\"error\":\"" + e.getMessage() + "\"}";
        }
    }

    @JavascriptInterface
    public String fetchCatalogEmbedded() {
        try {
            return store.loadEmbeddedCatalog().toString();
        } catch (Exception e) {
            return "{\"modulos\":[]}";
        }
    }


    /**
     * Consulta catálogo en segundo plano (remoto https://lesvencimos.com/catalogo.json
     * → fallback embebido). Emite lv:catalog. Solo consulta: NUNCA instala ni actualiza.
     * El usuario debe pulsar Instalar en la mesa.
     */
    @JavascriptInterface
    public void fetchCatalogAsync() {
        io.execute(() -> {
            try {
                JSONObject cat;
                String fuente;
                if (!BuildConfig.FLACO_MODE) {
                    cat = store.loadEmbeddedCatalog();
                    fuente = "embebido (fat · sin descarga)";
                } else {
                    try {
                        cat = store.fetchCatalogRemote();
                        fuente = "https://lesvencimos.com/catalogo.json";
                    } catch (Exception e) {
                        Log.w(TAG, "catálogo remoto, uso embebido", e);
                        cat = store.loadEmbeddedCatalog();
                        fuente = "embebido (assets)";
                    }
                }
                JSONObject payload = new JSONObject();
                payload.put("fuente", fuente);
                payload.put("remoto", fuente.startsWith("https://"));
                payload.put("catalogo", cat);
                emit("catalog", payload.toString());
            } catch (Exception e) {
                Log.e(TAG, "fetchCatalogAsync", e);
                emit("error", jsonErr(e.getMessage()));
            }
        });
    }

    /** Instala ZIP desde content URI (SAF «Añadir»). Solo flaco. */
    @JavascriptInterface
    public void installZipFromUri(String uriString) {
        if (!BuildConfig.FLACO_MODE) {
            toast("Todo el contenido ya está en la app");
            return;
        }
        MainActivity a = act();
        if (a == null || uriString == null) return;
        io.execute(() -> {
            try {
                android.net.Uri uri = android.net.Uri.parse(uriString);
                byte[] data;
                try (InputStream in = a.getContentResolver().openInputStream(uri)) {
                    if (in == null) throw new IllegalArgumentException("no se pudo abrir");
                    data = readAll(in);
                }
                String name = uri.getLastPathSegment();
                if (name == null) name = "pack.zip";
                String id = ModuleStore.slug(name);
                JSONObject meta = store.installZipBytes(data, id, null);
                emit("installed", meta.toString());
                toast("Instalado: " + meta.optString("nombre", id));
            } catch (Exception e) {
                Log.e(TAG, "installZipFromUri", e);
                emit("error", jsonErr(e.getMessage()));
                toast("Error al instalar: " + e.getMessage());
            }
        });
    }

    /** Instala ZIP en base64 (packs pequeños). Solo flaco. */
    @JavascriptInterface
    public void installZipFromBase64(String base64, String id, String nombre) {
        if (!BuildConfig.FLACO_MODE) {
            toast("Todo el contenido ya está en la app");
            return;
        }
        io.execute(() -> {
            try {
                byte[] data = Base64.decode(base64, Base64.DEFAULT);
                JSONObject meta = store.installZipBytes(data, id, nombre);
                emit("installed", meta.toString());
                toast("Instalado: " + meta.optString("nombre", id));
            } catch (Exception e) {
                Log.e(TAG, "installZipFromBase64", e);
                emit("error", jsonErr(e.getMessage()));
                toast("Error al instalar");
            }
        });
    }

    /**
     * Quita módulo. wipeData=true borra data/&lt;id&gt;.json.
     * La mesa debe preguntar antes de wipeData.
     */
    @JavascriptInterface
    public String uninstall(String id, boolean wipeData) {
        try {
            boolean ok = store.uninstall(id, wipeData);
            JSONObject o = new JSONObject();
            o.put("ok", ok);
            o.put("id", id);
            o.put("wipeData", wipeData);
            emit("uninstalled", o.toString());
            return o.toString();
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    @JavascriptInterface
    public boolean hasData(String id) {
        return store.hasData(id);
    }

    @JavascriptInterface
    public String readData(String id) {
        try {
            String raw = store.readData(id);
            JSONObject o = new JSONObject();
            o.put("id", id);
            if (raw == null) o.put("datos", JSONObject.NULL);
            else {
                String t = raw.trim();
                if (t.startsWith("[")) o.put("datos", new org.json.JSONArray(t));
                else o.put("datos", new JSONObject(t));
            }
            return o.toString();
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    @JavascriptInterface
    public String writeData(String id, String json) {
        try {
            store.writeData(id, json);
            JSONObject o = new JSONObject();
            o.put("ok", true);
            o.put("id", id);
            return o.toString();
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    /** Exporta backup → CREATE_DOCUMENT lesvencimos-backup.json */
    @JavascriptInterface
    public void exportBackup() {
        io.execute(() -> {
            try {
                JSONObject bak = store.exportBackup();
                byte[] bytes = bak.toString(2).getBytes(StandardCharsets.UTF_8);
                MainActivity a = act();
                if (a == null) return;
                main.post(() -> a.saveDocument("lesvencimos-backup.json", bytes, "application/json"));
            } catch (Exception e) {
                Log.e(TAG, "exportBackup", e);
                toast("No se pudo exportar");
                emit("error", jsonErr(e.getMessage()));
            }
        });
    }

    @JavascriptInterface
    public void downloadAndInstall(String url, String id) {
        if (!BuildConfig.FLACO_MODE) {
            toast("Todo el contenido ya está en la app");
            emit("error", jsonErr("sin descarga en Completo"));
            return;
        }
        io.execute(() -> {
            try {
                emit("progress", "{\"id\":\"" + id + "\",\"estado\":\"descargando\"}");
                JSONObject meta = store.downloadAndInstall(url, id);
                emit("installed", meta.toString());
                toast("Instalado: " + meta.optString("nombre", id));
            } catch (Exception e) {
                Log.e(TAG, "downloadAndInstall", e);
                emit("error", jsonErr(e.getMessage()));
                toast("Descarga fallida: " + e.getMessage());
            }
        });
    }

    @JavascriptInterface
    public void openModule(String id) {
        MainActivity a = act();
        if (a == null) return;
        main.post(() -> {
            try {
                if (id == null || id.trim().isEmpty()) {
                    toast("Instala el pack");
                    return;
                }
                if (!store.isInstalled(id)) {
                    String miss = BuildConfig.FLACO_MODE
                            ? "Instala el pack"
                            : "Módulo no disponible en Completo";
                    toast(miss);
                    emit("error", jsonErr(miss));
                    return;
                }
                java.io.File entry = store.resolveEntryFile(id);
                if (entry == null || !entry.isFile()) {
                    toast("Instala el pack");
                    emit("error", jsonErr("Instala el pack"));
                    return;
                }
                String url = store.moduleEntryUrl(id);
                Log.i(TAG, "openModule " + id + " → " + url);
                a.openUrl(url);
            } catch (IllegalArgumentException e) {
                String msg = e.getMessage() != null ? e.getMessage() : "";
                if (msg.contains("no instalado") || msg.contains("id")) {
                    toast("Instala el pack");
                    emit("error", jsonErr("Instala el pack"));
                } else {
                    toast("Instala el pack");
                    emit("error", jsonErr("Instala el pack"));
                }
            } catch (Exception e) {
                Log.e(TAG, "openModule", e);
                toast("Instala el pack");
                emit("error", jsonErr("Instala el pack"));
            }
        });
    }

    /** true si el módulo está en modules/<id>/. */
    @JavascriptInterface
    public boolean isInstalled(String id) {
        return store.isInstalled(id);
    }

    @JavascriptInterface
    public void openMesa() {
        MainActivity a = act();
        if (a == null) return;
        main.post(a::openEstanteria);
    }

    /** Fat: vuelve a la estantería (parade k3). */
    @JavascriptInterface
    public void openMesaView(String view) {
        MainActivity a = act();
        if (a == null) return;
        main.post(a::openEstanteria);
    }

    /** La mesa pide elegir un ZIP (SAF). */
    @JavascriptInterface
    public void pickZipToInstall() {
        MainActivity a = act();
        if (a == null) return;
        if (BuildConfig.FLACO_MODE) {
            main.post(a::pickZipToInstall);
        } else {
            toast("Todo el contenido ya está en la app");
        }
    }


    /**
     * API explícita para módulos que buscan LvBridge.speak / Android.speak
     * (además del polyfill speechSynthesis).
     */
    @JavascriptInterface
    public void speak(String text) {
        ttsSpeak(text, "es-ES", 1.0f, 1.0f);
    }

    @JavascriptInterface
    public void speakLang(String text, String lang) {
        ttsSpeak(text, lang != null && !lang.isEmpty() ? lang : "es-ES", 1.0f, 1.0f);
    }

    /** TTS nativo — polyfill speechSynthesis en packs (Maestro, cocina, gimnasio, marionetas…). */
    @JavascriptInterface
    public void ttsSpeak(String text, String lang, float rate, float pitch) {
        if (tts == null) return;
        tts.speak(text, lang, rate, pitch);
    }

    @JavascriptInterface
    public void ttsCancel() {
        if (tts != null) tts.cancel();
    }

    /** Alias documentado en LEEME-maestro-voz-apk (stop). */
    @JavascriptInterface
    public void ttsStop() {
        ttsCancel();
    }

    @JavascriptInterface
    public boolean ttsReady() {
        return tts != null && tts.isReady();
    }

    @JavascriptInterface
    public boolean ttsIsSpeaking() {
        return tts != null && tts.isSpeaking();
    }

    @JavascriptInterface
    public String ttsStatus() {
        return tts == null ? "none" : tts.status();
    }


    // ─── Audio / mic / SAF / MediaStore (2.0.10) ───────────────────────────

    /** true si RECORD_AUDIO ya concedido. */
    @JavascriptInterface
    public boolean hasMicPermission() {
        MainActivity a = act();
        if (a == null) return false;
        return a.checkSelfPermission(Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_GRANTED;
    }

    /** Pide RECORD_AUDIO en runtime; emite lv:mic-permission {granted}. */
    @JavascriptInterface
    public void requestMicPermission() {
        MainActivity a = act();
        if (a == null) return;
        main.post(a::requestMicPermissionFromJs);
    }


    /** HTML (grabadora): micro del teléfono, no el Bluetooth ocupado. No toca TTS. */
    @JavascriptInterface
    public void preferBuiltInMic() {
        MainActivity a = act();
        if (a == null) return;
        a.preferBuiltInMic();
    }

    /**
     * SAF: elegir audio(s) del usuario.
     * Emite lv:audio-picked {ok, name, mime, uri, url, bytes?} por cada archivo
     * (url = https://appassets…/user-audio/… reproducible en WebView).
     */
    @JavascriptInterface
    public void pickAudioFile() {
        MainActivity a = act();
        if (a == null) return;
        main.post(a::pickAudioFile);
    }

    /** Alias documentado. */
    @JavascriptInterface
    public void openDocument(String mimeCsv) {
        MainActivity a = act();
        if (a == null) return;
        final String mime = (mimeCsv == null || mimeCsv.trim().isEmpty())
                ? "audio/*" : mimeCsv.trim();
        main.post(() -> a.openDocument(mime));
    }

    /**
     * Guarda audio (base64) en Music/LesVencimos/ (MediaStore) o Documents/LesVencimos/.
     * Emite lv:audio-saved. Devuelve JSON síncrono con ok/uri/url/name.
     */
    @JavascriptInterface
    public String saveAudioBase64(String base64, String fileName, String mime) {
        MainActivity a = act();
        if (a == null) return jsonErr("no activity");
        try {
            if (base64 == null || base64.isEmpty()) return jsonErr("vacío");
            // data URL opcional
            String b64 = base64;
            int comma = b64.indexOf(',');
            if (b64.startsWith("data:") && comma > 0) {
                b64 = b64.substring(comma + 1);
            }
            byte[] data = Base64.decode(b64, Base64.DEFAULT);
            org.json.JSONObject meta = LvMedia.saveAudio(a, data, fileName, mime);
            emit("audio-saved", meta.toString());
            main.post(() -> Toast.makeText(a,
                    "Guardado en " + meta.optString("relativePath", "LesVencimos"),
                    Toast.LENGTH_SHORT).show());
            return meta.toString();
        } catch (Exception e) {
            Log.e(TAG, "saveAudioBase64", e);
            String err = jsonErr(e.getMessage());
            emit("error", err);
            return err;
        }
    }

    /** Lista hasta 50 grabaciones en Music/…/LesVencimos. */
    @JavascriptInterface
    public String listSavedRecordings() {
        MainActivity a = act();
        if (a == null) return "[]";
        try {
            return LvMedia.listRecordings(a).toString();
        } catch (Exception e) {
            return "[]";
        }
    }

    /** Carpeta lógica de usuario (informativo para HTML). */
    @JavascriptInterface
    public String getUserMediaFolder() {
        return LvMedia.FOLDER;
    }

    /** startRecording/stopRecording: no-op nativo — HTML usa MediaRecorder; mic vía getUserMedia. */
    @JavascriptInterface
    public String startRecording() {
        // Asegura permiso; el HTML sigue con MediaRecorder
        requestMicPermission();
        try {
            JSONObject o = new JSONObject();
            o.put("ok", true);
            o.put("mode", "webview-getUserMedia");
            o.put("hint", "Usar navigator.mediaDevices.getUserMedia + MediaRecorder");
            return o.toString();
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }

    @JavascriptInterface
    public String stopRecording() {
        try {
            JSONObject o = new JSONObject();
            o.put("ok", true);
            o.put("mode", "webview-getUserMedia");
            return o.toString();
        } catch (Exception e) {
            return jsonErr(e.getMessage());
        }
    }


    private static String jsonErr(String msg) {
        try {
            JSONObject o = new JSONObject();
            o.put("error", msg == null ? "error" : msg);
            return o.toString();
        } catch (Exception e) {
            return "{\"error\":\"error\"}";
        }
    }

    private static byte[] readAll(InputStream in) throws Exception {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int n;
        int total = 0;
        while ((n = in.read(buf)) > 0) {
            total += n;
            if (total > 30 * 1024 * 1024) throw new IllegalArgumentException("tamaño");
            bos.write(buf, 0, n);
        }
        return bos.toByteArray();
    }
}
