"""Detección ligera de estrellas en una imagen en escala de grises (lista de filas)."""
import statistics


def detect_stars(img, k=4.0, max_stars=20, min_pixels=1):
    h = len(img)
    w = len(img[0]) if h else 0
    flat = [p for row in img for p in row]
    if not flat:
        return []
    bg = statistics.median(flat)               # fondo (contaminación lumínica)
    sd = statistics.pstdev(flat) or 1.0
    thr = bg + k * sd
    seen = [[False] * w for _ in range(h)]
    blobs = []
    for y in range(h):
        for x in range(w):
            if img[y][x] <= thr or seen[y][x]:
                continue
            stack, pix = [(x, y)], []
            seen[y][x] = True
            while stack:
                cx, cy = stack.pop()
                pix.append((cx, cy))
                for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and img[ny][nx] > thr:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if len(pix) < min_pixels:
                continue
            flux = sum(img[py][px] - bg for px, py in pix)
            cx = sum((img[py][px] - bg) * px for px, py in pix) / flux
            cy = sum((img[py][px] - bg) * py for px, py in pix) / flux
            blobs.append({"x": cx, "y": cy, "flux": flux})
    blobs.sort(key=lambda b: b["flux"], reverse=True)
    return blobs[:max_stars]
