# Splash audio preview — v20261001f (local, no push)

## Jorge’s direction
- REMOVE succión / portazo / relámpago as default (felt wrong).
- SHORTEN ending (cut ~2.3 s dead freeze before Estantería).
- Warmer spoken greetings + **right-side written caption**, rotating languages.
- Tone: not bare hello/bye — warm lines («Hola», «Bienvenido» spirit → «Te queremos» / equivalents).

## Timing map (measured)
```
video duration     12.04 s  (freeze ~10.5–12.0 — jpeg Δ≈0)
melody (trimmed)    6.86 s  ASAP with picture
0.00 s              splash + Jorge melody
0.28 s              HELLO voice + caption (lang A)
~6.86 s             melody ends
8.55 s              BYE voice + caption (lang B)   ← was CIERRE_AT 11.15 succión
9.70 s              FINISH / fade → Estantería     ← was ~12.0 video end
```

## Rotation (`localStorage lv-splash-voz-i`)
- Round-robin index each visit.
- Every 3rd visit: **one** language for hello+bye.
- Otherwise: **two** languages (hello = idx, bye = idx+1+(idx%5)).
- Languages: es, ru, ko, ro, fr, en, it, pt, de, ja.

## Sample phrases (spoken + caption)
| Lang | Open (hi) | Close (bye) |
|------|-----------|-------------|
| Español | ¡Hola! Te queremos | ¡Adiós! Te queremos |
| Русский | Привет! Мы вас любим | До свидания! |
| 한국어 | 안녕하세요! 사랑해요 | 안녕히 가세요! |
| Română | Bună! Te iubim | La revedere! |
| Français | Bonjour! On t'aime | Au revoir! |
| English | Hello! We love you | Goodbye! |
| Italiano | Ciao! Ti vogliamo bene | Arrivederci! |
| Português | Olá! A gente te quer | Adeus! |
| Deutsch | Hallo! Wir haben dich lieb | Tschüss! |
| 日本語 | こんにちは / 大好き | またね! |

Clips: `brand/splash/voz/{hi,bye}-*.m4a` (~230 KB total). Offline/file:// safe (no SpeechSynthesis).

## Kept
- Clay `entrada.mp4` + Jorge `entrada-sonido.m4a` (silence-trimmed, ASAP).
- Unused on disk: `cierre-succion.m4a`, `cierre-portazo.m4a`, `cierre-relampago.m4a` (not wired).

## Preview
- `brand/splash/preview-audio-f.html` — listen clips + simulate timing
- Live: open `estanteria.html` (clear `sessionStorage lv-splash-v8` to re-show splash; bump `lv-splash-voz-i` to audition pairs)
