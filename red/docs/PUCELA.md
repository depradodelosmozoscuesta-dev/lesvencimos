# Formato `.pucela` (v6) — contenedor sellado especial

## Qué es (y qué no es)

`.pucela` es el **formato propietario** de documento ciudadano de esta red:

- **Cifrado de verdad**: cerrojo NaCl (X25519 efímera + box) hacia la clave box del destinatario (nodo/sesión oficial).
- **No es HTML**, ni PDF, ni un **zip disfrazado**.
- Partes permitidas: **texto**, **imagen fija**, **sonido**. **Sin vídeo**.
- Las fotos grandes **nunca se rechazan**: `FitImage` redimensiona/recomprimes hasta caber (≤1600 px lado largo, ≤512 KiB).

Versión de aplicación: **5.16.0**. Byte de formato en cable / manifiesto: **6** (se sigue leyendo **5**).

## Layout sellado

```
[7]  magic "PUCELA\x00"
[1]  version (5 o 6)
[32] ephemeral X25519 public
[24] nonce
[N]  NaCl box(ciphertext) de EncodeClear(manifest JSON + blobs)
```

Solo quien tiene la **box privada** del destinatario puede `Unseal`.

## Canal de audio codificado (v6)

### Por qué

El cerrojo ya protege el contenido. El **canal** es un *side-channel* embebido:

1. Tip lateral de integridad (`doc_id`, `author_id`, versión, hash-tip) verificable al abrir.
2. Un reproductor genérico solo oye **ruido/tonos suaves**; el cliente oficial decodifica datos.
3. Deja claro que el formato **no es un contenedor genérico** tipo zip.

### Cómo se genera

Al `Pack` (antes de `Sign`):

1. Si falta una parte `sound` con `role=canal`, se genera `canal.wav`.
2. Payload JSON (≤ ~512 B): `{doc_id, author_id, format, tip, notice?}`.
3. `tip` = prefijo hex (16 chars) de SHA-256 sobre manifiesto (sin sig/canal) + hashes de blobs no-canal.
4. Metadatos en manifiesto: `channel: {encoding, bytes}`.

### Encoding `pcm16-lsb-v1`

| Pieza | Detalle |
|-------|---------|
| Contenedor | WAV PCM **mono**, **16-bit LE**, **8000 Hz** |
| Transporte | LSB de cada muestra = 1 bit del frame |
| Frame | `sync 0xA55A` + magic `PCCH` + `len` u16 BE + payload + CRC32 IEEE |
| Orden de bits | MSB first dentro de cada byte del frame |
| Audible | amplitud ~1200 con tono suave ~100 Hz; el LSB no se oye como mensaje |

### Verificación al abrir

`Unseal` / `OpenDoc`:

- Wire **v5** sin canal → OK (compat).
- **v6** sin canal → **rechazo**.
- Canal presente pero `doc_id` / `author_id` / tip / CRC no cuadran → **fail-closed**.

## API útil

| Ruta | Rol |
|------|-----|
| `GET /api/pucela/limits` | Topes + `format_version` + `channel_encoding` |
| `POST /api/pucela` | Pack + Sign + Seal (v6 + canal) |
| `POST /api/pucela/{id}/open` | Unseal + verify canal |
| `GET /api/whoami` | Expone `box_public` (necesaria para reseello federado) |

## Reseello federado (taller)

Ver [`TALLER-FEDERACION.md`](TALLER-FEDERACION.md): el peer **Unseal** local → **Seal** a `box_public` del origen → upload. El origen solo `ImportSealed`.

## Cómo probar

```bash
go test ./internal/pucela/ -count=1
go test ./internal/api/ -run TallerArtifactPucela -count=1

# Manual
make run
# UI → pestaña Pucela → crear carta → abrir
curl -s http://127.0.0.1:8080/api/pucela/limits | jq .
```

## Limitaciones

- El canal **no sustituye** el cerrojo: sin la box privada no hay claro.
- Payload lateral pequeño (ids + tip + aviso corto); no es un segundo documento.
- Al reseellar un paquete **v5** antiguo a v6 se puede limpiar la firma Ed25519 (el tip de canal cubre integridad del contenido empaquetado).
- `PutSealedRaw` sigue existiendo para espejos legacy, pero el upload de taller **exige** reseello abríble en origen.
