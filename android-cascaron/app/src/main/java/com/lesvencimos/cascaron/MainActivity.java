package com.lesvencimos.cascaron;

import android.annotation.SuppressLint;
import android.Manifest;
import android.content.pm.PackageManager;
import android.webkit.PermissionRequest;
import android.webkit.ValueCallback;
import android.webkit.DownloadListener;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.media.AudioDeviceInfo;
import android.media.AudioManager;
import android.os.Build;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewCompat;
import androidx.webkit.WebViewFeature;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Les vencimos Android shell (dual fat/flaco).
 * Fat Completo 2.0.12: mic RECORD_AUDIO + SAF audio picker + MediaStore LesVencimos;
 * embed ZIP k9-todo-d (parade OFF) + educacion/ from filesDir + scroll touch + TTS shim.
 * Flaco 1.0.7: mesa.html + packs on demand (sin embed).
 * Entry: mesa.html flaco; estanteria.html fat.
 */
public class MainActivity extends AppCompatActivity {
    private static final String TAG = "LesVencimosFat";
    private static final String HOST = "appassets.androidplatform.net";
    private static final String WIZARD =
            "https://appassets.androidplatform.net/assets/wizard.html";
    private static final String ENTRY_FAT =
            "https://appassets.androidplatform.net/completo/estanteria.html";
    private static final String ENTRY_FLACO =
            "https://appassets.androidplatform.net/assets/mesa.html";

    private WebView webView;
    private View extractOverlay;
    private ProgressBar extractBar;
    private TextView extractLabel;
    private ModuleStore store;
    private LvBridge bridge;
    private LvTts tts;
    private AppPrefs prefs;
    private WebViewAssetLoader assetLoader;
    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private final Handler main = new Handler(Looper.getMainLooper());

    private byte[] pendingDownloadBytes;
    private String pendingDownloadName;

    /** WebView getUserMedia → runtime RECORD_AUDIO */
    private PermissionRequest pendingWebPermissionRequest;
    /** &lt;input type=file&gt; chooser */
    private ValueCallback<Uri[]> filePathCallback;

