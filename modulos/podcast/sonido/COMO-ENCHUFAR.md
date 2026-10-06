# Cómo enchufar LVPodcastAudio

Un solo archivo: `sonido/lv-podcast-audio.js`. Global `LVPodcastAudio`. No hay `LVSonido` ni `crearLimpieza`: el ruido es la puerta (`gateThresholdDb`).

`create` no toca `destination`. La mesa conecta ella la salida.

```html
<script src="sonido/lv-podcast-audio.js"></script>
<script>
const ctx = new AudioContext();
const studio = await LVPodcastAudio.create(ctx);

const mic = studio.addMic('locutor');   // síncrono; mic.input ya existe
const stream = await navigator.mediaDevices.getUserMedia({
  audio: LVPodcastAudio.micConstraints({ bleedGuard: false })
});
ctx.createMediaStreamSource(stream).connect(mic.input);
mic.setGainDb(-3);
mic.mute(false);
mic.solo(false);
mic.setParam('hpfHz', 90);

const melodia = studio.addBed('melodia');
const efectos = studio.addBed('efectos');
fuenteMusica.connect(melodia.input);
fuenteFx.connect(efectos.input);
melodia.setGainDb(-8);
melodia.setDuckDb(-28);   // solo esta cama
efectos.setDuckDb(null);  // usa el bedDuckDb de la escena

studio.setScene('entrevista');
studio.master.connect(ctx.destination);  // post-limitador (monitor). No lo hace create.
studio.meters(function (m) {
  // m.mics.locutor.inDb / outDb / gateOpen / deEssDb
  // m.beds.melodia.inDb / gainDb
  // m.masterDb, m.speechDb   silencio = -80, nunca NaN
});
</script>
```

## Estudio

| Qué | Firma | Notas |
| --- | --- | --- |
| Crear | `await LVPodcastAudio.create(audioContext)` | Espera al módulo. Equivale a `crear({ contexto, salida: false })`. |
| Micro | `studio.addMic(id)` | No es promesa. `input` es el AudioNode de entrada (worklet o ScriptProcessor). |
| Fader | `mic.setGainDb(db)` | dB, útil −18…+6, duro −90…+18. No es un `setParam`. |
| Mute / solo | `mic.mute(bool)`, `mic.solo(bool)` | Alias de `setMute` / `setSolo`. |
| Parámetros | `mic.setParam(nombre, valor)`, `mic.getParams()` | Mismos nombres. Unidades naturales, no 0..1 salvo donde se dice. |
| Cama | `studio.addBed(id)` | Varias. `input`, `setGainDb(db)`, `setDuckDb(db \| null)`. |
| Escena | `studio.setScene(id)` | Receta a los micros de ahora y a los siguientes. No toca el pan. Ajusta cross-duck y anti-bleed. |
| Anti-bleed | `studio.setBleedGuard(bool)` | Con la guarda, el umbral de puerta efectivo es el de la receta + 8 dB. `getParams().gateThresholdDb` sigue siendo el de la receta. |
| Salida | `studio.master.connect(nodo)` | Solo el nodo de después del limitador. `master.output` es ese nodo. `master.gain` es el fader maestro. |
| Medidores | `studio.meters(cb)` | Unos 20 Hz. Devuelve una función para dejar de escuchar. |
| Escena actual | `studio.scene` | |
| Motor | `studio.usingWorklet` | `true` AudioWorklet, `false` ScriptProcessor (típico en `file://`). |
| Cerrar | `studio.destroy()` | Para el grafo. No cierra el AudioContext. |
| Micro constraints | `LVPodcastAudio.micConstraints({ bleedGuard })` | `echoCancellation` solo si `bleedGuard`. `noiseSuppression: false`, `autoGainControl: false`, `channelCount: 1`. |
| Catálogo | `LVPodcastAudio.scenes` | `[{ id, name, blurb }]`. |

## Cadena

Micro: entrada → pasaaltos, puerta, EQ, de-esser, rider, compresor → fader (`setGainDb`) → mute/solo → panorama → cross-duck entre micros → bus de voz.

Cama: `input` → ganancia del usuario → recorte de escena → ganancia de duck → el mismo punto que el bus de voz, antes del limitador.

