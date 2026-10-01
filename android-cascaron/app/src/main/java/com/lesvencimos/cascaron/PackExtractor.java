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
            ? "v20261001k6" : "v20261001embed-k6";

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

        long totalHint = 34206487L;
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
