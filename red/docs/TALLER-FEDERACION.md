# Taller comunitario — federación (v5.14)

## Qué se comparte (índice público)

Entre nodos peers (allowlist de federación + sugerencias mDNS) **solo** viaja un
**índice público firmado** de proyectos del Taller:

| Campo | Significado |
|-------|-------------|
| `id` | Identificador del proyecto en el nodo de origen |
| `title` | Título |
| `category` | asistente / educacion / herramienta / otro |
| `status` | abierto / en_curso / cerrado |
| `blurb` | Resumen corto (recortado; no es la descripción completa de trabajo) |
| `origin_node_id` | Clave pública hex del nodo que lo publica |
| `updated_at` | Unix time de última actualización del proyecto |
| `open_tasks` | Conteo agregado (libres + reclamadas); **sin** títulos ni assignees |

El sobre `GET /api/taller/index` lleva `node_id`, `issued_at`, `projects[]` y
`sig` (Ed25519), el mismo patrón que el feed de federación.

## Reclamo de tareas (v5.11)

El **origen** del proyecto sigue siendo la fuente de verdad. Un peer **no**
sincroniza el tablero: pide al origen una lista mínima y envía acciones firmadas.

### DTO `PublicTask` (superficie mínima)

| Campo | Significado |
|-------|-------------|
| `id` / `proyecto_id` | Identificadores en el origen |
| `title` | Título corto |
| `status` | `open` / `claimed` / `done` |
| `claimer_tip` | Tip corto del node_id claimer (nunca el `claimed_by` completo en índice) |
| `blurb` | Opcional; solo en `open` (notas recortadas para decidir reclamar) |
| `updated_at` | Unix time |

### Endpoints en el origen

| Método | Ruta | Rol |
|--------|------|-----|
| `GET` | `/api/taller/proyectos/{id}/claimable` | Lista DTO mínimo (sin firma) |
| `POST` | `/api/taller/federacion/claim` | Body `SignedAction` — reclamar |
| `POST` | `/api/taller/federacion/release` | Liberar (solo el claimer) |
| `POST` | `/api/taller/federacion/complete` | Completar + aporte (metadatos + `file_id`/`pucela_id`) |
| `POST` | `/api/taller/federacion/upload` | **v5.12** Multipart `meta`+`blob` — artefacto ligero del claimer |

`SignedAction` se firma con la Ed25519 del nodo claimer (`claimer_node_id` =
pubkey hex). El origen verifica:

1. Firma válida y `issued_at` dentro de ±5 min.
2. `claimer_node_id` figura en la **allowlist** de federación (peer con NodeID).
3. Reglas de negocio: no double-claim; release/complete/upload solo del claimer.

### Transporte de artefactos (v5.12)

Cuando el peer B completa un claim **o** un job de cola en el origen A, puede
**subir el aporte** (fichero ligero y/o `.pucela`) para que la ref sea resoluble
en A.

| Pieza | Detalle |
|-------|---------|
| Meta firmada | `SignedUpload` (`action=upload`, `kind=file\|pucela`, `name`, `mime`, `size`, `sha256`) |
| Cuerpo | Multipart campo `blob` (tope **8 MiB** = `files.MaxBytes`) |
| Fichero ligero | `files.PutCivic` — plaintext en el store de `/api/files` (Nonce=`civic`) |
| `.pucela` | **v5.14 reseello**: el peer Unseal local → Seal a `box_public` del origen (`GET /api/whoami`) → upload; origen solo `ImportSealed` |
| Allowlist MIME | text/plain, markdown, csv, json, pdf, jpeg/png/gif/webp, octet-stream |
| Rate limit | `taller_fed` (misma política que claim/complete) |
| Autorización | claimer de tarea **o** arrendatario de job (`tarea_id` = `job_id`) |

### Reseello `.pucela` al origen (v5.14)

El aporte `.pucela` del peer suele estar sellado a la **box del peer**. El origen no podría abrirlo.

