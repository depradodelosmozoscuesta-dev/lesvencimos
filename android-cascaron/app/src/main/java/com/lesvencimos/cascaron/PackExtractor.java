package com.lesvencimos.cascaron;

import android.content.Context;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

/**
 * Extrae assets/embed/completo-offline.zip → filesDir/completo/ en la 1ª ejecución.
 */
public final class PackExtractor {
    private static final String TAG = "PackExtractor";
    public static final String ASSET_ZIP = "embed/completo-offline.zip";
    public static final String CONTENT_DIR = "completo";
    public static final String MARKER = ".lv-extracted";
    public static final String EXPECTED_VERSION = BuildConfig.FLACO_MODE
            ? "v20261001k6" : "v20261005embed-claridad";

    public interface Progress {
        void onProgress(int percent, String message);
    }

    private PackExtractor() {}

    public static File contentRoot(Context ctx) {
        return new File(ctx.getFilesDir(), CONTENT_DIR);
    }

    public static boolean isExtracted(Context ctx) {
        File marker = new File(contentRoot(ctx), MARKER);
        if (!marker.isFile()) return false;
        try {
            String v = readSmall(marker).trim();
            File entry = new File(contentRoot(ctx), "estanteria.html");
            return EXPECTED_VERSION.equals(v) && entry.isFile();
        } catch (Exception e) {
            return false;
        }
    }

    public static void extractIfNeeded(Context ctx, Progress progress) throws Exception {
        if (isExtracted(ctx)) {
            if (progress != null) progress.onProgress(100, "Listo");
            return;
        }
        File root = contentRoot(ctx);
        if (root.exists()) {
            deleteRecursive(root);
        }
        if (!root.mkdirs()) {
            throw new IllegalStateException("No se pudo crear " + root);
        }
        if (progress != null) progress.onProgress(1, "Preparando contenido…");

        long totalHint = 80000000L;
        long written = 0;
        byte[] buf = new byte[64 * 1024];
        try (InputStream raw = ctx.getAssets().open(ASSET_ZIP);
             ZipInputStream zis = new ZipInputStream(new BufferedInputStream(raw, 65536))) {
            ZipEntry entry;
            int count = 0;
            while ((entry = zis.getNextEntry()) != null) {
                String name = entry.getName();
                if (name == null || name.contains("..")) {
                    zis.closeEntry();
                    continue;
                }
                // Normalizar: sin prefijo absolute
                while (name.startsWith("/")) name = name.substring(1);
                File out = new File(root, name);
                if (entry.isDirectory()) {
                    //noinspection ResultOfMethodCallIgnored
                    out.mkdirs();
                    zis.closeEntry();
                    continue;
                }
                File parent = out.getParentFile();
                if (parent != null) {
                    //noinspection ResultOfMethodCallIgnored
                    parent.mkdirs();
                }
                try (BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(out), 65536)) {
                    int n;
                    while ((n = zis.read(buf)) > 0) {
                        bos.write(buf, 0, n);
                        written += n;
                    }
                }
                zis.closeEntry();
                count++;
                if (progress != null && count % 25 == 0) {
                    int pct = (int) Math.min(99, Math.max(2, (written * 100) / Math.max(totalHint, 1)));
                    progress.onProgress(pct, "Instalando… " + pct + "%");
                }
            }
        }
        File est = new File(root, "estanteria.html");
        if (!est.isFile()) {
            throw new IllegalStateException("ZIP sin estanteria.html");
        }
        writeSmall(new File(root, MARKER), EXPECTED_VERSION + "\n");
        if (progress != null) progress.onProgress(100, "Contenido listo");
        Log.i(TAG, "Extracted to " + root.getAbsolutePath());
    }

    /**
     * Resuelve /modulos/&lt;rel&gt; cuando la ruta directa no cae en modulos/ ni modules/.
     * Solo devuelve un fichero dentro de root (sin ..).
     */
    public static File resolveModuloFile(File root, String rel) {
        if (root == null || rel == null) return null;
        String r = rel;
        try {
            r = java.net.URLDecoder.decode(r, java.nio.charset.StandardCharsets.UTF_8.name());
        } catch (Exception ignored) {
        }
        while (r.startsWith("/")) r = r.substring(1);
        if (r.isEmpty() || r.contains("..") || r.indexOf('\\') >= 0) return null;
        String[] bases = new String[] {
                "modulos/" + r,
                "modules/" + r,
                r
        };
        for (String base : bases) {
            File hit = underRoot(root, base);
            if (hit != null) return hit;
            if (!base.endsWith(".html") && !base.endsWith(".htm")) {
                File html = underRoot(root, base + ".html");
                if (html != null) return html;
            }
        }
        return null;
    }

    /** Idempotente. El ZIP ya trae modulos/ plano; no reescribe la estantería ni el TTS. */
    public static void ensureModulosIndex(Context ctx) {
        File mod = new File(contentRoot(ctx), "modulos");
        if (!mod.isDirectory()) {
            Log.w(TAG, "ensureModulosIndex: falta modulos/");
            return;
        }
        File[] html = mod.listFiles((dir, name) -> name.endsWith(".html"));
        int n = html == null ? 0 : html.length;
        Log.i(TAG, "ensureModulosIndex: " + n + " html en modulos/");
    }

    private static File underRoot(File root, String rel) {
        try {
            File target = new File(root, rel);
            String rootCanon = root.getCanonicalPath();
            String fileCanon = target.getCanonicalPath();
            if (!fileCanon.equals(rootCanon) && !fileCanon.startsWith(rootCanon + File.separator)) {
                return null;
            }
            return target.isFile() ? target : null;
        } catch (Exception e) {
            return null;
        }
    }

    private static void deleteRecursive(File f) {
        if (f == null || !f.exists()) return;
        File[] kids = f.listFiles();
        if (kids != null) {
            for (File k : kids) deleteRecursive(k);
        }
        //noinspection ResultOfMethodCallIgnored
        f.delete();
    }

    private static String readSmall(File f) throws Exception {
        byte[] b = new byte[(int) Math.min(f.length(), 256)];
        try (InputStream in = new java.io.FileInputStream(f)) {
            int n = in.read(b);
            return n > 0 ? new String(b, 0, n, java.nio.charset.StandardCharsets.UTF_8) : "";
        }
    }

    private static void writeSmall(File f, String s) throws Exception {
        try (FileOutputStream out = new FileOutputStream(f)) {
            out.write(s.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        }
    }
}