La llave del duck de las camas es un medidor solo en el bus de voz. Por encima de −40 dBFS la cama baja su duck (ataque ~20 ms, suelta ~350 ms). `setDuckDb(null)` usa el `bedDuckDb` de la escena. Un número de 0 a −40 fija solo esa cama (melodía a −28, efectos con otro valor).

`audiolibro` pone el recorte de todas las camas a −80 dB. El resto de escenas, recorte 0 dB.

El panorama (`pan`, −1 izquierda … +1 derecha) va después del fader y antes del cross-duck. `StereoPannerNode` si el modo es worklet; si no, dos ganancias en igual potencia. `setScene` no lo cambia.

## Escenas

`setScene` acepta estos id:

- `radio` — Locución ya comprimida, con presencia, y la música 14 dB más baja cuando hay voz.
- `directo` — Casi la sala: poca compresión, anti-bleed encendido y un duck leve entre micros.
- `futbol` — Grito y ambiente: puerta rápida, compresión fuerte, duck entre micros y la cama muy abajo. Anti-bleed activo.
- `entrevista` — Dos voces: duck suave entre micros y la cama baja 12 dB.
- `intima` — Cerca del micro, con cuerpo y poca puerta; la música casi se va al hablar.
- `mesa` — Varias voces juntas: puerta más firme y duck entre canales.
- `humor` — La puerta deja pasar la risa; la compresión no aplasta el remate.
- `emotivo` — Dinámica ancha, graves y aire; la cama cede mucho.
- `audiolibro` — Voz sola. Las camas quedan a −80 dB.
- `educativo` — Presencia alta para que se entienda cada palabra.
- `historia` — Relato cálido, compresión moderada y cama discreta.
- `seco` — Cadena plana: sin EQ, sin puerta, sin rider ni compresor.
- `improvisacion` — Puerta muy abierta para no cortar la impro, compresión mínima y la cama solo 8 dB abajo.

`directo` y `futbol` encienden la guarda anti-bleed. Las demás la apagan. Se puede volver a cambiar con `setBleedGuard`.

## setParam

`getParams()` devuelve exactamente estos nombres. El fader no está aquí.

| Nombre | Unidad | Rango útil |
| --- | --- | --- |
| `gateThresholdDb` | dB | −60…−30 |
| `gateRangeDb` | dB (negativo: atenuación al cerrar) | −60…−18 |
| `gateAttackMs` | ms | 1…20 |
| `gateHoldMs` | ms | 30…180 |
| `gateReleaseMs` | ms | 40…300 |
| `gateHysteresisDb` | dB | 2…8 |
| `hpfHz` | Hz | 60…140 |
| `lowHz` | Hz | 90…250 |
| `lowGainDb` | dB | −4…+4 |
| `presenceHz` | Hz | 2000…5000 |
| `presenceGainDb` | dB | 0…+5 |
| `presenceQ` | Q | 0,7…1,6 |
| `airHz` | Hz | 8000…12000 |
| `airGainDb` | dB | 0…+4 |
| `deEssFreqHz` | Hz | 5000…9000 |
| `deEssThresholdDb` | dB | −32…−14 |
| `deEssMaxDb` | dB de corte, positivo | 3…12 |
| `deEssAttackMs` | ms | 0,5…5 |
| `deEssReleaseMs` | ms | 25…90 |
| `riderEnabled` | 0 o 1 | 0 o 1 |
| `riderTargetDb` | dB RMS | −24…−14 |
| `riderMaxBoostDb` | dB | 3…10 |
| `riderMaxCutDb` | dB | 3…12 |
| `compThresholdDb` | dB | −28…−12 |
| `compRatio` | :1 | 1,6…4 |
| `compKneeDb` | dB | 3…12 |
| `compAttackMs` | ms | 5…30 |
| `compReleaseMs` | ms | 60…250 |
| `compMakeupDb` | dB | 0…8 |
| `compMix` | 0..1 (1 = comprimido) | 0,6…1 |
| `pan` | −1…+1 | −1…+1 |

Un nombre que no esté en la lista lanza error. Los valores fuera del duro se recortan.