1. Peer resuelve URL del origen (allowlist / `origen_urls.json`).
2. `GET {origen}/api/whoami` → `box_public`.
3. `pucela.ResealFor(blob, boxPrivPeer, boxPubOrigen)` (abre, asegura canal v6, sella).
4. Multipart upload del ciphertext reseellado.
5. Origen: `ImportSealed` con su box; **rechaza** si no puede Unseal.
6. Sin `box_public` o si el peer no puede abrir su propio paquete → error (no se sube espejo opaco).

Detalle del formato: [`PUCELA.md`](PUCELA.md).

No es el camino de depósito grande / dead-drop: solo transferencias cívicas ligeras.

### Helpers en el peer local (UI)

| Método | Ruta | Rol |
|--------|------|-----|
| `GET` | `/api/taller/remoto/claimable?origin_node_id=&proyecto_id=` | Proxy → claimable del origen |
| `POST` | `/api/taller/remoto/claim` | Firma local + POST al origen |
| `POST` | `/api/taller/remoto/release` | Idem |
| `POST` | `/api/taller/remoto/upload` | Sube file/.pucela al origen (multipart) |
| `POST` | `/api/taller/remoto/complete` | JSON (refs) **o** multipart con `file`/`pucela` → upload + complete |
| `GET` | `/api/taller/remoto/mis-claims` | Recordatorio local (`claims_remotos.json`) |

La URL del origen se resuelve por allowlist (`PeerURLByNodeID`) o por la última
URL vista al hacer `POST /api/taller/sync` (`origen_urls.json`).

## Colas firmadas de trabajo (v5.13)

Complementario al claim por tarea: el origen publica una **cola de jobs**
(batch / “cada nodo procesa una rebanada”). El peer arrienda (lease) un job con
TTL, renueva (heartbeat) y entrega resultado.

### DTO `PublicJob`

| Campo | Significado |
|-------|-------------|
| `id` / `proyecto_id` | Identificadores en el origen |
| `title` / `blurb` | Título y resumen corto |
| `payload_ref` | Ref opcional (sin blob grande) |
| `payload` | Solo tras lease exitoso; inline ≤ **4 KiB** |
| `status` | `queued` / `leased` / `done` / `failed` |
| `holder_tip` | Tip del worker (nunca `lease_holder` completo en listado) |
| `lease_until` | Unix expiry del lease |
| `updated_at` | Unix time |
| `result_file_id` / `result_pucela_id` | Refs de resultado (en done/failed) |

### Lease TTL

| Constante | Valor |
|-----------|-------|
| Por defecto | **900 s (15 min)** |
| Mínimo | 60 s |
| Máximo | 3600 s (1 h) |

Al listar o arrendar, el origen **reclama** automáticamente leases expirados
(vuelven a `queued`). Renew / complete / fail con lease vencido → `lease expirado`.

### Endpoints en el origen

| Método | Ruta | Rol |
|--------|------|-----|
| `GET` | `/api/taller/proyectos/{id}/cola` | Lista DTO mínimo (sin payload) |
| `POST` | `/api/taller/proyectos/{id}/cola` | Crear job (local; `{title,blurb,payload,payload_ref}`) |
| `POST` | `/api/taller/federacion/cola/lease` | `SignedQueueAction` — siguiente o `job_id` concreto |
| `POST` | `/api/taller/federacion/cola/renew` | Extiende TTL (solo holder) |
| `POST` | `/api/taller/federacion/cola/complete` | Resultado + refs opcionales |
| `POST` | `/api/taller/federacion/cola/fail` | Marca failed |

`SignedQueueAction` (`action=lease|renew|job_complete|job_fail`) se firma con la
Ed25519 del worker (`worker_node_id`). El origen verifica firma, skew ±5 min,
allowlist y reglas: no double-lease; renew/complete/fail solo del holder; lease
no expirado.

### Helpers peer

| Método | Ruta | Rol |
|--------|------|-----|
| `GET` | `/api/taller/remoto/cola?origin_node_id=&proyecto_id=` | Ver cola remota |
| `POST` | `/api/taller/remoto/cola/lease` | Tomar siguiente o job concreto |
| `POST` | `/api/taller/remoto/cola/renew` | Heartbeat |
| `POST` | `/api/taller/remoto/cola/complete` | JSON o multipart (upload + complete) |
| `POST` | `/api/taller/remoto/cola/fail` | Fallar job |
| `GET` | `/api/taller/remoto/mis-leases` | Recordatorio local (`leases_remotos.json`) |