    private final androidx.activity.result.ActivityResultLauncher<String> micPermissionLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.RequestPermission(),
                    granted -> {
                        if (pendingWebPermissionRequest != null) {
                            try {
                                if (granted) {
                                    grantAudioCapture(pendingWebPermissionRequest);
                                } else {
                                    pendingWebPermissionRequest.deny();
                                }
                            } catch (Exception e) {
                                Log.e(TAG, "grant web permission", e);
                                try { pendingWebPermissionRequest.deny(); } catch (Exception ignored) {}
                            }
                            pendingWebPermissionRequest = null;
                        }
                        emitMicPermission(granted);
                    });

    private final androidx.activity.result.ActivityResultLauncher<String[]> micPermissionsLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions(),
                    result -> {
                        boolean granted = Boolean.TRUE.equals(
                                result.get(Manifest.permission.RECORD_AUDIO));
                        if (pendingWebPermissionRequest != null) {
                            try {
                                if (granted) {
                                    grantAudioCapture(pendingWebPermissionRequest);
                                } else {
                                    pendingWebPermissionRequest.deny();
                                }
                            } catch (Exception e) {
                                Log.e(TAG, "grant web permission multi", e);
                                try { pendingWebPermissionRequest.deny(); } catch (Exception ignored) {}
                            }
                            pendingWebPermissionRequest = null;
                        }
                        emitMicPermission(granted);
                    });

    private final androidx.activity.result.ActivityResultLauncher<Intent> pickAudioLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                            handlePickedAudio(result.getData());
                        } else if (bridge != null) {
                            bridgeEmit("audio-picked",
                                    "{\"ok\":false,\"cancelled\":true}");
                        }
                    });

    private final androidx.activity.result.ActivityResultLauncher<Intent> fileChooserLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        Uri[] uris = null;
                        if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                            Intent data = result.getData();
                            if (data.getClipData() != null) {
                                int n = data.getClipData().getItemCount();
                                uris = new Uri[n];
                                for (int i = 0; i < n; i++) {
                                    uris[i] = data.getClipData().getItemAt(i).getUri();
                                }
                            } else if (data.getData() != null) {
                                uris = new Uri[]{data.getData()};
                            }
                        }
                        if (filePathCallback != null) {
                            filePathCallback.onReceiveValue(uris);
                            filePathCallback = null;
                        }
                        // También notificar bridge (reproductor puede escuchar lv:audio-picked)
                        if (uris != null) {
                            for (Uri u : uris) {
                                deliverPickedUri(u);
                            }
                        }
                    });

    private final androidx.activity.result.ActivityResultLauncher<Intent> pickZipLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (result.getResultCode() == RESULT_OK && result.getData() != null
                                && result.getData().getData() != null && bridge != null) {
                            bridge.installZipFromUri(result.getData().getData().toString());
                        }
                    });

    private final androidx.activity.result.ActivityResultLauncher<Intent> createDocumentLauncher =
            registerForActivityResult(
                    new androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult(),
                    result -> {
                        if (pendingDownloadBytes == null) return;
                        if (result.getResultCode() == RESULT_OK && result.getData() != null
                                && result.getData().getData() != null) {
                            try (OutputStream os = getContentResolver()
                                    .openOutputStream(result.getData().getData())) {
                                if (os != null) {
                                    os.write(pendingDownloadBytes);
                                    os.flush();
                                    Toast.makeText(this, "Archivo guardado (solo este dispositivo)",
                                            Toast.LENGTH_SHORT).show();
                                }
                            } catch (Exception e) {
                                Log.e(TAG, "save failed", e);
                                Toast.makeText(this, "No se pudo guardar", Toast.LENGTH_SHORT).show();
                            }
                        }
                        pendingDownloadBytes = null;
                        pendingDownloadName = null;
                    });

    public WebView getWebView() {
        return webView;
    }

    public AppPrefs getPrefs() {
        return prefs;
    }

    public void openUrl(String url) {
        if (webView != null) webView.loadUrl(url);
    }

    public void openEstanteria() {
        openUrl(BuildConfig.FLACO_MODE ? ENTRY_FLACO : ENTRY_FAT);
    }

    public void pickZipToInstall() {
        if (!BuildConfig.FLACO_MODE) {
            Toast.makeText(this, "Todo el contenido ya está en la app", Toast.LENGTH_SHORT).show();
            return;
        }
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("application/zip");
        intent.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"application/zip", "application/octet-stream"});
        try {
            pickZipLauncher.launch(intent);
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "No hay gestor de archivos", Toast.LENGTH_SHORT).show();
        }
    }

    public void openWizard() {
        openUrl(WIZARD);
    }

    public void saveDocument(String name, byte[] bytes, String mime) {
        pendingDownloadBytes = bytes;
        pendingDownloadName = name;
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(mime != null ? mime : "application/json");
        intent.putExtra(Intent.EXTRA_TITLE, name != null ? name : "lesvencimos-backup.json");
        try {
            createDocumentLauncher.launch(intent);
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "No hay gestor de archivos", Toast.LENGTH_SHORT).show();
            pendingDownloadBytes = null;
        }
    }


    private void emitMicPermission(boolean granted) {
        if (bridge == null) return;
        try {
            org.json.JSONObject o = new org.json.JSONObject();
            o.put("granted", granted);
            o.put("permission", "RECORD_AUDIO");
            bridgeEmit("mic-permission", o.toString());
        } catch (Exception e) {
            Log.w(TAG, "emitMicPermission", e);
        }
    }

    private void bridgeEmit(String event, String json) {
        if (webView == null) return;
        String safe = json == null ? "null" : json;
        webView.evaluateJavascript(
                "(function(){try{window.dispatchEvent(new CustomEvent('lv:" + event
                        + "',{detail:" + safe + "}));}catch(e){}})()",
                null);
    }

    public void requestMicPermissionFromJs() {
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_GRANTED) {
            emitMicPermission(true);
            return;
        }
        micPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO);
    }


    /** Solo RESOURCE_AUDIO_CAPTURE. Antes, ruta al micro del teléfono (no SCO Bluetooth). No toca TTS. */
    private void grantAudioCapture(PermissionRequest request) {
        if (request == null) return;
        preferBuiltInMic();
        request.grant(new String[]{PermissionRequest.RESOURCE_AUDIO_CAPTURE});
    }

    /**
     * getUserMedia del WebView suele enganchar el Bluetooth SCO, que Android
     * reporta ocupado. Fijamos el micro integrado como dispositivo de comunicación.
     */
    public void preferBuiltInMic() {
        try {
            AudioManager am = (AudioManager) getSystemService(AUDIO_SERVICE);
            if (am == null) return;
            try { am.setBluetoothScoOn(false); } catch (Exception ignored) {}
            try { am.stopBluetoothSco(); } catch (Exception ignored) {}
            if (Build.VERSION.SDK_INT >= 31) {
                AudioDeviceInfo builtin = null;
                java.util.List<AudioDeviceInfo> devs = am.getAvailableCommunicationDevices();
                if (devs != null) {
                    for (AudioDeviceInfo d : devs) {
                        if (d != null && d.getType() == AudioDeviceInfo.TYPE_BUILTIN_MIC) {
                            builtin = d;
                            break;
                        }
                    }
                }
                if (builtin != null) am.setCommunicationDevice(builtin);
                else am.clearCommunicationDevice();
            }
        } catch (Exception e) {
            Log.w(TAG, "preferBuiltInMic", e);
        }
    }

    private void ensureMicThenGrant(PermissionRequest request) {
        pendingWebPermissionRequest = request;
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO)
                == PackageManager.PERMISSION_GRANTED) {
            try {
                grantAudioCapture(request);
            } catch (Exception e) {
                Log.e(TAG, "grant", e);
                try { request.deny(); } catch (Exception ignored) {}
            }
            pendingWebPermissionRequest = null;
            emitMicPermission(true);
            return;
        }
        micPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO);
    }

    /** SAF audio picker (LvBridge.pickAudioFile). */
    public void pickAudioFile() {
        openDocument("audio/*");
    }

    public void openDocument(String mime) {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        String m = (mime == null || mime.isEmpty()) ? "audio/*" : mime;
        if (m.contains(",")) {
            String[] parts = m.split(",");
            intent.setType("*/*");
            intent.putExtra(Intent.EXTRA_MIME_TYPES, parts);
        } else {
            intent.setType(m);
        }
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        intent.addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
        try {
            pickAudioLauncher.launch(intent);
        } catch (ActivityNotFoundException e) {
            // Fallback GET_CONTENT
            try {
                Intent alt = new Intent(Intent.ACTION_GET_CONTENT);
                alt.addCategory(Intent.CATEGORY_OPENABLE);
                alt.setType(m.contains(",") ? "*/*" : m);
                alt.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                pickAudioLauncher.launch(alt);
            } catch (ActivityNotFoundException e2) {
                Toast.makeText(this, "No hay gestor de archivos", Toast.LENGTH_SHORT).show();
                bridgeEmit("audio-picked", "{\"ok\":false,\"error\":\"no picker\"}");
            }
        }
    }

    private void handlePickedAudio(Intent data) {
        if (data.getClipData() != null) {
            int n = data.getClipData().getItemCount();
            for (int i = 0; i < n; i++) {
                deliverPickedUri(data.getClipData().getItemAt(i).getUri());
            }
        } else if (data.getData() != null) {
            deliverPickedUri(data.getData());
        }
    }

    private void deliverPickedUri(Uri uri) {
        if (uri == null) return;
        io.execute(() -> {
            try {
                try {
                    getContentResolver().takePersistableUriPermission(uri,
                            Intent.FLAG_GRANT_READ_URI_PERMISSION);
                } catch (Exception ignored) {}
                String name = uri.getLastPathSegment();
                if (name == null) name = "audio.m4a";
                int slash = name.lastIndexOf('/');
                if (slash >= 0) name = name.substring(slash + 1);
                java.io.File cached = LvMedia.copyUriToCache(this, uri, name);
                org.json.JSONObject o = new org.json.JSONObject();
                o.put("ok", true);
                o.put("uri", uri.toString());
                o.put("name", cached.getName());
                o.put("mime", LvMedia.mimeFromName(cached.getName()));
                o.put("bytes", cached.length());
                o.put("url", "https://appassets.androidplatform.net/user-audio/" + cached.getName());
                o.put("cachePath", cached.getAbsolutePath());
                String json = o.toString();
                main.post(() -> bridgeEmit("audio-picked", json));
            } catch (Exception e) {
                Log.e(TAG, "deliverPickedUri", e);
                main.post(() -> bridgeEmit("audio-picked",
                        "{\"ok\":false,\"error\":\"" + String.valueOf(e.getMessage()).replace("\"", "'") + "\"}"));
            }
        });
    }


    public void onWizardFinished() {
        main.post(this::openEstanteria);
    }

    static String mimeFromPath(String path) {
        if (path == null) return null;
        String p = path.toLowerCase(Locale.ROOT);
        int q = p.indexOf('?');
        if (q >= 0) p = p.substring(0, q);
        if (p.endsWith(".m4a") || p.endsWith(".mp4a")) return "audio/mp4";
        if (p.endsWith(".mp3")) return "audio/mpeg";
        if (p.endsWith(".ogg") || p.endsWith(".oga")) return "audio/ogg";
        if (p.endsWith(".wav")) return "audio/wav";
        if (p.endsWith(".aac")) return "audio/aac";
        if (p.endsWith(".weba")) return "audio/webm";
        if (p.endsWith(".mp4")) return "video/mp4";
        if (p.endsWith(".webm")) return "video/webm";
        if (p.endsWith(".m4v")) return "video/mp4";
        if (p.endsWith(".html") || p.endsWith(".htm")) return "text/html";
        if (p.endsWith(".js")) return "application/javascript";
        if (p.endsWith(".css")) return "text/css";
        if (p.endsWith(".json")) return "application/json";
        if (p.endsWith(".png")) return "image/png";
        if (p.endsWith(".jpg") || p.endsWith(".jpeg")) return "image/jpeg";
        if (p.endsWith(".svg")) return "image/svg+xml";
        if (p.endsWith(".webp")) return "image/webp";
        if (p.endsWith(".woff")) return "font/woff";
        if (p.endsWith(".woff2")) return "font/woff2";
        if (p.endsWith(".ttf")) return "font/ttf";
        return null;
    }

    private WebResourceResponse serveFile(File root, String relPath) {
        try {
            String rel = relPath;
            while (rel.startsWith("/")) rel = rel.substring(1);
            if (rel.isEmpty() || rel.contains("..")) return null;
            File target = new File(root, rel);
            String rootCanon = root.getCanonicalPath();
            String fileCanon = target.getCanonicalPath();
            if (!fileCanon.startsWith(rootCanon + File.separator) && !fileCanon.equals(rootCanon)) {
                return null;
            }
            if (!target.isFile()) return null;
            String mime = mimeFromPath(target.getName());
            if (mime == null) mime = "application/octet-stream";
            InputStream in = new FileInputStream(target);
            Map<String, String> headers = new HashMap<>();
            headers.put("Cache-Control", "no-store");
            headers.put("Content-Type", mime);
            return new WebResourceResponse(mime, "UTF-8", 200, "OK", headers, in);
        } catch (Exception e) {
            Log.e(TAG, "serveFile " + relPath, e);
            return null;
        }
    }


    /** Respuesta HTML clara cuando falta ruta local (evita error opaco en WebView). */
    private WebResourceResponse missingLocalHtml(String title, String detail) {
        String safeTitle = title == null ? "Contenido" : title.replace("<", "");
        String safeDetail = detail == null ? "" : detail.replace("<", "");
        String html = "<!DOCTYPE html><html lang=es><meta charset=utf-8>"
                + "<meta name=viewport content=\"width=device-width,initial-scale=1\">"
                + "<body style=\"background:#0E0E0C;color:#E6E1D6;font:1rem system-ui;padding:1.5rem\">"
                + "<h1>" + safeTitle + "</h1><p>" + safeDetail + "</p>"
                + "<p>Vuelve a la estantería y abre el icono de Educación.</p></body></html>";
        InputStream in = new ByteArrayInputStream(html.getBytes(StandardCharsets.UTF_8));
        Map<String, String> headers = new HashMap<>();
        headers.put("Cache-Control", "no-store");
        headers.put("Content-Type", "text/html; charset=UTF-8");
        return new WebResourceResponse("text/html", "UTF-8", 404, "Not Found", headers, in);
    }

    private WebResourceResponse withFixedMime(Uri uri, WebResourceResponse resp) {
        if (resp == null || uri == null) return resp;
        String want = mimeFromPath(uri.getPath());
        if (want == null) return resp;
        String have = resp.getMimeType();
        if (have != null && !have.isEmpty()
                && !have.equals("application/octet-stream")
                && !have.equals("text/plain")) {
            if (want.startsWith("audio/") && have.startsWith("audio/")) return resp;
            if (want.startsWith("video/") && have.startsWith("video/")) return resp;
            if (!have.equals("application/octet-stream")) return resp;
        }
        Map<String, String> headers = resp.getResponseHeaders();
        if (headers == null) headers = new HashMap<>();
        else headers = new HashMap<>(headers);
        headers.put("Content-Type", want);
        int code = resp.getStatusCode() > 0 ? resp.getStatusCode() : 200;
        String reason = resp.getReasonPhrase() != null ? resp.getReasonPhrase() : "OK";
        return new WebResourceResponse(
                want,
                resp.getEncoding() != null ? resp.getEncoding() : "UTF-8",
                code, reason, headers, resp.getData());
    }

    /**
     * Corre ANTES que el JS de estantería/módulos (document-start).
     * Crítico: WebView reporta prefers-reduced-motion:reduce y speechSynthesis mudo.
     */
    private static String bootScript() {
        String fatEarly = BuildConfig.FLACO_MODE ? ""
                : ("try{window.__lvFatOffline=1;window.__lvNoDownload=1;"
                + "localStorage.setItem('lv-fat-offline','1');"
                + "localStorage.setItem('lv-no-download','1');}catch(eFat){}");
        return "(function(){"
                + "try{if(!window.__lvBoot){window.__lvBoot=1;"
                + fatEarly
                + "window.__lvNoParade=1;window.__lvForceParade=0;"
                + "try{window.startShelfDrift=function(){};window.__lvKickParade=function(){};window.__lvRestartParade=function(){};}catch(e){}"
                + "var __mm=window.matchMedia;window.matchMedia=function(q){q=String(q||'');"
                + "if(q.indexOf('prefers-reduced-motion')>=0){return{matches:false,media:q,"
                + "addListener:function(){},removeListener:function(){},addEventListener:function(){},"
                + "removeEventListener:function(){},onchange:null,dispatchEvent:function(){return false;}};"
                + "}return __mm.call(window,q);};"
                + "}}catch(e){}"
                + "function __lvInstallTts(){try{"
                + "if(!window.LvBridge||typeof LvBridge.ttsSpeak!=='function')return false;"
                + "if(window.__lvTtsShim)return true;window.__lvTtsShim=1;"
                + "function LvUtt(t){this.text=t||'';this.lang='es-ES';this.rate=1;this.pitch=1;"
                + "this.volume=1;this.onend=null;this.onerror=null;this.onstart=null;this.voice=null;}"
                + "var _utt=null,_poll=null;"
                + "function clearPoll(){if(_poll){clearInterval(_poll);_poll=null;}}"
                + "var synth={speaking:false,pending:false,paused:false,"
                + "getVoices:function(){return[{name:'LesVencimos-TTS',lang:'es-ES',localService:true,"
                + "default:true,voiceURI:'lesvencimos-native'}];},"
                + "cancel:function(){try{LvBridge.ttsCancel();}catch(e){}this.speaking=false;clearPoll();_utt=null;},"
                + "pause:function(){},resume:function(){},"
                + "speak:function(u){if(!u)return;var self=this;clearPoll();try{LvBridge.ttsCancel();}catch(e){}"
                + "var text=String(u.text||'');if(!text)return;"
                + "var lang=u.lang||'es-ES';var rate=u.rate!=null?Number(u.rate):1;"
                + "var pitch=u.pitch!=null?Number(u.pitch):1;"
                + "_utt=u;self.speaking=true;try{if(u.onstart)u.onstart();}catch(e){}"
                + "try{LvBridge.ttsSpeak(text,lang,rate,pitch);}catch(e){self.speaking=false;"
                + "try{if(u.onerror)u.onerror(e);}catch(x){}return;}"
                + "_poll=setInterval(function(){var sp=false;try{sp=!!LvBridge.ttsIsSpeaking();}catch(e){}"
                + "if(!sp){clearPoll();self.speaking=false;var done=_utt;_utt=null;"
                + "try{if(done&&done.onend)done.onend();}catch(e){}}},120);}};"
                + "try{Object.defineProperty(window,'speechSynthesis',{configurable:true,enumerable:true,"
                + "get:function(){return synth;},set:function(){}});}catch(e){window.speechSynthesis=synth;}"
                + "try{window.SpeechSynthesisUtterance=LvUtt;}catch(e){}"
                + "try{window.Android=window.Android||{};"
                + "window.Android.speak=function(tx){try{if(typeof LvBridge.speak==='function')LvBridge.speak(String(tx||''));"
                + "else LvBridge.ttsSpeak(String(tx||''),'es-ES',1,1);}catch(e){};};"
                + "window.lvSpeak=window.Android.speak;"
                + "if(typeof LvBridge.speak==='function'){/* native */} "
                + "}catch(e){}"
                + "try{if(typeof speechSynthesis.onvoiceschanged==='function'||speechSynthesis.onvoiceschanged===null)"
                + "{var ev=speechSynthesis.onvoiceschanged;setTimeout(function(){try{if(ev)ev();}catch(e){}},0);}"
                + "}catch(e){}"
                + "return true;}catch(e){return false;}}"
                + "try{(function(){if(document.getElementById('lv-apk-scroll-fluid'))return;var st=document.createElement('style');st.id='lv-apk-scroll-fluid';st.textContent='html,body{-webkit-overflow-scrolling:touch!important;}.shelf-icons,.shelf-row,.shelves,main,#shelves,.shelf{-webkit-overflow-scrolling:touch!important;touch-action:pan-x pan-y!important;}.shelf-icons{touch-action:pan-x!important;min-width:0!important;}.shelf-parade-ghost{display:none!important;}';(document.documentElement||document.head).appendChild(st);})();}catch(e){}"
                + "__lvInstallTts();"
                + "setTimeout(__lvInstallTts,0);setTimeout(__lvInstallTts,30);setTimeout(__lvInstallTts,120);"
                + "})();";
    }

    private void injectHelpers() {
        if (webView == null) return;
        // Preferencias wizard → localStorage + hide modules no elegidos
        String prefsJson = "null";
        try {
            prefsJson = prefs.toJson().toString();
        } catch (Exception ignored) {
        }
        String safePrefs = prefsJson
                .replace("\\", "\\\\")
                .replace("'", "\\'");
        // Re-aplicar boot (por si document-start no está) + prefs + parade OFF + scroll fluido
        String js = "(function(){"
                + "try{window.__lvNoParade=1;window.__lvForceParade=0;"
                + "try{window.startShelfDrift=function(){};window.__lvKickParade=function(){};window.__lvRestartParade=function(){};}catch(eNP){}"
                + "var __mm=window.matchMedia;if(!window.__lvMmPatched){window.__lvMmPatched=1;"
                + "window.matchMedia=function(q){q=String(q||'');if(q.indexOf('prefers-reduced-motion')>=0){"
                + "return{matches:false,media:q,addListener:function(){},removeListener:function(){},"
                + "addEventListener:function(){},removeEventListener:function(){},onchange:null,"
                + "dispatchEvent:function(){return false;}};}return __mm.call(window,q);};}}catch(e){}"
                // TTS shim (idempotente)
                + "try{(function(){if(!window.LvBridge||typeof LvBridge.ttsSpeak!=='function')return;"
                + "if(window.__lvTtsShim)return;window.__lvTtsShim=1;"
                + "function LvUtt(t){this.text=t||'';this.lang='es-ES';this.rate=1;this.pitch=1;"
                + "this.volume=1;this.onend=null;this.onerror=null;this.onstart=null;this.voice=null;}"
                + "var _utt=null,_poll=null;function clearPoll(){if(_poll){clearInterval(_poll);_poll=null;}}"
                + "var synth={speaking:false,pending:false,paused:false,"
                + "getVoices:function(){return[{name:'LesVencimos-TTS',lang:'es-ES',localService:true,default:true,voiceURI:'lesvencimos-native'}];},"
                + "cancel:function(){try{LvBridge.ttsCancel();}catch(e){}this.speaking=false;clearPoll();_utt=null;},"
                + "pause:function(){},resume:function(){},"
                + "speak:function(u){if(!u)return;var self=this;clearPoll();try{LvBridge.ttsCancel();}catch(e){}"
                + "var text=String(u.text||'');if(!text)return;var lang=u.lang||'es-ES';"
                + "var rate=u.rate!=null?Number(u.rate):1;var pitch=u.pitch!=null?Number(u.pitch):1;"
                + "_utt=u;self.speaking=true;try{if(u.onstart)u.onstart();}catch(e){}"
                + "try{LvBridge.ttsSpeak(text,lang,rate,pitch);}catch(e){self.speaking=false;try{if(u.onerror)u.onerror(e);}catch(x){}return;}"
                + "_poll=setInterval(function(){var sp=false;try{sp=!!LvBridge.ttsIsSpeaking();}catch(e){}"
                + "if(!sp){clearPoll();self.speaking=false;var done=_utt;_utt=null;try{if(done&&done.onend)done.onend();}catch(e){}}},120);}};"
                + "try{Object.defineProperty(window,'speechSynthesis',{configurable:true,enumerable:true,get:function(){return synth;},set:function(){}});}catch(e){window.speechSynthesis=synth;}"
                + "try{window.SpeechSynthesisUtterance=LvUtt;}catch(e){}"
                + "try{window.Android=window.Android||{};window.Android.speak=function(tx){try{if(typeof LvBridge.speak==='function')LvBridge.speak(String(tx||''));else LvBridge.ttsSpeak(String(tx||''),'es-ES',1,1);}catch(e){}};window.lvSpeak=window.Android.speak;}catch(e){}"
                + "})();}catch(e){}"
                + "if(window.__lvFatHelpers){try{window.__lvEnsureScrollFluid&&window.__lvEnsureScrollFluid();}catch(e){}return;}"
                + "window.__lvFatHelpers=1;"

                // Fat Completo: ocultar Añadir / ZIP / catálogo (si isFatOffline)
                + "try{if(window.LvBridge&&typeof LvBridge.isFatOffline==='function'&&LvBridge.isFatOffline()){"
                + "localStorage.setItem('lv-fat-offline','1');"
                + "localStorage.setItem('lv-no-download','1');"
                + "window.__lvFatOffline=1;window.__lvNoDownload=1;"
                + "if(!document.getElementById('lv-fat-no-dl')){"
                + "var st=document.createElement('style');st.id='lv-fat-no-dl';"
                + "st.textContent='label.file-btn,#local-file,.bar-anadir,#btnPickZip,#btnIrCompleto,"
                + "#btnInstalarSel,#disponibles,#atajoInstala,#menuAnadir,#btnAtajoAnadir,"
                + "#btnExportar+*,.tile[data-id=_anadir],[data-id=_anadir]{display:none!important}';"
                + "document.documentElement.appendChild(st);}"
                + "}}catch(e){}"

                // Hide Añadir
                + "try{(function(){function hideAnadir(){try{var ids=['local-file','file-err','btnAtajoAnadir','menuAnadir'];ids.forEach(function(id){var el=document.getElementById(id);if(el){el.style.display='none';el.hidden=true;}});document.querySelectorAll('button,a').forEach(function(el){var t=(el.textContent||'').replace(/\\s+/g,' ').trim();if(t.indexOf('Añadir')===0||t.indexOf('Anadir')===0){el.style.display='none';el.hidden=true;}});}catch(e){}}hideAnadir();setTimeout(hideAnadir,400);setTimeout(hideAnadir,1500);window.__lvHideAnadir=1;})();}catch(e){}"
                + "try{var P=JSON.parse('" + safePrefs + "');"
                + "localStorage.setItem('lv-app-prefs',JSON.stringify(P));"
                + "window.__lvAppPrefs=P;"
                + "if(P&&P.wizardDone){try{localStorage.setItem('lv-onboarding-done-v1','1');}catch(eOn){}}"
                + "if(P&&P.mode==='custom'&&Array.isArray(P.visibleModules)){"
                + "var allow={};P.visibleModules.forEach(function(id){allow[id]=1;});allow['pack-1eso']=1;"
                + "function hide(){try{"
                + "document.querySelectorAll('[data-pack],[data-module],[data-id]').forEach(function(el){"
                + "var id=el.getAttribute('data-pack')||el.getAttribute('data-module')||el.getAttribute('data-id');"
                + "if(id&&id.indexOf('pack-')===0&&!allow[id]){el.style.display='none';}"
                + "});"
                + "}catch(e){}};"
                + "hide();setTimeout(hide,500);setTimeout(hide,2000);"
                + "}"
                + "}catch(e){}"
                // seedFull / Educación siempre (k9 fat)
                + "try{if(typeof seedFullDesktop==='function'){seedFullDesktop();}else if(typeof fillDesktop==='function'){fillDesktop(true);}if(typeof ensureEducacionFolder==='function'){ensureEducacionFolder();}if(typeof arrangeToShelves==='function'){arrangeToShelves();}if(typeof renderChips==='function'){renderChips();}setTimeout(function(){try{if(typeof seedFullDesktop==='function')seedFullDesktop();if(typeof ensureEducacionFolder==='function')ensureEducacionFolder();if(typeof arrangeToShelves==='function')arrangeToShelves();}catch(e2){}},600);}catch(eSeed){}"
                // Parade OFF + scroll fluido (stamp j): sin KickParade / sin ghosts 240vw
                + "try{window.__lvEnsureScrollFluid=function(){"
                + "try{if(!document.getElementById('lv-apk-scroll-fluid')){"
                + "var st=document.createElement('style');st.id='lv-apk-scroll-fluid';"
                + "st.textContent='html,body{-webkit-overflow-scrolling:touch!important;}"
                + ".shelf-icons,.shelf-row,.shelves,main,#shelves,.shelf{"
                + "-webkit-overflow-scrolling:touch!important;touch-action:pan-x pan-y!important;}"
                + ".shelf-icons{touch-action:pan-x!important;min-width:0!important;}"
                + ".shelf-parade-ghost{display:none!important;}"
                + "#lv-apk-parade-force{display:none!important;}';"
                + "(document.head||document.documentElement).appendChild(st);}"
                + "var old=document.getElementById('lv-apk-parade-force');if(old)try{old.remove();}catch(eR){}"
                + "document.querySelectorAll('.shelf-parade-ghost').forEach(function(g){try{g.remove();}catch(eG){}});"
                + "document.querySelectorAll('.shelf-icons').forEach(function(el){"
                + "try{el.style.minWidth='';el.style.paddingRight='';"
                + "el.style.touchAction='pan-x';el.style.webkitOverflowScrolling='touch';}catch(e1){}});"
                + "}catch(eK){}};"
                + "window.__lvKickParade=function(){};"
                + "window.__lvEnsureScrollFluid();"
                + "setTimeout(window.__lvEnsureScrollFluid,300);"
                + "setTimeout(window.__lvEnsureScrollFluid,1200);"
                + "}catch(e){}"
                // AudioContext unlock (piano / Web Audio)
                + "function lvUnlockAc(){try{var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;"
                + "if(!window.__lvAc)window.__lvAc=new AC();if(window.__lvAc.state==='suspended')window.__lvAc.resume();}catch(e){}}"
                + "document.addEventListener('touchstart',lvUnlockAc,{passive:true});"
                + "document.addEventListener('mousedown',lvUnlockAc,{passive:true});"

                // 2.0.10: blob download → MediaStore vía LvBridge.saveAudioBase64
                + "try{(function(){if(window.__lvAudioSaveHook)return;window.__lvAudioSaveHook=1;"
                + "function b64FromBlob(blob,cb){var r=new FileReader();r.onload=function(){cb(null,String(r.result||''));};"
                + "r.onerror=function(){cb(r.error);};r.readAsDataURL(blob);}"
                + "document.addEventListener('click',function(ev){try{"
                + "if(!window.LvBridge||typeof LvBridge.saveAudioBase64!=='function')return;"
                + "var a=ev.target&&ev.target.closest?ev.target.closest('a[download]'):null;"
                + "if(!a||!a.href)return;var href=a.href;"
                + "if(href.indexOf('blob:')!==0&&href.indexOf('data:')!==0)return;"
                + "ev.preventDefault();ev.stopPropagation();"
                + "var name=a.getAttribute('download')||('grabacion-'+Date.now()+'.webm');"
                + "function saveDataUrl(du){try{var r=LvBridge.saveAudioBase64(du,name,'');"
                + "console.log('lv save',r);}catch(e){console.error(e);}}"
                + "if(href.indexOf('data:')===0){saveDataUrl(href);return;}"
                + "fetch(href).then(function(res){return res.blob();}).then(function(blob){"
                + "b64FromBlob(blob,function(err,du){if(err||!du)return;saveDataUrl(du);});"
                + "}).catch(function(e){console.error(e);});"
                + "}catch(e){}});})();}catch(e){}"
                // 2.0.10: botón opcional pick vía bridge si existe #pick
                + "try{(function(){if(window.__lvPickHook)return;window.__lvPickHook=1;"
                + "window.addEventListener('lv:audio-picked',function(ev){try{"
                + "var d=ev&&ev.detail;if(!d||!d.ok||!d.url)return;"
                + "if(typeof window.__lvOnAudioPicked==='function'){window.__lvOnAudioPicked(d);return;}"
                + "var audio=document.querySelector('audio');if(audio){audio.src=d.url;try{audio.play();}catch(e){}}"
                + "}catch(e){}});})();}catch(e){}"

                + "})();";
        webView.evaluateJavascript(js, null);

        // data helpers (lvAlmacen → filesDir/data)
        String dataJs = "(function(){"
                + "if(window.__lvDataHelpers)return;window.__lvDataHelpers=1;"
                + "if(!window.LvBridge||typeof LvBridge.writeData!=='function')return;"
                + "function idFromPath(){try{var parts=location.pathname.split('/').filter(Boolean);"
                + "var i=parts.indexOf('modules');if(i<0)i=parts.indexOf('modulos');if(i>=0&&parts[i+1])return parts[i+1];}catch(e){}return null;}"
                + "function parseDatos(raw){if(!raw)return null;try{var o=JSON.parse(raw);if(o&&o.datos!==undefined)return o.datos;return o;}catch(e){return null;}}"
                + "var api={id:idFromPath(),"
                + "leer:function(id){id=id||this.id;if(!id)return null;try{return parseDatos(LvBridge.readData(id));}catch(e){return null;}},"
                + "escribir:function(obj,id){id=id||this.id;if(!id)return false;try{var body=(typeof obj==='string')?obj:JSON.stringify(obj);"
                + "var r=LvBridge.writeData(id,body);var j=JSON.parse(r);return !!(j&&j.ok);}catch(e){return false;}}};"
                + "window.lvAlmacen=api;"
                + "})();";
        webView.evaluateJavascript(dataJs, null);
    }

    @SuppressLint({"SetJavaScriptEnabled", "JavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setVolumeControlStream(AudioManager.STREAM_MUSIC);

        prefs = new AppPrefs(this);
        prefs.migrateK9(); // Educación siempre + fat flags + marker k9
        File modulesRoot = new File(PackExtractor.contentRoot(this), "modules");
        store = new ModuleStore(this, modulesRoot,
                new File(getFilesDir(), "data"), getCacheDir());
        bridge = new LvBridge(this, store);
        tts = new LvTts(this);
        bridge.setTts(tts);

        webView = findViewById(R.id.webview);
        extractOverlay = findViewById(R.id.extract_overlay);
        extractBar = findViewById(R.id.extract_bar);
        extractLabel = findViewById(R.id.extract_label);

        File contentRoot = PackExtractor.contentRoot(this);
        //noinspection ResultOfMethodCallIgnored
        contentRoot.mkdirs();

        assetLoader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .addPathHandler("/completo/",
                        new WebViewAssetLoader.InternalStoragePathHandler(this, contentRoot))
                .build();

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setAllowFileAccessFromFileURLs(false);
        s.setAllowUniversalAccessFromFileURLs(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        // Fat: zoom off (compite con parade). Flaco: zoom on.
        s.setSupportZoom(BuildConfig.FLACO_MODE);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        // Scroll touch fluido (Completo j): no bloquear overscroll del contenido.
        webView.setOverScrollMode(View.OVER_SCROLL_IF_CONTENT_SCROLLS);
        webView.setNestedScrollingEnabled(true);
        webView.setHorizontalScrollBarEnabled(false);
        webView.setVerticalScrollBarEnabled(false);
        webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        if (android.os.Build.VERSION.SDK_INT >= 23) {
            s.setOffscreenPreRaster(true);
        }
        // Mantener animaciones/JS timers vivos para desfile de baldas.
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);

        webView.addJavascriptInterface(bridge, "LvBridge");
        // Document-start: reduced-motion bypass + TTS shim ANTES del JS de estantería/Maestro
        if (WebViewFeature.isFeatureSupported(WebViewFeature.DOCUMENT_START_SCRIPT)) {
            try {
                WebViewCompat.addDocumentStartJavaScript(
                        webView, bootScript(), Set.of("*"));
            } catch (Exception e) {
                Log.w(TAG, "DOCUMENT_START_SCRIPT", e);
            }
        }
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                main.post(() -> {
                    if (request == null) return;
                    String[] resources = request.getResources();
                    boolean wantsAudio = false;
                    if (resources != null) {
                        for (String r : resources) {
                            if (PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(r)) {
                                wantsAudio = true;
                                break;
                            }
                        }
                    }
                    if (wantsAudio) {
                        ensureMicThenGrant(request);
                    } else {
                        // Solo concedemos audio; denegar cámara u otros
                        try { request.deny(); } catch (Exception ignored) {}
                    }
                });
            }

            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> callback,
                                             WebChromeClient.FileChooserParams params) {
                if (filePathCallback != null) {
                    filePathCallback.onReceiveValue(null);
                }
                filePathCallback = callback;
                Intent intent = null;
                try {
                    intent = params != null ? params.createIntent() : null;
                } catch (Exception e) {
                    Log.w(TAG, "createIntent", e);
                }
                if (intent == null) {
                    intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                    intent.addCategory(Intent.CATEGORY_OPENABLE);
                    intent.setType("audio/*");
                    intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                } else {
                    // Prefer OPEN_DOCUMENT for persistable grants when possible
                    String type = intent.getType();
                    if (type == null || "*/*".equals(type) || type.startsWith("audio")) {
                        Intent open = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                        open.addCategory(Intent.CATEGORY_OPENABLE);
                        open.setType(type != null && type.startsWith("audio") ? type : "audio/*");
                        open.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                        if (params != null && params.getAcceptTypes() != null
                                && params.getAcceptTypes().length > 0) {
                            open.putExtra(Intent.EXTRA_MIME_TYPES, params.getAcceptTypes());
                        }
                        open.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                        intent = open;
                    }
                }
                try {
                    fileChooserLauncher.launch(intent);
                    return true;
                } catch (ActivityNotFoundException e) {
                    try {
                        Intent alt = new Intent(Intent.ACTION_GET_CONTENT);
                        alt.addCategory(Intent.CATEGORY_OPENABLE);
                        alt.setType("audio/*");
                        alt.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                        fileChooserLauncher.launch(alt);
                        return true;
                    } catch (ActivityNotFoundException e2) {
                        filePathCallback = null;
                        Toast.makeText(MainActivity.this, "No hay gestor de archivos",
                                Toast.LENGTH_SHORT).show();
                        return false;
                    }
                }
            }
        });

        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(String url, String userAgent, String contentDisposition,
                                        String mimeType, long contentLength) {
                // blob: no se puede leer desde nativo — el inject Helpers usa LvBridge.saveAudioBase64
                if (url == null || url.startsWith("blob:") || url.startsWith("data:")) {
                    Toast.makeText(MainActivity.this,
                            "Usa «Guardar en LesVencimos» o el puente nativo para conservar el audio",
                            Toast.LENGTH_SHORT).show();
                    return;
                }
                io.execute(() -> {
                    try {
                        byte[] data;
                        if (url.startsWith("content:") || url.startsWith("file:")) {
                            try (java.io.InputStream in = getContentResolver()
                                    .openInputStream(Uri.parse(url))) {
                                if (in == null) throw new IllegalArgumentException("no stream");
                                java.io.ByteArrayOutputStream bos = new java.io.ByteArrayOutputStream();
                                byte[] buf = new byte[8192];
                                int n; int total = 0;
                                while ((n = in.read(buf)) > 0) {
                                    total += n;
                                    if (total > 80 * 1024 * 1024) throw new IllegalArgumentException("grande");
                                    bos.write(buf, 0, n);
                                }
                                data = bos.toByteArray();
                            }
                        } else {
                            return; // no descargar http arbitrario en fat offline
                        }
                        String name = "descarga-" + System.currentTimeMillis() + ".bin";
                        if (contentDisposition != null && contentDisposition.contains("filename=")) {
                            int i = contentDisposition.indexOf("filename=");
                            name = contentDisposition.substring(i + 9).replace("\"", "").trim();
                        }
                        org.json.JSONObject meta = LvMedia.saveAudio(MainActivity.this, data, name, mimeType);
                        main.post(() -> {
                            bridgeEmit("audio-saved", meta.toString());
                            Toast.makeText(MainActivity.this,
                                    "Guardado en " + meta.optString("relativePath", LvMedia.FOLDER),
                                    Toast.LENGTH_SHORT).show();
                        });
                    } catch (Exception e) {
                        Log.e(TAG, "download", e);
                        main.post(() -> Toast.makeText(MainActivity.this,
                                "No se pudo guardar", Toast.LENGTH_SHORT).show());
                    }
                });
            }
        });


        final File root = contentRoot;
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (uri != null && HOST.equals(uri.getHost())) {
                    String path = uri.getPath() != null ? uri.getPath() : "";
                    // /user-audio/** → cacheDir/user-audio (grabaciones / picks)
                    if (path.startsWith("/user-audio/") || "/user-audio".equals(path)) {
                        String rel = path.startsWith("/user-audio/")
                                ? path.substring("/user-audio/".length()) : "";
                        if (!rel.isEmpty() && !rel.contains("..")) {
                            WebResourceResponse r = serveFile(LvMedia.cacheDir(MainActivity.this), rel);
                            if (r != null) return withFixedMime(uri, r);
                        }
                    }
                    // /educacion/** → filesDir/completo/educacion/** (post-extract)
                    if (path.startsWith("/educacion/") || "/educacion".equals(path)) {
                        String rel = path.startsWith("/educacion/")
                                ? path.substring(1) // educacion/...
                                : "educacion/index.html";
                        WebResourceResponse r = serveFile(root, rel);
                        if (r != null) return withFixedMime(uri, r);
                        return missingLocalHtml("Educación",
                                "No está en el pack local: " + path
                                + " — usa educacion/… (p. ej. educacion/Profesor.html).");
                    }
                    // Legacy /profesor/** → map to educacion/ or clear offline message
                    if (path.startsWith("/profesor/") || "/profesor".equals(path)
                            || "/Profesor.html".equals(path) || "/profesor.html".equals(path)) {
                        String mapped;
                        if ("/Profesor.html".equals(path) || "/profesor.html".equals(path)
                                || "/profesor".equals(path) || "/profesor/".equals(path)) {
                            mapped = "educacion/Profesor.html";
                        } else {
                            // /profesor/1eso-mates/... → educacion/1eso-mates/...
                            mapped = "educacion/" + path.substring("/profesor/".length());
                        }
                        WebResourceResponse r = serveFile(root, mapped);
                        if (r != null) {
                            Log.i(TAG, "map " + path + " → " + mapped);
                            return withFixedMime(uri, r);
                        }
                        return missingLocalHtml("Profesor / Educación",
                                "Ruta antigua /profesor/ no encontrada en pack. "
                                + "Abre Educación desde la estantería (educacion/…), no /profesor/.");
                    }
                    // Alias /modules/ y /modulos/ → filesDir post-extract
                    if (path.startsWith("/modules/") || path.startsWith("/modulos/")) {
                        String rel = path.startsWith("/modules/")
                                ? path.substring("/modules/".length())
                                : path.substring("/modulos/".length());
                        WebResourceResponse r = serveFile(new File(root, "modules"), rel);
                        if (r == null) r = serveFile(new File(root, "modulos"), rel);
                        if (r == null) {
                            File hit = PackExtractor.resolveModuloFile(root, rel);
                            if (hit != null) {
                                try {
                                    String rootCanon = root.getCanonicalPath();
                                    String hitCanon = hit.getCanonicalPath();
                                    if (hitCanon.startsWith(rootCanon + File.separator)) {
                                        String relHit = hitCanon.substring(rootCanon.length() + 1);
                                        r = serveFile(root, relHit);
                                    }
                                } catch (Exception e) {
                                    Log.w(TAG, "modulos resolve " + rel, e);
                                }
                            }
                        }
                        if (r != null) return withFixedMime(uri, r);
                    }
                    if (path.startsWith("/completo/")) {
                        WebResourceResponse r = serveFile(root, path.substring("/completo/".length()));
                        if (r != null) return withFixedMime(uri, r);
                    }
                }
                WebResourceResponse resp = assetLoader.shouldInterceptRequest(uri);
                return withFixedMime(uri, resp);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                injectHelpers();
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String host = uri.getHost() != null ? uri.getHost() : "";
                String scheme = uri.getScheme() != null ? uri.getScheme() : "";
                if (HOST.equals(host)) return false;
                if ("http".equals(scheme) || "https".equals(scheme)) {
                    try {
                        startActivity(new Intent(Intent.ACTION_VIEW, uri));
                    } catch (ActivityNotFoundException e) {
                        Toast.makeText(MainActivity.this, "No hay navegador", Toast.LENGTH_SHORT).show();
                    }
                    return true;
                }
                return false;
            }
        });

        startBootstrap();
    }

    private void startBootstrap() {
        if (BuildConfig.FLACO_MODE) {
            hideExtractOverlay();
            openEstanteria();
            return;
        }
        if (PackExtractor.isExtracted(this)) {
            PackExtractor.ensureModulosIndex(this);
            hideExtractOverlay();
            goNext();
            return;
        }
        showExtractOverlay("Preparando Les vencimos…");
        io.execute(() -> {
            try {
                PackExtractor.extractIfNeeded(this, (pct, msg) -> main.post(() -> {
                    if (extractBar != null) extractBar.setProgress(pct);
                    if (extractLabel != null) extractLabel.setText(msg);
                }));
                main.post(() -> {
                    hideExtractOverlay();
                    goNext();
                });
            } catch (Exception e) {
                Log.e(TAG, "extract failed", e);
                main.post(() -> {
                    hideExtractOverlay();
                    String err = e.getMessage() != null ? e.getMessage() : "error";
                    String html = "<!DOCTYPE html><html lang=es><meta charset=utf-8>"
                            + "<meta name=viewport content=\"width=device-width,initial-scale=1\">"
                            + "<body style=\"background:#0E0E0C;color:#E6E1D6;font:1rem system-ui;padding:2rem\">"
                            + "<h1>No se pudo preparar el contenido</h1><p>" + err + "</p>"
                            + "<p>Reinstala la app o libera espacio.</p></body></html>";
                    webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null);
                });
            }
        });
    }

    private void goNext() {
        if (!prefs.isWizardDone()) {
            openWizard();
        } else {
            openEstanteria();
        }
    }

    private void showExtractOverlay(String msg) {
        if (extractOverlay != null) extractOverlay.setVisibility(View.VISIBLE);
        if (extractLabel != null) extractLabel.setText(msg);
        if (extractBar != null) extractBar.setProgress(0);
    }

    private void hideExtractOverlay() {
        if (extractOverlay != null) extractOverlay.setVisibility(View.GONE);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) {
            webView.onResume();
            webView.resumeTimers();
            // Parade OFF (2.0.6): reafirmar scroll fluido; no drift.
            webView.evaluateJavascript(
                    "(function(){try{"
                    + "window.__lvNoParade=1;window.__lvForceParade=0;"
                    + "try{window.startShelfDrift=function(){};}catch(e){}"
                    + "if(window.__lvEnsureScrollFluid)window.__lvEnsureScrollFluid();"
                    + "}catch(e){}})();",
                    null);
        }
    }

    @Override
    protected void onPause() {
        // No pauseTimers(): evita congelar timers UI; parade OFF — no reiniciar drift.
        if (webView != null) {
            webView.onPause();
            // Explicit: never pauseTimers() — Chromium congela requestAnimationFrame.
        }
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        if (tts != null) {
            tts.shutdown();
            tts = null;
        }
        io.shutdownNow();
        super.onDestroy();
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
