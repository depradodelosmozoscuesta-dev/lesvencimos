# Splash audio preview — v20261001h (local, no push)

## Jorge’s direction (supersedes g)
1. **Timing:** End splash with Jorge’s melody (~6.86 s). No dead air to 9.7 s. Keep warm lighting at close (frame ~6.86 has LES VENCIMOS + glow).
2. **Voices:** Higher-quality neural TTS (edge-tts warm female Neural / Multilingual). Mild rate −5%, pitch −1 Hz, soft loudnorm. Not the soft-clipped −15% g set.
3. **Chorus:** Staggered greetings only (hola / hello / olá / bonjour / ciao / …) overlapping «pas, pas, pas». NO adiós. «Te queremos» (or multilingual love) near warm end.
4. Caption on the **RIGHT** — current phrase + brief stack.
5. Local preview only — **no push / no Pages**. Completo **j** scroll sacred; after Jorge OK notify Aspecto+Web for fusion.

## Timing map
```
video                 12.04 s (freeze later unused)
melody (Jorge)         6.86 s  ASAP with picture
0.00 s                 splash + melody
0.20 s                 CHORUS start (lang stack)     ← CHORUS_AT
+0.20 s each           next greeting (7 voices)     ← CHORUS_STEP
~1.40 s                last chorus hit
4.55 s                 «te queremos» / love         ← LOVE_AT
~6.55 s                love clip ends (overlaps fade)
6.86 s                 FINISH / fade → Estantería   ← FINISH_AT (= melody end)
```

## Voices (edge-tts Neural)
| Lang | Voice | Open | Close (love) |
|------|-------|------|----------------|
| es | es-MX-DaliaNeural | ¡Hola! | Te queremos |
| en | en-US-JennyNeural | Hello! | We love you |
| fr | fr-FR-DeniseNeural | Bonjour! | On t'aime |
| pt | pt-BR-FranciscaNeural | Olá! | A gente te quer |
| it | it-IT-IsabellaNeural | Ciao! | Ti vogliamo bene |
| de | de-DE-AmalaNeural | Hallo! | Wir haben dich lieb |
| ro | ro-RO-AlinaNeural | Bună! | Te iubim |
| ru | ru-RU-SvetlanaNeural | Привет! | Мы вас любим |
| ja | ja-JP-NanamiNeural | こんにちは | 大好き |
| ko | ko-KR-SunHiNeural | 안녕하세요! | 사랑해요 |

Clips: `brand/splash/voz/{hi,bye}-*.m4a` (bye filename = love content). Backup of g: `voz/_bak-g/`.

## Rotation (`localStorage lv-splash-voz-i`)
- Each visit: 7 staggered greetings starting at idx (choir).
- Love line: lang at (idx+3) % n (warm end, no goodbye).

## Preview
- `brand/splash/preview-audio-h.html`
- Live local: `estanteria.html` / `offline-estanteria/estanteria.html` (clear `sessionStorage lv-splash-v8`)
- Cache bust V=`20261001h`

## Coordination
- Completo **j** scroll stamp sacred — do not stomp.
- After Jorge OKs: notify Aspecto+Web for **k** fusion. NO Pages from this lane alone.