Persistencia en origen: `data-dir/taller/jobs.json`.

## Qué NO se sincroniza

- Descripciones largas / notas de **tareas** (salvo blurb corto en `open`)
- Tableros completos, chat, casas, depósitos
- Gossip de claims/leases entre terceros
- Blobs grandes de depósito / citas dead-drop (fuera de alcance)
- Payload de cola en el listado público (solo tras lease)

## Cómo probar con dos nodos

```bash
# Nodo A (origen)
go run ./cmd/node --addr 127.0.0.1:8080 --data-dir /tmp/rcv-a

# Nodo B (peer)
go run ./cmd/node --addr 127.0.0.1:8081 --data-dir /tmp/rcv-b \
  --peer-url http://127.0.0.1:8080

# Mutual allowlist
curl -s -X POST http://127.0.0.1:8080/api/federacion/peers \
  -H 'Content-Type: application/json' \
  -d '{"peer_url":"http://127.0.0.1:8081"}'
curl -s -X POST http://127.0.0.1:8081/api/federacion/peers \
  -H 'Content-Type: application/json' \
  -d '{"peer_url":"http://127.0.0.1:8080"}'

# En A: crear proyecto + job de cola
# PID=$(curl -s -X POST http://127.0.0.1:8080/api/taller/proyectos \
#   -H 'Content-Type: application/json' \
#   -d '{"titulo":"Batch vecinal","categoria":"educacion"}' | jq -r .proyecto.id)
# curl -s -X POST http://127.0.0.1:8080/api/taller/proyectos/$PID/cola \
#   -H 'Content-Type: application/json' \
#   -d '{"title":"Filas 1-100","blurb":"limpiar CSV","payload":"{\"from\":1,\"to\":100}"}'

# En B: sync + ver cola + tomar + entregar
curl -s -X POST http://127.0.0.1:8081/api/taller/sync | jq .
# ORIGIN=$(curl -s http://127.0.0.1:8080/api/node | jq -r .node_id)
# curl -s "http://127.0.0.1:8081/api/taller/remoto/cola?origin_node_id=$ORIGIN&proyecto_id=$PID" | jq .
# curl -s -X POST http://127.0.0.1:8081/api/taller/remoto/cola/lease \
#   -H 'Content-Type: application/json' \
#   -d "{\"origin_node_id\":\"$ORIGIN\",\"proyecto_id\":\"$PID\"}" | jq .
# curl -s -X POST http://127.0.0.1:8081/api/taller/remoto/cola/complete \
#   -H 'Content-Type: application/json' \
#   -d "{\"origin_node_id\":\"$ORIGIN\",\"proyecto_id\":\"$PID\",\"job_id\":\"JOB\",\"result_notas\":\"ok\"}" | jq .

# UI: Taller → En esta red → ficha remota → sección Cola → Tomar job / Entregar
```

## Limitaciones

- Upload `.pucela` sin `box_public` del origen o sin poder Unseal local → rechazo (reseello obligatorio).
- Ambos nodos deben tener al otro en allowlist (A necesita el NodeID de B).
- Sin allowlist / NodeID desconocido → claim/lease/upload rechazado (403).
- mDNS solo sugiere URLs; la allowlist es la fuente fiable.
- Un mismo `id` en dos nodos son fichas distintas (clave `origin_node_id:id`).
- Tope **8 MiB** por artefacto; MIME fuera de allowlist → rechazo.
- Payload inline de job ≤ **4 KiB**; para más usá `payload_ref`.
- Máx **200** jobs por proyecto; leases recordados en peer ≤ 200.
- `.pucela` sellado a la box del peer queda espejado en A (`PutSealedRaw`);
  abrir el claro en A requiere re-sello a la box de A (fuera de este MVP).
- Sin sync wholesale de tableros, chat, casas ni dependencia VitaInk.
- Cola ≠ claim: son superficies paralelas (una tarea y un job pueden coexistir).
