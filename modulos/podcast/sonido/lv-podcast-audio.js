/*
 * LVPodcastAudio — cadena de micro del estudio Les vencimos.
 * Un archivo, sin CDN, usable en file://. No existe LVSonido ni crearLimpieza:
 * el ruido se gobierna con la puerta (gateThresholdDb).
 *
 * Orden de cada micro, de la cápsula a la suma:
 *   entrada mono
 *   → procesador (pasaaltos, puerta, EQ, de-esser, rider, compresor con 2 ms de antelación)
 *     AudioWorklet si el navegador deja cargar el módulo; si no (típico en file://),
 *     el mismo código corre en ScriptProcessor de 256 muestras.
 *   → fader   mic.setGainDb(dB)     ← no es un setParam
 *   → mute / solo
 *   → panorama (StereoPannerNode, o ganancias en igual potencia si no existe)
 *   → cross-duck (el que habla más bajo cede; no es un setParam)
 *   → bus → fader maestro → limitador de techo → (grabación) y monitor
 *
 * setParam / getParams comparten exactamente LVPodcastAudio.PARAMETROS.
 */
(function (global) {
  'use strict';

  var FICHA = [
    { nombre: 'gateThresholdDb', unidad: 'dB', util: [-60, -30], duro: [-90, 0], defecto: -42,
      nota: 'Nivel por encima del cual la puerta se abre. Más alto, más silencio entre frases.' },
    { nombre: 'gateRangeDb', unidad: 'dB', util: [-60, -18], duro: [-90, 0], defecto: -45,
      nota: 'Atenuación con la puerta cerrada. Siempre negativo: -45 cierra 45 dB. 0 no atenúa.' },
    { nombre: 'gateAttackMs', unidad: 'ms', util: [1, 20], duro: [0.1, 200], defecto: 4,
      nota: 'Tiempo en abrirse la puerta al empezar la voz.' },
    { nombre: 'gateHoldMs', unidad: 'ms', util: [30, 180], duro: [0, 1000], defecto: 90,
      nota: 'Tiempo que sigue abierta tras caer la voz, antes de soltar.' },
    { nombre: 'gateReleaseMs', unidad: 'ms', util: [40, 300], duro: [5, 2000], defecto: 140,
      nota: 'Tiempo en cerrarse del todo después de la espera.' },
    { nombre: 'gateHysteresisDb', unidad: 'dB', util: [2, 8], duro: [0, 18], defecto: 4,
      nota: 'Margen para no tabletear: se abre en el umbral y se cierra umbral menos este valor.' },

    { nombre: 'hpfHz', unidad: 'Hz', util: [60, 140], duro: [20, 400], defecto: 85,
      nota: 'Pasaaltos de 2.º orden (rumble, mesa, pops). 20 Hz queda prácticamente fuera.' },
    { nombre: 'lowHz', unidad: 'Hz', util: [90, 250], duro: [40, 500], defecto: 160,
      nota: 'Frecuencia de la estantería de graves.' },
    { nombre: 'lowGainDb', unidad: 'dB', util: [-4, 4], duro: [-18, 18], defecto: 0,
      nota: 'Ganancia de graves. Negativo adelgaza, positivo da cuerpo.' },
    { nombre: 'presenceHz', unidad: 'Hz', util: [2000, 5000], duro: [800, 8000], defecto: 3200,
      nota: 'Centro de la campana de presencia (inteligibilidad).' },
    { nombre: 'presenceGainDb', unidad: 'dB', util: [0, 5], duro: [-18, 18], defecto: 2,
      nota: 'Realce o corte de presencia.' },
    { nombre: 'presenceQ', unidad: 'Q', util: [0.7, 1.6], duro: [0.3, 8], defecto: 1,
      nota: 'Ancho de la campana. Q alto, campana estrecha.' },
    { nombre: 'airHz', unidad: 'Hz', util: [8000, 12000], duro: [3000, 16000], defecto: 10000,
      nota: 'Frecuencia de la estantería de aire.' },
    { nombre: 'airGainDb', unidad: 'dB', util: [0, 4], duro: [-18, 18], defecto: 1.5,
      nota: 'Aire / brillo. Mucho aire sube las eses: el de-esser va detrás.' },

    { nombre: 'deEssFreqHz', unidad: 'Hz', util: [5000, 9000], duro: [2000, 12000], defecto: 6500,
      nota: 'Centro de la ese. El corte es una campana dinámica (Q interno ≈ 1.4), no un mute de toda la banda.' },
    { nombre: 'deEssThresholdDb', unidad: 'dB', util: [-32, -14], duro: [-60, 0], defecto: -22,
      nota: 'Nivel de la banda de la ese a partir del cual empieza a cortar.' },
    { nombre: 'deEssMaxDb', unidad: 'dB', util: [3, 12], duro: [0, 24], defecto: 7,
      nota: 'Corte máximo, en positivo. 0 deja el de-esser en bypass.' },
    { nombre: 'deEssAttackMs', unidad: 'ms', util: [0.5, 5], duro: [0.1, 50], defecto: 1,
      nota: 'Rapidez del corte de la ese.' },
    { nombre: 'deEssReleaseMs', unidad: 'ms', util: [25, 90], duro: [5, 300], defecto: 45,
      nota: 'Vuelta del de-esser tras la ese.' },

    { nombre: 'riderEnabled', unidad: '0 o 1', util: [0, 1], duro: [0, 1], defecto: 1,
      nota: '1 activa el rider de nivel. 0 lo deja en 0 dB. También acepta true/false. Se guarda 0 o 1.' },
    { nombre: 'riderTargetDb', unidad: 'dB RMS', util: [-24, -14], duro: [-48, -6], defecto: -18,
      nota: 'RMS al que el rider intenta llevar la voz cuando la puerta está abierta.' },
    { nombre: 'riderMaxBoostDb', unidad: 'dB', util: [3, 10], duro: [0, 18], defecto: 6,
      nota: 'Subida máxima del rider, en positivo.' },
    { nombre: 'riderMaxCutDb', unidad: 'dB', util: [3, 12], duro: [0, 24], defecto: 8,
      nota: 'Bajada máxima del rider, en positivo.' },

    { nombre: 'compThresholdDb', unidad: 'dB', util: [-28, -12], duro: [-60, 0], defecto: -20,
      nota: 'Umbral del compresor de voz.' },
    { nombre: 'compRatio', unidad: ':1', util: [1.6, 4], duro: [1, 20], defecto: 2.5,
      nota: 'Relación. 1 no comprime. 2.5 significa 2.5:1.' },
    { nombre: 'compKneeDb', unidad: 'dB', util: [3, 12], duro: [0, 30], defecto: 6,
      nota: 'Rodilla. 0 es rodilla dura.' },
    { nombre: 'compAttackMs', unidad: 'ms', util: [5, 30], duro: [0.2, 200], defecto: 12,
      nota: 'Ataque del compresor. La detección va 2 ms por delante del audio.' },
    { nombre: 'compReleaseMs', unidad: 'ms', util: [60, 250], duro: [10, 2000], defecto: 130,
      nota: 'Suelta del compresor.' },
    { nombre: 'compMakeupDb', unidad: 'dB', util: [0, 8], duro: [-12, 24], defecto: 2,
      nota: 'Ganancia de compensación solo en la señal ya comprimida.' },
    { nombre: 'compMix', unidad: '0..1', util: [0.6, 1], duro: [0, 1], defecto: 1,
      nota: 'Mezcla paralela. 1 = solo comprimido, 0 = seco (sigue habiendo 2 ms de antelación).' },

    { nombre: 'pan', unidad: '-1..+1', util: [-1, 1], duro: [-1, 1], defecto: 0,
      nota: 'Panorama. -1 izquierda, 0 centro, +1 derecha. Va después del fader y antes del cross-duck.' }
  ];

  var PARAMETROS = FICHA.map(function (f) { return f.nombre; });
  var POR_NOMBRE = {};
  FICHA.forEach(function (f) { POR_NOMBRE[f.nombre] = f; });

  function mezclar(base, encima) {
    var o = {}, k;
    for (k in base) o[k] = base[k];
    for (k in encima) o[k] = encima[k];
    return o;
  }

  var RADIO = {
    hpfHz: 100, lowHz: 180, lowGainDb: -1.5, presenceHz: 3200, presenceGainDb: 4, presenceQ: 1,
    airHz: 10000, airGainDb: 2,
    gateThresholdDb: -40, gateRangeDb: -80, gateAttackMs: 2, gateHoldMs: 80, gateReleaseMs: 120, gateHysteresisDb: 4,
    deEssFreqHz: 6500, deEssThresholdDb: -28, deEssMaxDb: 6, deEssAttackMs: 2, deEssReleaseMs: 60,
    riderEnabled: 1, riderTargetDb: -16, riderMaxBoostDb: 6, riderMaxCutDb: 6,
    compThresholdDb: -20, compRatio: 4, compKneeDb: 6, compAttackMs: 8, compReleaseMs: 90, compMakeupDb: 5, compMix: 0.85
  };
  var INTIMA = mezclar(RADIO, {
    hpfHz: 70, lowHz: 200, lowGainDb: 2.5, presenceHz: 2500, presenceGainDb: 1.5, presenceQ: 0.8,
    airHz: 12000, airGainDb: 2,
    gateThresholdDb: -48, gateRangeDb: -14, gateAttackMs: 5, gateHoldMs: 160, gateReleaseMs: 260, gateHysteresisDb: 3,
    deEssMaxDb: 3,
    riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 4, riderMaxCutDb: 4,
    compThresholdDb: -16, compRatio: 2, compKneeDb: 10, compAttackMs: 20, compReleaseMs: 180, compMakeupDb: 2, compMix: 0.7
  });

  function escena(meta, params) {
    return {
      id: meta.id, name: meta.name, blurb: meta.blurb,
      crossDuck: meta.crossDuck, bleed: !!meta.bleed, bedDuck: meta.bedDuck, bedTrim: meta.bedTrim,
      params: params
    };
  }

  var LISTA_ESCENAS = [
    escena({ id: "radio", name: "Radio", blurb: "Locución ya comprimida, con presencia y la música 14 dB más baja cuando hay voz.", crossDuck: 0, bleed: false, bedDuck: -14, bedTrim: 0 }, RADIO),
    escena({ id: "directo", name: "Directo", blurb: "Casi la sala: poca compresión, anti-bleed encendido y un duck leve entre micros.", crossDuck: -2, bleed: true, bedDuck: -10, bedTrim: 0 }, mezclar(RADIO, {
      hpfHz: 80, lowGainDb: 0, presenceHz: 2800, presenceGainDb: 1.5, presenceQ: 0.9, airGainDb: 0.5,
      gateThresholdDb: -46, gateRangeDb: -24, gateAttackMs: 8, gateHoldMs: 140, gateReleaseMs: 220, gateHysteresisDb: 3,
      deEssMaxDb: 3,
      riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 8, riderMaxCutDb: 6,
      compThresholdDb: -18, compRatio: 1.8, compKneeDb: 10, compAttackMs: 25, compReleaseMs: 200, compMakeupDb: 1, compMix: 0.6
    })),
    escena({ id: "futbol", name: "Fútbol", blurb: "Grito y ambiente: puerta rápida, compresión fuerte, duck entre micros y la cama muy abajo. Anti-bleed activo.", crossDuck: -8, bleed: true, bedDuck: -16, bedTrim: 0 }, mezclar(RADIO, {
      hpfHz: 100, lowHz: 220, lowGainDb: -2, presenceHz: 3500, presenceGainDb: 5, presenceQ: 1.2, airGainDb: 1.5,
      gateThresholdDb: -38, gateRangeDb: -50, gateAttackMs: 2, gateHoldMs: 50, gateReleaseMs: 80, gateHysteresisDb: 4,
      deEssFreqHz: 6800, deEssThresholdDb: -26, deEssMaxDb: 6, deEssAttackMs: 1, deEssReleaseMs: 50,
      riderEnabled: 1, riderTargetDb: -14, riderMaxBoostDb: 6, riderMaxCutDb: 8,
      compThresholdDb: -16, compRatio: 4.5, compKneeDb: 3, compAttackMs: 3, compReleaseMs: 60, compMakeupDb: 4, compMix: 1
    })),
    escena({ id: "entrevista", name: "Entrevista", blurb: "Dos voces en conversación: duck suave entre micros y la cama baja 12 dB.", crossDuck: -4, bleed: false, bedDuck: -12, bedTrim: 0 }, mezclar(RADIO, {
      hpfHz: 85, lowGainDb: 0, presenceHz: 3000, presenceGainDb: 2.5, presenceQ: 1, airGainDb: 1.5,
      gateThresholdDb: -42, gateRangeDb: -40, gateAttackMs: 4, gateHoldMs: 100, gateReleaseMs: 150, gateHysteresisDb: 4,
      deEssThresholdDb: -24, deEssMaxDb: 5,
      riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 6, riderMaxCutDb: 6,
      compThresholdDb: -18, compRatio: 2.5, compKneeDb: 8, compAttackMs: 12, compReleaseMs: 140, compMakeupDb: 2, compMix: 0.8
    })),
    escena({ id: "intima", name: "Íntima", blurb: "Cerca del micro, con cuerpo y poca puerta; la música casi se va cuando hablas.", crossDuck: -3, bleed: false, bedDuck: -18, bedTrim: 0 }, INTIMA),
    escena({ id: "mesa", name: "Mesa", blurb: "Varias voces juntas: puerta más firme, duck entre canales y cama contenida.", crossDuck: -6, bleed: false, bedDuck: -12, bedTrim: 0 }, mezclar(RADIO, {
      hpfHz: 90, lowHz: 250, lowGainDb: -2, presenceHz: 3000, presenceGainDb: 3, presenceQ: 1.1, airGainDb: 1,
      gateThresholdDb: -38, gateRangeDb: -60, gateAttackMs: 3, gateHoldMs: 60, gateReleaseMs: 100, gateHysteresisDb: 4,
      deEssMaxDb: 5,
      riderEnabled: 1, riderTargetDb: -16, riderMaxBoostDb: 6, riderMaxCutDb: 6,
      compThresholdDb: -18, compRatio: 3, compKneeDb: 6, compAttackMs: 10, compReleaseMs: 120, compMakeupDb: 4, compMix: 0.9
    })),
    escena({ id: "humor", name: "Humor", blurb: "La puerta deja pasar la risa; la compresión no aplasta el remate.", crossDuck: -2, bleed: false, bedDuck: -10, bedTrim: 0 }, mezclar(INTIMA, {
      hpfHz: 75, lowGainDb: 1, presenceHz: 2800, presenceGainDb: 1.5, airGainDb: 1.5,
      gateThresholdDb: -55, gateRangeDb: -12, gateAttackMs: 10, gateHoldMs: 280, gateReleaseMs: 400, gateHysteresisDb: 3,
      deEssMaxDb: 2,
      riderEnabled: 1, riderTargetDb: -16, riderMaxBoostDb: 4, riderMaxCutDb: 4,
      compThresholdDb: -22, compRatio: 1.8, compKneeDb: 12, compAttackMs: 30, compReleaseMs: 250, compMakeupDb: 1, compMix: 0.55
    })),
    escena({ id: "emotivo", name: "Emotivo", blurb: "Dinámica ancha, graves y aire; la cama cede mucho a la voz.", crossDuck: -2, bleed: false, bedDuck: -20, bedTrim: 0 }, mezclar(INTIMA, {
      hpfHz: 65, lowHz: 140, lowGainDb: 3, presenceHz: 2400, presenceGainDb: 1, presenceQ: 0.7, airHz: 11000, airGainDb: 2.5,
      gateThresholdDb: -46, gateRangeDb: -20, gateAttackMs: 12, gateHoldMs: 180, gateReleaseMs: 300,
      deEssMaxDb: 4,
      riderEnabled: 1, riderTargetDb: -20, riderMaxBoostDb: 4, riderMaxCutDb: 4,
      compThresholdDb: -20, compRatio: 1.8, compKneeDb: 12, compAttackMs: 28, compReleaseMs: 240, compMakeupDb: 2, compMix: 0.65
    })),
    escena({ id: "audiolibro", name: "Audiolibro", blurb: "Voz sola y pareja. Las camas quedan a -80 dB: no hay música debajo.", crossDuck: 0, bleed: false, bedDuck: 0, bedTrim: -80 }, mezclar(RADIO, {
      hpfHz: 80, lowGainDb: 0.5, presenceHz: 3000, presenceGainDb: 2.5, presenceQ: 0.9, airGainDb: 0.5,
      gateThresholdDb: -40, gateRangeDb: -70, gateAttackMs: 3, gateHoldMs: 70, gateReleaseMs: 110,
      deEssMaxDb: 5,
      riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 8, riderMaxCutDb: 8,
      compThresholdDb: -18, compRatio: 3, compKneeDb: 6, compAttackMs: 10, compReleaseMs: 100, compMakeupDb: 3, compMix: 0.95
    })),
    escena({ id: "educativo", name: "Educativo", blurb: "Presencia alta para que se entienda cada palabra, con la cama por debajo.", crossDuck: -3, bleed: false, bedDuck: -14, bedTrim: 0 }, mezclar(RADIO, {
      hpfHz: 95, lowGainDb: -1, presenceHz: 3400, presenceGainDb: 4.5, presenceQ: 1.2, airGainDb: 1,
      gateThresholdDb: -40, gateRangeDb: -55, gateAttackMs: 3, gateHoldMs: 80, gateReleaseMs: 120,
      deEssThresholdDb: -24, deEssMaxDb: 5,
      riderEnabled: 1, riderTargetDb: -16, riderMaxBoostDb: 6, riderMaxCutDb: 6,
      compThresholdDb: -18, compRatio: 3, compKneeDb: 5, compAttackMs: 8, compReleaseMs: 100, compMakeupDb: 3, compMix: 0.9
    })),
    escena({ id: "historia", name: "Historia", blurb: "Relato cálido, compresión moderada y una cama discreta.", crossDuck: 0, bleed: false, bedDuck: -8, bedTrim: 0 }, mezclar(INTIMA, {
      hpfHz: 70, lowHz: 150, lowGainDb: 2.5, presenceHz: 2600, presenceGainDb: 2, presenceQ: 0.8, airHz: 9000, airGainDb: 0.5,
      gateThresholdDb: -44, gateRangeDb: -35, gateAttackMs: 6, gateHoldMs: 120, gateReleaseMs: 180,
      deEssMaxDb: 4,
      riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 5, riderMaxCutDb: 5,
      compThresholdDb: -20, compRatio: 2.2, compKneeDb: 8, compAttackMs: 18, compReleaseMs: 160, compMakeupDb: 2, compMix: 0.75
    })),
    escena({ id: "seco", name: "Seco", blurb: "Cadena plana: sin EQ, sin puerta, sin rider ni compresor, y la cama no se agacha.", crossDuck: 0, bleed: false, bedDuck: 0, bedTrim: 0 }, {
      hpfHz: 20, lowHz: 160, lowGainDb: 0, presenceHz: 3200, presenceGainDb: 0, presenceQ: 1, airHz: 10000, airGainDb: 0,
      gateThresholdDb: -90, gateRangeDb: 0, gateAttackMs: 1, gateHoldMs: 0, gateReleaseMs: 20, gateHysteresisDb: 0,
      deEssFreqHz: 6500, deEssThresholdDb: 0, deEssMaxDb: 0, deEssAttackMs: 1, deEssReleaseMs: 40,
      riderEnabled: 0, riderTargetDb: -18, riderMaxBoostDb: 0, riderMaxCutDb: 0,
      compThresholdDb: 0, compRatio: 1, compKneeDb: 0, compAttackMs: 5, compReleaseMs: 50, compMakeupDb: 0, compMix: 0
    }),
    escena({ id: "improvisacion", name: "Improvisación", blurb: "Puerta muy abierta para no cortar la impro, compresión mínima y la cama solo 8 dB abajo.", crossDuck: -2, bleed: false, bedDuck: -8, bedTrim: 0 }, mezclar(INTIMA, {
      hpfHz: 70, lowGainDb: 1, presenceHz: 2800, presenceGainDb: 1.5, presenceQ: 0.8, airGainDb: 1.5,
      gateThresholdDb: -56, gateRangeDb: -10, gateAttackMs: 12, gateHoldMs: 300, gateReleaseMs: 450, gateHysteresisDb: 3,
      deEssMaxDb: 2,
      riderEnabled: 1, riderTargetDb: -18, riderMaxBoostDb: 3, riderMaxCutDb: 3,
      compThresholdDb: -24, compRatio: 1.5, compKneeDb: 12, compAttackMs: 35, compReleaseMs: 280, compMakeupDb: 0.5, compMix: 0.4
    }))
  ];
  var ESCENAS = {};
  LISTA_ESCENAS.forEach(function (sc) { ESCENAS[sc.id] = sc; });
  ESCENAS.neutro = ESCENAS.seco;

  var FUENTE = [
    "class CanalPodcast extends AudioWorkletProcessor {",
    "  static get parameterDescriptors() {",
    "    return [",
    "      { name: 'gateThresholdDb', defaultValue: -42, minValue: -90, maxValue: 0, automationRate: 'k-rate' },",
    "      { name: 'gateRangeDb', defaultValue: -45, minValue: -90, maxValue: 0, automationRate: 'k-rate' },",
    "      { name: 'gateAttackMs', defaultValue: 4, minValue: 0.1, maxValue: 200, automationRate: 'k-rate' },",
    "      { name: 'gateHoldMs', defaultValue: 90, minValue: 0, maxValue: 1000, automationRate: 'k-rate' },",
    "      { name: 'gateReleaseMs', defaultValue: 140, minValue: 5, maxValue: 2000, automationRate: 'k-rate' },",
    "      { name: 'gateHysteresisDb', defaultValue: 4, minValue: 0, maxValue: 18, automationRate: 'k-rate' },",
    "      { name: 'hpfHz', defaultValue: 85, minValue: 20, maxValue: 400, automationRate: 'k-rate' },",
    "      { name: 'lowHz', defaultValue: 160, minValue: 40, maxValue: 500, automationRate: 'k-rate' },",
    "      { name: 'lowGainDb', defaultValue: 0, minValue: -18, maxValue: 18, automationRate: 'k-rate' },",
    "      { name: 'presenceHz', defaultValue: 3200, minValue: 800, maxValue: 8000, automationRate: 'k-rate' },",
    "      { name: 'presenceGainDb', defaultValue: 2, minValue: -18, maxValue: 18, automationRate: 'k-rate' },",
    "      { name: 'presenceQ', defaultValue: 1, minValue: 0.3, maxValue: 8, automationRate: 'k-rate' },",
    "      { name: 'airHz', defaultValue: 10000, minValue: 3000, maxValue: 16000, automationRate: 'k-rate' },",
    "      { name: 'airGainDb', defaultValue: 1.5, minValue: -18, maxValue: 18, automationRate: 'k-rate' },",
    "      { name: 'deEssFreqHz', defaultValue: 6500, minValue: 2000, maxValue: 12000, automationRate: 'k-rate' },",
    "      { name: 'deEssThresholdDb', defaultValue: -22, minValue: -60, maxValue: 0, automationRate: 'k-rate' },",
    "      { name: 'deEssMaxDb', defaultValue: 7, minValue: 0, maxValue: 24, automationRate: 'k-rate' },",
    "      { name: 'deEssAttackMs', defaultValue: 1, minValue: 0.1, maxValue: 50, automationRate: 'k-rate' },",
    "      { name: 'deEssReleaseMs', defaultValue: 45, minValue: 5, maxValue: 300, automationRate: 'k-rate' },",
    "      { name: 'riderEnabled', defaultValue: 1, minValue: 0, maxValue: 1, automationRate: 'k-rate' },",
    "      { name: 'riderTargetDb', defaultValue: -18, minValue: -48, maxValue: -6, automationRate: 'k-rate' },",
    "      { name: 'riderMaxBoostDb', defaultValue: 6, minValue: 0, maxValue: 18, automationRate: 'k-rate' },",
    "      { name: 'riderMaxCutDb', defaultValue: 8, minValue: 0, maxValue: 24, automationRate: 'k-rate' },",
    "      { name: 'compThresholdDb', defaultValue: -20, minValue: -60, maxValue: 0, automationRate: 'k-rate' },",
    "      { name: 'compRatio', defaultValue: 2.5, minValue: 1, maxValue: 20, automationRate: 'k-rate' },",
    "      { name: 'compKneeDb', defaultValue: 6, minValue: 0, maxValue: 30, automationRate: 'k-rate' },",
    "      { name: 'compAttackMs', defaultValue: 12, minValue: 0.2, maxValue: 200, automationRate: 'k-rate' },",
    "      { name: 'compReleaseMs', defaultValue: 130, minValue: 10, maxValue: 2000, automationRate: 'k-rate' },",
    "      { name: 'compMakeupDb', defaultValue: 2, minValue: -12, maxValue: 24, automationRate: 'k-rate' },",
    "      { name: 'compMix', defaultValue: 1, minValue: 0, maxValue: 1, automationRate: 'k-rate' }",
    "    ];",
    "  }",
    "  constructor() {",
    "    super();",
    "    this.hpf = biq(); this.low = biq(); this.pres = biq(); this.air = biq();",
    "    this.bp = biq(); this.de = biq();",
    "    this.gOpen = 0; this.hold = 0; this.env = 0; this.rms = 1e-8;",
    "    this.rider = 0; this.det = 0; this.gr = 0; this.deGr = 0; this.band = 0;",
    "    this.dly = new Float32Array(512); this.w = 0;",
    "    this.la = Math.max(1, Math.min(511, Math.round(0.002 * sampleRate)));",
    "    this.bloques = 0;",
    "    this.sello = '';",
    "    this.deSello = '';",
    "    this.deDb = 0;",
    "  }",
    "  process(inputs, outputs, parameters) {",
    "    var out = outputs[0] && outputs[0][0];",
    "    if (!out) return true;",
    "    var n = out.length;",
    "    var inn = inputs[0];",
    "    var in0 = inn && inn[0];",
    "    var in1 = inn && inn[1];",
    "    var P = function (nombre) { return parameters[nombre][0]; };",
    "    var sr = sampleRate;",
    "    var hpfHz = P('hpfHz');",
    "    var lowHz = P('lowHz'), lowG = P('lowGainDb');",
    "    var prHz = P('presenceHz'), prG = P('presenceGainDb'), prQ = P('presenceQ');",
    "    var airHz = P('airHz'), airG = P('airGainDb');",
    "    var sello = hpfHz + '|' + lowHz + '|' + lowG + '|' + prHz + '|' + prG + '|' + prQ + '|' + airHz + '|' + airG;",
    "    if (sello !== this.sello) {",
    "      this.sello = sello;",
    "      if (hpfHz <= 22) fijarBypass(this.hpf); else disenar(this.hpf, 'hpf', sr, hpfHz, 0.7071, 0);",
    "      if (Math.abs(lowG) < 0.05) fijarBypass(this.low); else disenar(this.low, 'low', sr, lowHz, 1, lowG);",
    "      if (Math.abs(prG) < 0.05) fijarBypass(this.pres); else disenar(this.pres, 'peak', sr, prHz, prQ, prG);",
    "      if (Math.abs(airG) < 0.05) fijarBypass(this.air); else disenar(this.air, 'high', sr, airHz, 1, airG);",
    "    }",
    "    var deF = P('deEssFreqHz');",
    "    var deThr = P('deEssThresholdDb');",
    "    var deMax = P('deEssMaxDb');",
    "    var cDeA = coef(P('deEssAttackMs'), sr);",
    "    var cDeR = coef(P('deEssReleaseMs'), sr);",
    "    var marcaDe = deF.toFixed(1);",
    "    if (marcaDe !== this.deSello) { this.deSello = marcaDe; disenar(this.bp, 'bp', sr, deF, 2, 0); }",
    "    var thr = P('gateThresholdDb');",
    "    var range = P('gateRangeDb');",
    "    var hyst = P('gateHysteresisDb');",
    "    var cAbre = coef(P('gateAttackMs'), sr);",
    "    var cCierra = coef(P('gateReleaseMs'), sr);",
    "    var holdN = Math.max(0, Math.round(P('gateHoldMs') * 0.001 * sr));",
    "    var cEnvUp = coef(0.4, sr);",
    "    var cEnvDn = coef(12, sr);",
    "    var cRms = coef(150, sr);",
    "    var riderOn = P('riderEnabled') >= 0.5;",
    "    var riderT = P('riderTargetDb');",
    "    var riderUp = P('riderMaxBoostDb');",
    "    var riderDn = P('riderMaxCutDb');",
    "    var cRidA = coef(220, sr);",
    "    var cRidR = coef(320, sr);",
    "    var cRidOff = coef(120, sr);",
    "    var cThr = P('compThresholdDb');",
    "    var cRatio = P('compRatio');",
    "    var cKnee = P('compKneeDb');",
    "    var cAtk = coef(P('compAttackMs'), sr);",
    "    var cRel = coef(P('compReleaseMs'), sr);",
    "    var makeup = P('compMakeupDb');",
    "    var mix = P('compMix');",
    "    var cDetUp = coef(0.3, sr);",
    "    var cDetDn = coef(10, sr);",
    "    var cBandUp = coef(0.4, sr);",
    "    var cBandDn = coef(8, sr);",
    "    var peak = 0, suma = 0, i, x, y, ax, nivel, abrir, objetivo, c, err, deseado, seco, nivelC, exceso, grDes, gDb, wet, b;",
    "    for (i = 0; i < n; i++) {",
    "      if (!in0) x = 0;",
    "      else if (!in1) x = in0[i];",
    "      else x = 0.5 * (in0[i] + in1[i]);",
    "      x = tick(this.hpf, x);",
    "      ax = x < 0 ? -x : x;",
    "      c = ax > this.env ? cEnvUp : cEnvDn;",
    "      this.env = ax + (this.env - ax) * c;",
    "      nivel = linDb(this.env);",
    "      if (nivel >= thr) { this.hold = holdN; objetivo = 1; }",
    "      else if (nivel >= thr - hyst) { this.hold = holdN; objetivo = this.gOpen > 0.5 ? 1 : 0; }",
    "      else if (this.hold > 0) { this.hold--; objetivo = 1; }",
    "      else objetivo = 0;",
    "      c = objetivo > this.gOpen ? cAbre : cCierra;",
    "      this.gOpen = objetivo + (this.gOpen - objetivo) * c;",
    "      if (this.gOpen < 1e-5) this.gOpen = 0;",
    "      x *= dbLin(range * (1 - this.gOpen));",
    "      x = tick(this.low, x);",
    "      x = tick(this.pres, x);",
    "      x = tick(this.air, x);",
    "      b = tick(this.bp, x);",
    "      ax = b < 0 ? -b : b;",
    "      c = ax > this.band ? cBandUp : cBandDn;",
    "      this.band = ax + (this.band - ax) * c;",
    "      exceso = linDb(this.band) - deThr;",
    "      grDes = exceso > 0 ? exceso : 0;",
    "      if (grDes > deMax) grDes = deMax;",
    "      c = grDes > this.deGr ? cDeA : cDeR;",
    "      this.deGr = grDes + (this.deGr - grDes) * c;",
    "      if (deMax <= 0.05 || this.deGr < 0.05) {",
    "        if (this.deDb !== 0) { this.deDb = 0; fijarBypass(this.de); }",
    "      } else if (Math.abs(this.deGr - this.deDb) > 0.08) {",
    "        this.deDb = this.deGr;",
    "        disenar(this.de, 'peak', sr, deF, 1.4, -this.deGr);",
    "      }",
    "      x = tick(this.de, x);",
    "      this.rms = (x * x) + (this.rms - (x * x)) * cRms;",
    "      if (!riderOn) {",
    "        this.rider = 0 + (this.rider - 0) * cRidOff;",
    "      } else if (this.gOpen > 0.8 && this.rms > 1e-10) {",
    "        err = riderT - linDb(Math.sqrt(this.rms));",
    "        if (err > riderUp) err = riderUp;",
    "        if (err < -riderDn) err = -riderDn;",
    "        c = err > this.rider ? cRidA : cRidR;",
    "        this.rider = err + (this.rider - err) * c;",
    "      }",
    "      x *= dbLin(this.rider);",
    "      this.dly[this.w] = x;",
    "      var r = this.w - this.la; if (r < 0) r += 512;",
    "      seco = this.dly[r];",
    "      this.w++; if (this.w >= 512) this.w = 0;",
    "      ax = x < 0 ? -x : x;",
    "      c = ax > this.det ? cDetUp : cDetDn;",
    "      this.det = ax + (this.det - ax) * c;",
    "      nivelC = linDb(this.det);",
    "      grDes = reduccion(nivelC, cThr, cRatio, cKnee);",
    "      c = grDes > this.gr ? cAtk : cRel;",
    "      this.gr = grDes + (this.gr - grDes) * c;",
    "      gDb = -this.gr + makeup;",
    "      wet = seco * dbLin(gDb);",
    "      y = seco * (1 - mix) + wet * mix;",
    "      if (y > 4) y = 4; else if (y < -4) y = -4;",
    "      if (y !== y) y = 0;",
    "      out[i] = y;",
    "      ax = y < 0 ? -y : y;",
    "      if (ax > peak) peak = ax;",
    "      suma += y * y;",
    "    }",
    "    this.bloques++;",
    "    if ((this.bloques & 3) === 0) {",
    "      this.port.postMessage({",
    "        inDb: linDb(this.env),",
    "        outPeakDb: linDb(peak),",
    "        outRmsDb: 10 * Math.log10(suma / n + 1e-20),",
    "        puerta: this.gOpen,",
    "        puertaDb: range * (1 - this.gOpen),",
    "        deEssDb: this.deGr,",
    "        compDb: this.gr,",
    "        riderDb: this.rider",
    "      });",
    "    }",
    "    return true;",
    "  }",
    "}",
    "class GrabadorPodcast extends AudioWorkletProcessor {",
    "  constructor() {",
    "    super();",
    "    this.max = sampleRate * 60 * 10;",
    "    this.cap = 0; this.n = 0; this.L = null; this.R = null; this.lleno = false; this.parado = false;",
    "    var self = this;",
    "    this.port.onmessage = function (e) {",
    "      if (!e.data || e.data.cmd !== 'parar' || self.parado) return;",
    "      self.parado = true;",
    "      var l = new Float32Array(self.n);",
    "      var r = new Float32Array(self.n);",
    "      if (self.n) { l.set(self.L.subarray(0, self.n)); r.set(self.R.subarray(0, self.n)); }",
    "      self.L = null; self.R = null;",
    "      self.port.postMessage({ cmd: 'wav', l: l, r: r, lleno: self.lleno, sr: sampleRate }, [l.buffer, r.buffer]);",
    "    };",
    "  }",
    "  asegurar(necesita) {",
    "    if (this.cap >= necesita) return;",
    "    var cap = this.cap || Math.round(sampleRate);",
    "    while (cap < necesita) cap *= 2;",
    "    if (cap > this.max) cap = this.max;",
    "    var L = new Float32Array(cap), R = new Float32Array(cap);",
    "    if (this.L && this.n) { L.set(this.L.subarray(0, this.n)); R.set(this.R.subarray(0, this.n)); }",
    "    this.L = L; this.R = R; this.cap = cap;",
    "  }",
    "  process(inputs) {",
    "    if (this.parado || this.lleno) return true;",
    "    var a = inputs[0];",
    "    if (!a || !a[0]) return true;",
    "    var l = a[0], r = a[1] || a[0], i, queda;",
    "    if (this.n + l.length > this.max) { this.lleno = true; queda = this.max - this.n; if (queda <= 0) return true; l = l.subarray(0, queda); r = r.subarray(0, queda); }",
    "    this.asegurar(this.n + l.length);",
    "    for (i = 0; i < l.length; i++) { this.L[this.n + i] = l[i]; this.R[this.n + i] = r[i]; }",
    "    this.n += l.length;",
    "    return true;",
    "  }",
    "}",
    "function biq() { return { b0: 1, b1: 0, b2: 0, a1: 0, a2: 0, x1: 0, x2: 0, y1: 0, y2: 0 }; }",
    "function fijarBypass(f) { f.b0 = 1; f.b1 = 0; f.b2 = 0; f.a1 = 0; f.a2 = 0; }",
    "function tick(f, x) {",
    "  var y = f.b0 * x + f.b1 * f.x1 + f.b2 * f.x2 - f.a1 * f.y1 - f.a2 * f.y2;",
    "  f.x2 = f.x1; f.x1 = x; f.y2 = f.y1; f.y1 = y;",
    "  return y;",
    "}",
    "function disenar(f, tipo, sr, freq, q, gainDb) {",
    "  var ny = sr * 0.45;",
    "  if (freq < 15) freq = 15;",
    "  if (freq > ny) freq = ny;",
    "  if (!(q > 0.05)) q = 0.05;",
    "  var A = Math.pow(10, gainDb / 40);",
    "  var w0 = 2 * Math.PI * freq / sr;",
    "  var cos = Math.cos(w0), sin = Math.sin(w0);",
    "  var alpha, b0, b1, b2, a0, a1, a2, two;",
    "  if (tipo === 'hpf' || tipo === 'bp' || tipo === 'peak') alpha = sin / (2 * q);",
    "  else alpha = sin / 2 * Math.sqrt((A + 1 / A) * (1 / q - 1) + 2);",
    "  if (tipo === 'hpf') {",
    "    b0 = (1 + cos) / 2; b1 = -(1 + cos); b2 = (1 + cos) / 2;",
    "    a0 = 1 + alpha; a1 = -2 * cos; a2 = 1 - alpha;",
    "  } else if (tipo === 'bp') {",
    "    b0 = alpha; b1 = 0; b2 = -alpha;",
    "    a0 = 1 + alpha; a1 = -2 * cos; a2 = 1 - alpha;",
    "  } else if (tipo === 'peak') {",
    "    b0 = 1 + alpha * A; b1 = -2 * cos; b2 = 1 - alpha * A;",
    "    a0 = 1 + alpha / A; a1 = -2 * cos; a2 = 1 - alpha / A;",
    "  } else if (tipo === 'low') {",
    "    two = 2 * Math.sqrt(A) * alpha;",
    "    b0 = A * ((A + 1) - (A - 1) * cos + two);",
    "    b1 = 2 * A * ((A - 1) - (A + 1) * cos);",
    "    b2 = A * ((A + 1) - (A - 1) * cos - two);",
    "    a0 = (A + 1) + (A - 1) * cos + two;",
    "    a1 = -2 * ((A - 1) + (A + 1) * cos);",
    "    a2 = (A + 1) + (A - 1) * cos - two;",
    "  } else {",
    "    two = 2 * Math.sqrt(A) * alpha;",
    "    b0 = A * ((A + 1) + (A - 1) * cos + two);",
    "    b1 = -2 * A * ((A - 1) + (A + 1) * cos);",
    "    b2 = A * ((A + 1) + (A - 1) * cos - two);",
    "    a0 = (A + 1) - (A - 1) * cos + two;",
    "    a1 = 2 * ((A - 1) - (A + 1) * cos);",
    "    a2 = (A + 1) - (A - 1) * cos - two;",
    "  }",
    "  f.b0 = b0 / a0; f.b1 = b1 / a0; f.b2 = b2 / a0; f.a1 = a1 / a0; f.a2 = a2 / a0;",
    "}",
    "function coef(ms, sr) {",
    "  var t = ms * 0.001;",
    "  if (t < 0.00005) t = 0.00005;",
    "  return Math.exp(-1 / (t * sr));",
    "}",
    "function linDb(x) {",
    "  if (!(x > 1e-10)) return -120;",
    "  return 20 * Math.log10(x);",
    "}",
    "function dbLin(db) {",
    "  if (db <= -120) return 0;",
    "  return Math.pow(10, db / 20);",
    "}",
    "function reduccion(nivel, thr, ratio, knee) {",
    "  if (!(ratio > 1)) return 0;",
    "  var pend = 1 - 1 / ratio;",
    "  if (!(knee > 0)) { var over = nivel - thr; return over > 0 ? over * pend : 0; }",
    "  var half = knee * 0.5;",
    "  if (nivel < thr - half) return 0;",
    "  if (nivel > thr + half) return (nivel - thr) * pend;",
    "  var x = nivel - thr + half;",
    "  return (x * x) / (2 * knee) * pend;",
    "}",
    "registerProcessor('lv-podcast-canal', CanalPodcast);",
    "registerProcessor('lv-podcast-wav', GrabadorPodcast);"
  ].join('\n');

  function dbALineal(db) {
    if (db <= -89.9) return 0;
    return Math.pow(10, db / 20);
  }

  function error(msg) { throw new Error('LVPodcastAudio: ' + msg); }

  function normalizar(nombre, valor) {
    var f = POR_NOMBRE[nombre];
    if (!f) error('parámetro desconocido «' + nombre + '». Los nombres válidos son los de LVPodcastAudio.PARAMETROS.');
    if (nombre === 'riderEnabled' && typeof valor === 'boolean') valor = valor ? 1 : 0;
    if (typeof valor !== 'number' || !isFinite(valor)) error('«' + nombre + '» espera un número.');
    if (nombre === 'riderEnabled') valor = valor >= 0.5 ? 1 : 0;
    if (valor < f.duro[0]) valor = f.duro[0];
    if (valor > f.duro[1]) valor = f.duro[1];
    return valor;
  }

  function rampa(ctx, param, valor, tau) {
    var t = ctx.currentTime || 0;
    if (!(t > 0) || !(tau > 0)) {
      param.cancelScheduledValues(0);
      param.setValueAtTime(valor, 0);
      return;
    }
    param.cancelScheduledValues(t);
    param.setValueAtTime(param.value, t);
    param.setTargetAtTime(valor, t, tau);
  }

  function fijarMono(nodo) {
    try {
      nodo.channelCount = 1;
      nodo.channelCountMode = 'explicit';
      nodo.channelInterpretation = 'speakers';
    } catch (e) { /* el worklet a veces no deja fijar el conteo; la salida sigue siendo mono */ }
  }

  function fijarEstereo(nodo) {
    /* No forzar channelCount 2: en file:// con ScriptProcessor, un GainNode
       estéreo explícito deja colgado el render offline de Chrome. El merger
       ya entrega dos canales y el modo por defecto los conserva. */
    void nodo;
  }

  function gananciasPan(p) {
    var ang = ((p + 1) * 0.5) * Math.PI * 0.5;
    return [Math.cos(ang), Math.sin(ang)];
  }

  function codificarWav(L, R, sr) {
    var n = L.length;
    var bytes = n * 2 * 2;
    var buf = new ArrayBuffer(44 + bytes);
    var v = new DataView(buf);
    function str(o, s) { for (var i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); }
    str(0, 'RIFF');
    v.setUint32(4, 36 + bytes, true);
    str(8, 'WAVE');
    str(12, 'fmt ');
    v.setUint32(16, 16, true);
    v.setUint16(20, 1, true);
    v.setUint16(22, 2, true);
    v.setUint32(24, sr, true);
    v.setUint32(28, sr * 4, true);
    v.setUint16(32, 4, true);
    v.setUint16(34, 16, true);
    str(36, 'data');
    v.setUint32(40, bytes, true);
    var o = 44, i, s;
    for (i = 0; i < n; i++) {
      s = L[i]; if (s > 1) s = 1; else if (s < -1) s = -1;
      v.setInt16(o, s < 0 ? Math.round(s * 32768) : Math.round(s * 32767), true); o += 2;
      s = R[i]; if (s > 1) s = 1; else if (s < -1) s = -1;
      v.setInt16(o, s < 0 ? Math.round(s * 32768) : Math.round(s * 32767), true); o += 2;
    }
    return new Blob([buf], { type: 'audio/wav' });
  }

  function elegirMime() {
    if (typeof MediaRecorder === 'undefined' || !MediaRecorder.isTypeSupported) return '';
    var lista = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus'];
    for (var i = 0; i < lista.length; i++) if (MediaRecorder.isTypeSupported(lista[i])) return lista[i];
    return '';
  }

  function crear(opciones) {
    opciones = opciones || {};
    var Ctx = global.AudioContext || global.webkitAudioContext;
    if (!Ctx && !opciones.contexto) error('este navegador no tiene AudioContext.');
    var ctx = opciones.contexto || null;
    if (!ctx) {
      try {
        var opts = { latencyHint: 'interactive' };
        if (opciones.sampleRate) opts.sampleRate = opciones.sampleRate;
        ctx = new Ctx(opts);
      } catch (e) {
        ctx = new Ctx();
      }
    }
    if (!ctx.audioWorklet) error('este navegador no tiene AudioWorklet. Hace falta Chrome, Edge o Firefox reciente.');

    var modoPan = opciones.panoramica || 'auto';
    var usarPanner = modoPan !== 'ganancias' && typeof ctx.createStereoPanner === 'function';
    if (modoPan === 'stereo' && !usarPanner) error('este navegador no tiene StereoPannerNode.');

    var bus = ctx.createGain();
    fijarEstereo(bus);
    bus.gain.value = 1;
    var master = ctx.createGain();
    fijarEstereo(master);
    var limitador = ctx.createDynamicsCompressor();
    limitador.threshold.value = -1.5;
    limitador.knee.value = 0;
    limitador.ratio.value = 20;
    limitador.attack.value = 0.002;
    limitador.release.value = 0.08;
    var monitor = ctx.createGain();
    fijarEstereo(monitor);
    var analizador = ctx.createAnalyser();
    analizador.fftSize = 2048;
    analizador.smoothingTimeConstant = 0.4;
    var analizadorVoz = ctx.createAnalyser();
    analizadorVoz.fftSize = 2048;
    analizadorVoz.smoothingTimeConstant = 0.25;
    bus.connect(analizadorVoz);
    bus.connect(master);
    master.connect(limitador);
    limitador.connect(monitor);
    limitador.connect(analizador);
    if (opciones.salida !== false) monitor.connect(ctx.destination);

    var estado = {
      ctx: ctx,
      bus: bus,
      master: master,
      limitador: limitador,
      monitor: monitor,
      analizador: analizador,
      analizadorVoz: analizadorVoz,
      micros: [],
      porId: {},
      monitorDb: typeof opciones.monitorDb === 'number' ? opciones.monitorDb : 0,
      monitorMudo: false,
      masterDb: 0,
      techoDb: -1.5,
      limitadorActivo: opciones.limitador !== false,
      duck: { activo: true, profundidadDb: -10, ataqueMs: 15, sueltaMs: 280, umbralDb: -32 },
      grabacion: null,
      usarPanner: usarPanner,
      seq: 1,
      cerrado: false,
      camas: [],
      porCama: {},
      escenaId: 'entrevista',
      bleed: false,
      oyentes: [],
      speechDb: -80
    };
    aplicarMaster(estado);
    aplicarMonitor(estado);
    aplicarLimitador(estado);

    var listo = asegurarModulo(ctx);

    var esOffline = typeof ctx.startRendering === 'function';
    var reloj = esOffline ? 0 : setInterval(function () {
      if (estado.cerrado) return;
      actualizarDucks(estado);
      actualizarCamas(estado);
    }, 20);
    var relojMed = esOffline ? 0 : setInterval(function () {
      if (!estado.cerrado) publicarMedidores(estado);
    }, 50);
    estado.reloj = reloj;
    estado.relojMed = relojMed;

    var api = {
      _estado: estado,
      contexto: ctx,
      listo: listo,
      nodoMezcla: bus,
      nodoMaster: master,
      nodoMonitor: monitor,
      usarStereoPanner: usarPanner,
      modo: function () { return ctx._lvModo || 'cargando'; },
      crearMicro: function (id) { return crearMicro(estado, listo, id); },
      quitarMicro: function (id) { quitarMicro(estado, id); },
      micro: function (id) { return estado.porId[id] || null; },
      listaMicros: function () { return estado.micros.map(function (m) { return m.id; }); },
      reanudar: function () { return ctx.state === 'running' ? Promise.resolve(ctx.state) : ctx.resume().then(function () { return ctx.state; }); },
      setGananciaMaestraDb: function (db) {
        if (typeof db !== 'number' || !isFinite(db)) error('la ganancia maestra espera un número en dB.');
        if (db < -90) db = -90;
        if (db > 18) db = 18;
        estado.masterDb = db;
        rampa(ctx, master.gain, dbALineal(db), 0.015);
        return db;
      },
      getGananciaMaestraDb: function () { return estado.masterDb; },
      setTechoDb: function (db) {
        if (typeof db !== 'number' || !isFinite(db)) error('el techo espera un número en dB.');
        if (db < -18) db = -18;
        if (db > 0) db = 0;
        estado.techoDb = db;
        estado.limitadorActivo = true;
        aplicarLimitador(estado);
        return db;
      },
      getTechoDb: function () { return estado.techoDb; },
      setLimitador: function (activo) {
        estado.limitadorActivo = !!activo;
        aplicarLimitador(estado);
        return estado.limitadorActivo;
      },
      setMonitorDb: function (db) {
        if (typeof db !== 'number' || !isFinite(db)) error('el monitor espera un número en dB.');
        if (db < -90) db = -90;
        if (db > 12) db = 12;
        estado.monitorDb = db;
        aplicarMonitor(estado);
        return db;
      },
      getMonitorDb: function () { return estado.monitorDb; },
      setMonitorMudo: function (activo) {
        estado.monitorMudo = !!activo;
        aplicarMonitor(estado);
        return estado.monitorMudo;
      },
      getMonitorMudo: function () { return estado.monitorMudo; },
      setCrossDuck: function (cfg) {
        cfg = cfg || {};
        var d = estado.duck;
        if (cfg.activo != null) d.activo = !!cfg.activo;
        if (cfg.profundidadDb != null) {
          var p = +cfg.profundidadDb;
          if (!isFinite(p)) error('profundidadDb del cross-duck no es un número.');
          if (p > 0) p = -p;
          if (p < -30) p = -30;
          d.profundidadDb = p;
        }
        if (cfg.ataqueMs != null) d.ataqueMs = clampNum(+cfg.ataqueMs, 1, 200);
        if (cfg.sueltaMs != null) d.sueltaMs = clampNum(+cfg.sueltaMs, 20, 2000);
        if (cfg.umbralDb != null) d.umbralDb = clampNum(+cfg.umbralDb, -80, 0);
        return api.getCrossDuck();
      },
      getCrossDuck: function () {
        return {
          activo: estado.duck.activo,
          profundidadDb: estado.duck.profundidadDb,
          ataqueMs: estado.duck.ataqueMs,
          sueltaMs: estado.duck.sueltaMs,
          umbralDb: estado.duck.umbralDb
        };
      },
      leerMaster: function () { return { rmsDb: rmsAnalizador(analizador), techoDb: estado.techoDb, faderDb: estado.masterDb }; },
      grabar: function (op) { return grabar(estado, op || {}); },
      pararGrabacion: function () { return pararGrabacion(estado); },
      estaGrabando: function () { return !!estado.grabacion; },
      cerrar: function () {
        estado.cerrado = true;
        if (estado.reloj) clearInterval(estado.reloj);
        if (estado.relojMed) clearInterval(estado.relojMed);
        if (estado.grabacion) {
          try { estado.grabacion.abortar(); } catch (e) {}
        }
        estado.micros.slice().forEach(function (m) { quitarMicro(estado, m.id); });
        try { monitor.disconnect(); } catch (e) {}
        if (ctx.close) return Promise.resolve(ctx.close()).catch(function () {});
        return Promise.resolve();
      }
    };
    fijarEscena(estado, 'entrevista');
    return api;
  }

  function clampNum(v, a, b) {
    if (!isFinite(v)) error('se esperaba un número.');
    if (v < a) return a;
    if (v > b) return b;
    return v;
  }

  function aplicarMaster(estado) {
    rampa(estado.ctx, estado.master.gain, dbALineal(estado.masterDb), 0);
  }

  function aplicarMonitor(estado) {
    var lin = estado.monitorMudo ? 0 : dbALineal(estado.monitorDb);
    rampa(estado.ctx, estado.monitor.gain, lin, estado.ctx.currentTime > 0 ? 0.015 : 0);
  }

  function aplicarLimitador(estado) {
    var lim = estado.limitador;
    if (!estado.limitadorActivo) {
      lim.threshold.value = 0;
      lim.knee.value = 0;
      lim.ratio.value = 1;
      lim.attack.value = 0.002;
      lim.release.value = 0.05;
      return;
    }
    lim.threshold.value = estado.techoDb;
    lim.knee.value = 0;
    lim.ratio.value = 20;
    lim.attack.value = 0.002;
    lim.release.value = 0.08;
  }

  function nucleoLocal(sampleRate) {
    var factory = new Function('sampleRate', [
      'var registrados = {};',
      'function AudioWorkletProcessor() {',
      '  this.port = { postMessage: function (m) { this.ultimo = m; } };',
      '}',
      'function registerProcessor(nombre, Ctor) { registrados[nombre] = Ctor; }',
      FUENTE,
      'return registrados;'
    ].join('\n'));
    return factory(sampleRate);
  }

  function asegurarModulo(ctx) {
    if (ctx._lvPodcastModulo) return ctx._lvPodcastModulo;
    var blob = new Blob([FUENTE], { type: 'application/javascript' });
    var url = URL.createObjectURL(blob);
    ctx._lvPodcastModulo = ctx.audioWorklet.addModule(url).then(function () {
      URL.revokeObjectURL(url);
      ctx._lvModo = 'worklet';
    }, function () {
      URL.revokeObjectURL(url);
      ctx._lvModo = 'script';
      ctx._lvRegs = nucleoLocal(ctx.sampleRate);
    });
    return ctx._lvPodcastModulo;
  }

  function engancharScript(estado, mic) {
    var regs = estado.ctx._lvRegs;
    var Ctor = regs['lv-podcast-canal'];
    var motor = new Ctor();
    var bufs = {};
    Ctor.parameterDescriptors.forEach(function (d) {
      if (d.name === 'pan') return;
      bufs[d.name] = new Float32Array([mic._params[d.name]]);
    });
    var sp = estado.ctx.createScriptProcessor(256, 1, 1);
    sp.onaudioprocess = function (e) {
      var inn = e.inputBuffer.getChannelData(0);
      var out = e.outputBuffer.getChannelData(0);
      var k, i;
      try {
        for (k in bufs) bufs[k][0] = mic._params[k];
        if (bufs.gateThresholdDb) bufs.gateThresholdDb[0] = umbralEfectivo(estado, mic._params.gateThresholdDb);
        motor.process([[inn]], [[out]], bufs);
        if (motor.port && motor.port.ultimo) mic._med = motor.port.ultimo;
      } catch (err) {
        mic._fallo = String(err && err.stack || err);
        for (i = 0; i < out.length; i++) out[i] = 0;
      }
    };
    sp.connect(mic.fader);
    mic._script = sp;
    mic._motor = motor;
    mic.entrada = sp;
    mic.latenciaMs = 2 + Math.round(256000 / estado.ctx.sampleRate);
    montarPan(estado, mic, false);
    return mic;
  }

  function fabricarMicro(estado, id) {
    var ctx = estado.ctx;
    var fader = ctx.createGain();
    var mute = ctx.createGain();
    fijarMono(fader);
    fijarMono(mute);
    fader.gain.value = 1;
    mute.gain.value = 1;
    fader.connect(mute);

    var panNodo, gainL, gainR, merger;
    var duck = ctx.createGain();
    fijarEstereo(duck);
    duck.gain.value = 1;

    duck.connect(estado.bus);
    /* panorama se monta al saber el modo */

    var params = {};
    FICHA.forEach(function (f) { params[f.nombre] = f.defecto; });

    var mic = {
      id: id,
      nodo: null,
      fader: fader,
      mute: mute,
      panNodo: panNodo || null,
      gainL: gainL || null,
      gainR: gainR || null,
      duck: duck,
      _params: params,
      _gainDb: 0,
      _mudo: false,
      _solo: false,
      _fuente: null,
      _ajena: false,
      _med: { inDb: -120, outPeakDb: -120, outRmsDb: -120, puerta: 0, puertaDb: 0, deEssDb: 0, compDb: 0, riderDb: 0 },
      _duckEnv: 0,
      _errorProcesador: false
    };

    mic.setParam = function (nombre, valor) {
      var v = normalizar(nombre, valor);
      mic._params[nombre] = v;
      if (nombre === 'pan') aplicarPan(estado, mic, v);
      else if (mic.nodo) {
        var enviado = nombre === 'gateThresholdDb' ? umbralEfectivo(estado, v) : v;
        var p = mic.nodo.parameters.get(nombre);
        rampa(estado.ctx, p, enviado, estado.ctx.currentTime > 0 ? 0.012 : 0);
      }
      return v;
    };
    mic.getParams = function () {
      var o = {};
      for (var i = 0; i < PARAMETROS.length; i++) o[PARAMETROS[i]] = mic._params[PARAMETROS[i]];
      return o;
    };
    mic.setGainDb = function (db) {
      if (typeof db !== 'number' || !isFinite(db)) error('setGainDb espera un número en dB.');
      if (db < -90) db = -90;
      if (db > 18) db = 18;
      mic._gainDb = db;
      rampa(ctx, fader.gain, dbALineal(db), ctx.currentTime > 0 ? 0.012 : 0);
      return db;
    };
    mic.getGainDb = function () { return mic._gainDb; };
    mic.setMute = function (activo) {
      mic._mudo = !!activo;
      aplicarRutas(estado);
      return mic._mudo;
    };
    mic.getMute = function () { return mic._mudo; };
    mic.setSolo = function (activo) {
      mic._solo = !!activo;
      aplicarRutas(estado);
      return mic._solo;
    };
    mic.getSolo = function () { return mic._solo; };
    mic.enchufarStream = function (stream) {
      if (!mic.entrada) error('el micro aún no está listo. Espera a la promesa de crearMicro.');
      if (!stream || typeof stream.getAudioTracks !== 'function' || stream.getAudioTracks().length === 0) {
        error('el stream no trae pista de audio.');
      }
      mic.desenchufar();
      var src = ctx.createMediaStreamSource(stream);
      src.connect(mic.entrada);
      mic._fuente = src;
      mic._ajena = false;
      mic._stream = stream;
      return mic;
    };
    mic.enchufarNodo = function (nodo) {
      if (!mic.entrada) error('el micro aún no está listo. Espera a la promesa de crearMicro.');
      if (!nodo || typeof nodo.connect !== 'function') error('enchufarNodo espera un AudioNode.');
      mic.desenchufar();
      nodo.connect(mic.entrada);
      mic._fuente = nodo;
      mic._ajena = true;
      return mic;
    };
    mic.desenchufar = function () {
      if (mic._fuente) {
        try { mic._fuente.disconnect(mic.entrada); } catch (e) {}
      }
      mic._fuente = null;
      mic._stream = null;
      mic._ajena = false;
      return mic;
    };
    mic.leerMedidor = function () {
      var m = mic._med || {};
      return {
        entradaDb: m.inDb,
        salidaDb: m.outRmsDb,
        picoDb: m.outPeakDb,
        puerta: m.puerta,
        puertaDb: m.puertaDb,
        deEssDb: m.deEssDb,
        compDb: m.compDb,
        riderDb: m.riderDb,
        faderDb: mic._gainDb,
        mudo: mic._mudo,
        solo: mic._solo,
        pan: mic._params.pan,
        duck: mic._duckEnv
      };
    };
    mic.aplicarReceta = function (nombre) { return aplicarReceta(mic, nombre); };
    mic.latenciaMs = 2;
    return mic;
  }

  function montarPan(estado, mic, conPanner) {
    if (mic._panMontado) return;
    var ctx = estado.ctx;
    var usar = !!conPanner && estado.usarPanner;
    if (usar) {
      mic.panNodo = ctx.createStereoPanner();
      mic.panNodo.pan.value = 0;
      mic.mute.connect(mic.panNodo);
      mic.panNodo.connect(mic.duck);
    } else {
      mic.gainL = ctx.createGain();
      mic.gainR = ctx.createGain();
      fijarMono(mic.gainL);
      fijarMono(mic.gainR);
      var merger = ctx.createChannelMerger(2);
      mic.mute.connect(mic.gainL);
      mic.mute.connect(mic.gainR);
      mic.gainL.connect(merger, 0, 0);
      mic.gainR.connect(merger, 0, 1);
      merger.connect(mic.duck);
      mic._merger = merger;
    }
    mic._panMontado = true;
    aplicarPan(estado, mic, mic._params.pan);
  }

  function aplicarPan(estado, mic, p) {
    if (mic.panNodo) {
      rampa(estado.ctx, mic.panNodo.pan, p, estado.ctx.currentTime > 0 ? 0.012 : 0);
      return;
    }
    var g = gananciasPan(p);
    rampa(estado.ctx, mic.gainL.gain, g[0], estado.ctx.currentTime > 0 ? 0.012 : 0);
    rampa(estado.ctx, mic.gainR.gain, g[1], estado.ctx.currentTime > 0 ? 0.012 : 0);
  }

  function aplicarRutas(estado) {
    var alguno = false;
    for (var i = 0; i < estado.micros.length; i++) if (estado.micros[i]._solo) alguno = true;
    var t = estado.ctx.currentTime > 0 ? 0.005 : 0;
    for (i = 0; i < estado.micros.length; i++) {
      var m = estado.micros[i];
      var abierto = !m._mudo && (!alguno || m._solo);
      rampa(estado.ctx, m.mute.gain, abierto ? 1 : 0, t);
    }
  }

  function nivelPostFader(mic) {
    if (mic._mudo) return -120;
    var rms = mic._med && typeof mic._med.outRmsDb === 'number' ? mic._med.outRmsDb : -120;
    return rms + mic._gainDb;
  }

  function actualizarDucks(estado) {
    var d = estado.duck;
    var niveles = estado.micros.map(nivelPostFader);
    var ahora = estado.ctx.currentTime || 0;
    for (var i = 0; i < estado.micros.length; i++) {
      var otro = -120;
      for (var j = 0; j < niveles.length; j++) if (j !== i && niveles[j] > otro) otro = niveles[j];
      var amount = 0;
      if (d.activo && estado.micros.length > 1 && otro >= d.umbralDb) {
        if (niveles[i] < d.umbralDb) amount = (otro - d.umbralDb) / 12;
        else amount = (otro - niveles[i]) / 10;
        if (amount < 0) amount = 0;
        if (amount > 1) amount = 1;
      }
      var env = estado.micros[i]._duckEnv;
      var tau = ((amount > env ? d.ataqueMs : d.sueltaMs) / 1000);
      if (tau < 0.005) tau = 0.005;
      var k = 1 - Math.exp(-0.02 / tau);
      env = env + (amount - env) * k;
      if (env < 1e-4) env = 0;
      estado.micros[i]._duckEnv = env;
      var db = d.profundidadDb * env;
      var lin = dbALineal(db);
      if (ahora > 0) {
        try {
          estado.micros[i].duck.gain.setTargetAtTime(lin, ahora, 0.01);
        } catch (e) {}
      } else {
        estado.micros[i].duck.gain.value = lin;
      }
    }
  }

  function quitarMicro(estado, id) {
    var mic = estado.porId[id];
    if (!mic) error('no hay micro «' + id + '».');
    mic.desenchufar();
    try { if (mic.nodo) mic.nodo.disconnect(); } catch (e) {}
    try { if (mic._script) { mic._script.onaudioprocess = null; mic._script.disconnect(); } } catch (e) {}
    try { mic.fader.disconnect(); } catch (e) {}
    try { mic.mute.disconnect(); } catch (e) {}
    try { if (mic.panNodo) mic.panNodo.disconnect(); } catch (e) {}
    try { if (mic.gainL) mic.gainL.disconnect(); } catch (e) {}
    try { if (mic.gainR) mic.gainR.disconnect(); } catch (e) {}
    try { mic.duck.disconnect(); } catch (e) {}
    if (mic.nodo && mic.nodo.port) mic.nodo.port.onmessage = null;
    delete estado.porId[id];
    estado.micros = estado.micros.filter(function (m) { return m !== mic; });
    aplicarRutas(estado);
  }

  function aplicarReceta(mic, nombre) {
    if (nombre === 'defecto') {
      FICHA.forEach(function (f) { mic.setParam(f.nombre, f.defecto); });
      return mic.getParams();
    }
    if (nombre === 'neutro') nombre = 'seco';
    var sc = ESCENAS[nombre];
    if (!sc || !sc.params) error('escena desconocida «' + nombre + '».');
    Object.keys(sc.params).forEach(function (k) {
      if (k === 'pan') return;
      mic.setParam(k, sc.params[k]);
    });
    return mic.getParams();
  }

  function rmsAnalizador(an) {
    var buf = new Float32Array(an.fftSize);
    try { an.getFloatTimeDomainData(buf); } catch (e) { return -120; }
    var s = 0;
    for (var i = 0; i < buf.length; i++) s += buf[i] * buf[i];
    return 10 * Math.log10(s / buf.length + 1e-12);
  }

  function grabar(estado, op) {
    if (estado.grabacion) error('ya hay una grabación en curso.');
    if (estado.ctx.state === 'suspended') error('el contexto está suspendido. Llama a reanudar() dentro del gesto.');
    var formato = op.formato || 'webm';
    var t0 = estado.ctx.currentTime;
    if (formato === 'wav') return grabarWav(estado, t0);
    if (formato !== 'webm') error('formato de grabación desconocido. Usa "webm" o "wav".');
    if (typeof estado.ctx.createMediaStreamDestination !== 'function' || typeof MediaRecorder === 'undefined') {
      error('este navegador no puede grabar webm. Usa formato "wav".');
    }
    var dest = estado.ctx.createMediaStreamDestination();
    estado.limitador.connect(dest);
    var mime = elegirMime();
    var rec;
    try { rec = mime ? new MediaRecorder(dest.stream, { mimeType: mime, audioBitsPerSecond: 128000 }) : new MediaRecorder(dest.stream); }
    catch (e) { try { dest.disconnect(); } catch (e2) {} error('no se pudo abrir MediaRecorder.'); }
    var partes = [];
    rec.ondataavailable = function (e) { if (e.data && e.data.size) partes.push(e.data); };
    var toma = {
      formato: 'webm',
      abortar: function () { try { rec.stop(); } catch (e) {} try { estado.limitador.disconnect(dest); } catch (e) {} },
      parar: function () {
        return new Promise(function (resolver, rechazar) {
          rec.onstop = function () {
            try { estado.limitador.disconnect(dest); } catch (e) {}
            var tipo = rec.mimeType || mime || 'audio/webm';
            var blob = new Blob(partes, { type: tipo });
            resolver({
              blob: blob,
              mime: tipo,
              url: URL.createObjectURL(blob),
              duracionSeg: Math.max(0, estado.ctx.currentTime - t0),
              formato: 'webm',
              recortado: false
            });
          };
          rec.onerror = function () { rechazar(new Error('LVPodcastAudio: falló la grabación.')); };
          try { rec.stop(); } catch (e) { rechazar(e); }
        });
      }
    };
    try { rec.start(1000); } catch (e) { try { estado.limitador.disconnect(dest); } catch (e2) {} error('no se pudo empezar a grabar.'); }
    estado.grabacion = toma;
    return toma;
  }

  function grabarWavScript(estado) {
    var sr = estado.ctx.sampleRate;
    var max = sr * 60 * 10;
    var sp = estado.ctx.createScriptProcessor(1024, 2, 2);
    var trozosL = [], trozosR = [], muestras = 0, lleno = false, parado = false;
    sp.onaudioprocess = function (e) {
      if (parado || lleno) return;
      var l = e.inputBuffer.getChannelData(0);
      var rch = e.inputBuffer.numberOfChannels > 1 ? e.inputBuffer.getChannelData(1) : l;
      var n = l.length;
      var queda = max - muestras;
      if (n > queda) { n = queda; lleno = true; }
      if (n <= 0) return;
      trozosL.push(l.slice(0, n));
      trozosR.push(rch.slice(0, n));
      muestras += n;
    };
    estado.limitador.connect(sp);
    var sumidero = estado.ctx.createGain();
    sumidero.gain.value = 0;
    sp.connect(sumidero);
    sumidero.connect(estado.ctx.destination);
    return {
      formato: 'wav',
      abortar: function () {
        parado = true;
        try { estado.limitador.disconnect(sp); } catch (e) {}
        try { sp.disconnect(); } catch (e) {}
        sp.onaudioprocess = null;
      },
      parar: function () {
        parado = true;
        try { estado.limitador.disconnect(sp); } catch (e) {}
        try { sp.disconnect(); } catch (e) {}
        sp.onaudioprocess = null;
        var L = new Float32Array(muestras);
        var R = new Float32Array(muestras);
        var o = 0, i;
        for (i = 0; i < trozosL.length; i++) {
          L.set(trozosL[i], o);
          R.set(trozosR[i], o);
          o += trozosL[i].length;
        }
        var blob = codificarWav(L, R, sr);
        return Promise.resolve({
          blob: blob,
          mime: 'audio/wav',
          url: URL.createObjectURL(blob),
          duracionSeg: muestras / sr,
          formato: 'wav',
          recortado: lleno,
          muestras: muestras
        });
      }
    };
  }

  function grabarWav(estado, t0) {
    return asegurarModulo(estado.ctx).then(function () {
      if (estado.grabacion) error('ya hay una grabación en curso.');
      if (estado.ctx._lvModo === 'script') {
        var tomaS = grabarWavScript(estado);
        estado.grabacion = tomaS;
        return tomaS;
      }
      var nodo = new AudioWorkletNode(estado.ctx, 'lv-podcast-wav', {
        numberOfInputs: 1,
        numberOfOutputs: 1,
        outputChannelCount: [2],
        channelCount: 2,
        channelCountMode: 'explicit'
      });
      fijarEstereo(nodo);
      estado.limitador.connect(nodo);
      // El worklet no tiene salida útil: un gain mudo lo mantiene en el grafo.
      var sumidero = estado.ctx.createGain();
      sumidero.gain.value = 0;
      nodo.connect(sumidero);
      sumidero.connect(estado.ctx.destination);
      var toma = {
        formato: 'wav',
        abortar: function () {
          try { nodo.port.postMessage({ cmd: 'parar' }); } catch (e) {}
          try { estado.limitador.disconnect(nodo); } catch (e) {}
          try { nodo.disconnect(); } catch (e) {}
        },
        parar: function () {
          return new Promise(function (resolver, rechazar) {
            var timer = setTimeout(function () { rechazar(new Error('LVPodcastAudio: la grabación WAV no respondió.')); }, 8000);
            nodo.port.onmessage = function (ev) {
              var data = ev.data || {};
              if (data.cmd !== 'wav') return;
              clearTimeout(timer);
              try { estado.limitador.disconnect(nodo); } catch (e) {}
              try { nodo.disconnect(); } catch (e) {}
              var blob = codificarWav(data.l, data.r, data.sr || estado.ctx.sampleRate);
              resolver({
                blob: blob,
                mime: 'audio/wav',
                url: URL.createObjectURL(blob),
                duracionSeg: data.l.length / (data.sr || estado.ctx.sampleRate),
                formato: 'wav',
                recortado: !!data.lleno,
                muestras: data.l.length
              });
            };
            nodo.port.postMessage({ cmd: 'parar' });
          });
        }
      };
      estado.grabacion = toma;
      return toma;
    });
  }

  function pararGrabacion(estado) {
    var toma = estado.grabacion;
    if (!toma) error('no hay grabación en curso.');
    estado.grabacion = null;
    return Promise.resolve(toma.parar());
  }

  function medirBuffer(buf, desdeSeg) {
    var a = buf.getChannelData(0);
    var b = buf.numberOfChannels > 1 ? buf.getChannelData(1) : a;
    var i0 = Math.floor(desdeSeg * buf.sampleRate);
    if (i0 < 0) i0 = 0;
    var sl = 0, sr = 0, n = 0, i;
    for (i = i0; i < a.length; i++) { sl += a[i] * a[i]; sr += b[i] * b[i]; n++; }
    function db(p) { return 10 * Math.log10(p + 1e-20); }
    return { rmsL: db(sl / n), rmsR: db(sr / n), rmsSuma: db((sl + sr) / n), n: n };
  }

  function autoPrueba() {
    var pruebas = [];
    function anotar(nombre, ok, detalle) {
      pruebas.push({ nombre: nombre, ok: !!ok, detalle: detalle == null ? '' : String(detalle) });
    }
    var Offline = global.OfflineAudioContext || global.webkitOfflineAudioContext;
    if (!Offline) {
      anotar('offline', false, 'no hay OfflineAudioContext');
      return Promise.resolve({ ok: false, pruebas: pruebas });
    }

    function render(freq, amp, dur, panoramica, tocar) {
      var sr = 48000;
      var muestras = Math.ceil(sr * dur / 256) * 256;
      var ctx = new Offline(2, muestras, sr);
      var motor = crear({ contexto: ctx, limitador: false, monitorDb: 0, panoramica: panoramica || 'auto', salida: true });
      return motor.listo.then(function () { return motor.crearMicro('t'); }).then(function (mic) {
        mic.aplicarReceta('neutro');
        mic.setGainDb(0);
        mic.setMute(false);
        mic.setSolo(false);
        if (tocar) tocar(mic, motor);
        var osc = ctx.createOscillator();
        var gn = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, 0);
        gn.gain.setValueAtTime(amp, 0);
        osc.connect(gn);
        mic.enchufarNodo(gn);
        osc.start(0);
        return ctx.startRendering().then(function (buf) {

          return motor.cerrar().then(function () { return buf; });
        });
      });
    }

    // Contrato, sin audio.
    var clavesOk = PARAMETROS.join('|') === FICHA.map(function (f) { return f.nombre; }).join('|');
    anotar('nombres', clavesOk && PARAMETROS.length === 31, PARAMETROS.length + ' nombres');
    anotar('sin LVSonido', typeof global.LVSonido === 'undefined', typeof global.LVSonido);
    var ctxC = new Offline(2, 1024, 48000);
    var motorC = crear({ contexto: ctxC, limitador: false, salida: false });
    return motorC.listo.then(function () { return motorC.crearMicro('c'); }).then(function (mic) {
      var gp = mic.getParams();
      var claves = Object.keys(gp);
      anotar('getParams mismos nombres', claves.join('|') === PARAMETROS.join('|'), claves.join(','));
      var defectoOk = FICHA.every(function (f) { return gp[f.nombre] === f.defecto; });
      anotar('defectos', defectoOk, defectoOk ? '' : JSON.stringify(gp));
      var lanzo = false;
      try { mic.setParam('crearLimpieza', 1); } catch (e) { lanzo = true; }
      anotar('nombre ajeno rechazado', lanzo, '');
      anotar('pan se recorta a 1', mic.setParam('pan', 4) === 1 && mic.getParams().pan === 1, mic.getParams().pan);
      anotar('riderEnabled 0 o 1', mic.setParam('riderEnabled', 0.2) === 0 && mic.setParam('riderEnabled', true) === 1, '');
      anotar('compMix dentro de 0..1', mic.setParam('compMix', 3) === 1, mic.getParams().compMix);
      anotar('setGainDb no es setParam', (function () {
        var mal = false;
        try { mic.setParam('setGainDb', -3); } catch (e) { mal = true; }
        return mal && mic.setGainDb(-6) === -6 && mic.getGainDb() === -6 && mic.getParams().pan === 1;
      })(), '');
      anotar('mute y solo', mic.setMute(true) === true && mic.getMute() === true && mic.setSolo(true) === true && mic.setMute(false) === false, '');
      return ctxC.startRendering().then(function () { return motorC.cerrar(); });
    }).then(function () {
      var esperado = 20 * Math.log10(0.2) - 10 * Math.log10(2); // 10*log10(potencia) de un seno de pico 0.2
      // potencia media = A^2/2 → 10*log10(A^2/2) = 20*log10(A) - 10*log10(2)
      return render(440, 0.2, 0.45, 'auto').then(function (buf) {
        var m = medirBuffer(buf, 0.12);
        anotar('unidad ~0 dB de fader', Math.abs(m.rmsSuma - esperado) < 1.5, m.rmsSuma.toFixed(2) + ' vs ' + esperado.toFixed(2));
        return render(440, 0.2, 0.45, 'auto', function (mic) { mic.setGainDb(-6); }).then(function (buf2) {
          var m2 = medirBuffer(buf2, 0.12);
          anotar('fader -6 dB', Math.abs((m2.rmsSuma - m.rmsSuma) - (-6)) < 0.8, (m2.rmsSuma - m.rmsSuma).toFixed(2));
          return { base: m };
        });
      });
    }).then(function () {
      return render(440, 0.05, 0.45, 'auto', function (mic) {
        mic.setParam('gateThresholdDb', -12);
        mic.setParam('gateRangeDb', -80);
        mic.setParam('gateHysteresisDb', 1);
        mic.setParam('gateHoldMs', 0);
        mic.setParam('gateReleaseMs', 20);
      }).then(function (buf) {
        var m = medirBuffer(buf, 0.15);
        anotar('puerta cerrada', m.rmsSuma < -70, m.rmsSuma.toFixed(1));
      });
    }).then(function () {
      return Promise.all([
        render(100, 0.2, 0.45, 'auto', function (mic) { mic.setParam('hpfHz', 300); }),
        render(2000, 0.2, 0.45, 'auto', function (mic) { mic.setParam('hpfHz', 300); })
      ]).then(function (bufs) {
        var a = medirBuffer(bufs[0], 0.12).rmsSuma;
        var b = medirBuffer(bufs[1], 0.12).rmsSuma;
        anotar('pasaaltos atenúa graves', (b - a) > 12, (b - a).toFixed(1) + ' dB');
      });
    }).then(function () {
      return Promise.all([
        render(2000, 0.1, 0.45, 'auto', function (mic) { mic.setParam('presenceHz', 2000); mic.setParam('presenceGainDb', 0); mic.setParam('presenceQ', 2); }),
        render(2000, 0.1, 0.45, 'auto', function (mic) { mic.setParam('presenceHz', 2000); mic.setParam('presenceGainDb', 12); mic.setParam('presenceQ', 2); })
      ]).then(function (bufs) {
        var d = medirBuffer(bufs[1], 0.12).rmsSuma - medirBuffer(bufs[0], 0.12).rmsSuma;
        anotar('presencia +12 dB', d > 10 && d < 14, d.toFixed(2));
      });
    }).then(function () {
      return Promise.all([
        render(6000, 0.25, 0.45, 'auto', function (mic) { mic.setParam('deEssMaxDb', 0); }),
        render(6000, 0.25, 0.45, 'auto', function (mic) {
          mic.setParam('deEssFreqHz', 6000);
          mic.setParam('deEssThresholdDb', -50);
          mic.setParam('deEssMaxDb', 12);
          mic.setParam('deEssAttackMs', 0.5);
          mic.setParam('deEssReleaseMs', 30);
        })
      ]).then(function (bufs) {
        var d = medirBuffer(bufs[0], 0.16).rmsSuma - medirBuffer(bufs[1], 0.16).rmsSuma;
        anotar('de-esser corta la ese', d > 6, d.toFixed(2));
      });
    }).then(function () {
      function comp(mixOn) {
        return render(440, 0.6, 0.5, 'auto', function (mic) {
          mic.setParam('compThresholdDb', -30);
          mic.setParam('compRatio', mixOn ? 10 : 1);
          mic.setParam('compKneeDb', 0);
          mic.setParam('compAttackMs', 1);
          mic.setParam('compReleaseMs', 40);
          mic.setParam('compMakeupDb', 0);
          mic.setParam('compMix', 1);
        });
      }
      return Promise.all([comp(false), comp(true)]).then(function (bufs) {
        var d = medirBuffer(bufs[0], 0.16).rmsSuma - medirBuffer(bufs[1], 0.16).rmsSuma;
        anotar('compresor baja el pico sostenido', d > 8, d.toFixed(2));
      });
    }).then(function () {
      return render(440, 0.2, 0.4, 'auto', function (mic) { mic.setParam('pan', 1); }).then(function (buf) {
        var m = medirBuffer(buf, 0.1);
        anotar('pan +1 a la derecha', (m.rmsR - m.rmsL) > 20, 'L ' + m.rmsL.toFixed(1) + ' R ' + m.rmsR.toFixed(1));
        return render(440, 0.2, 0.4, 'ganancias', function (mic) { mic.setParam('pan', -1); });
      }).then(function (buf) {
        var m = medirBuffer(buf, 0.1);
        anotar('pan -1 sin StereoPanner', (m.rmsL - m.rmsR) > 20, 'L ' + m.rmsL.toFixed(1) + ' R ' + m.rmsR.toFixed(1));
      });
    }).then(function () {
      var ok = pruebas.every(function (p) { return p.ok; });
      return { ok: ok, pruebas: pruebas, parametros: PARAMETROS.slice() };
    }).catch(function (e) {
      anotar('excepción', false, e && e.stack ? e.stack : String(e));
      return { ok: false, pruebas: pruebas };
    });
  }


  function umbralEfectivo(estado, umbralReceta) {
    var v = umbralReceta;
    if (estado.bleed) v = v + 8;
    if (v > 0) v = 0;
    if (v < -90) v = -90;
    return v;
  }

  function sueloMedidor(db) {
    if (typeof db !== 'number' || !isFinite(db) || db < -80) return -80;
    return db;
  }

  function aplicarEscenaAMicro(estado, mic) {
    var sc = ESCENAS[estado.escenaId];
    if (!sc) return;
    var pan = mic._params.pan;
    Object.keys(sc.params).forEach(function (k) {
      if (k === 'pan') return;
      mic.setParam(k, sc.params[k]);
    });
    if (mic._params.pan !== pan) mic.setParam('pan', pan);
  }

  function engancharWorklet(estado, mic) {
    var nodo = new AudioWorkletNode(estado.ctx, 'lv-podcast-canal', {
      numberOfInputs: 1,
      numberOfOutputs: 1,
      outputChannelCount: [1],
      channelCount: 1,
      channelCountMode: 'explicit',
      channelInterpretation: 'speakers'
    });
    mic.nodo = nodo;
    fijarMono(nodo);
    nodo.port.onmessage = function (ev) {
      mic._med = ev.data || mic._med;
    };
    nodo.onprocessorerror = function () {
      mic._errorProcesador = true;
    };
    PARAMETROS.forEach(function (nombre) {
      if (nombre === 'pan') return;
      var p = nodo.parameters.get(nombre);
      if (!p) error('el procesador no expone «' + nombre + '».');
      var valor = nombre === 'gateThresholdDb' ? umbralEfectivo(estado, mic._params[nombre]) : mic._params[nombre];
      rampa(estado.ctx, p, valor, 0);
    });
    nodo.connect(mic.fader);
    mic.entrada = nodo;
    mic.latenciaMs = 2;
    montarPan(estado, mic, true);
    return mic;
  }

  function engancharProcesador(estado, mic) {
    if (estado.ctx._lvModo === 'script') return engancharScript(estado, mic);
    if (estado.ctx._lvModo === 'worklet') return engancharWorklet(estado, mic);
    error('el módulo de audio aún no está cargado.');
    return mic;
  }

  function prepararMicro(estado, id) {
    if (estado.cerrado) error('el motor está cerrado.');
    if (estado.micros.length >= 16) error('tope de 16 micros.');
    if (id == null) id = 'mic' + (estado.seq++);
    id = String(id);
    if (!id.trim()) error('el micro necesita un id.');
    if (estado.porId[id]) error('ya existe un micro «' + id + '».');
    var mic = fabricarMicro(estado, id);
    estado.micros.push(mic);
    estado.porId[id] = mic;
    return mic;
  }

  function crearMicro(estado, listo, id) {
    var mic = prepararMicro(estado, id);
    return listo.then(function () {
      if (estado.cerrado || !estado.porId[id]) return mic;
      engancharProcesador(estado, mic);
      return mic;
    });
  }

  function añadirMicroSync(estado, id) {
    if (estado.ctx._lvModo !== 'worklet' && estado.ctx._lvModo !== 'script') {
      error('addMic es síncrono solo después de await LVPodcastAudio.create().');
    }
    var mic = prepararMicro(estado, id);
    engancharProcesador(estado, mic);
    aplicarEscenaAMicro(estado, mic);
    return mic;
  }

  function vistaMicro(mic) {
    return {
      id: mic.id,
      input: mic.entrada,
      setGainDb: function (db) { return mic.setGainDb(db); },
      getGainDb: function () { return mic.getGainDb(); },
      setParam: function (nombre, valor) { return mic.setParam(nombre, valor); },
      getParams: function () { return mic.getParams(); },
      mute: function (activo) { return mic.setMute(activo); },
      solo: function (activo) { return mic.setSolo(activo); },
      setMute: function (activo) { return mic.setMute(activo); },
      setSolo: function (activo) { return mic.setSolo(activo); },
      getMute: function () { return mic.getMute(); },
      getSolo: function () { return mic.getSolo(); }
    };
  }

  function recorteEscena(estado) {
    var sc = ESCENAS[estado.escenaId];
    if (!sc) return 0;
    return sc.bedTrim;
  }

  function añadirCama(estado, id) {
    if (estado.cerrado) error('el motor está cerrado.');
    if (id == null) id = 'bed' + (estado.seq++);
    id = String(id);
    if (!id.trim()) error('la cama necesita un id.');
    if (estado.porCama[id]) error('ya existe una cama «' + id + '».');
    var ctx = estado.ctx;
    var input = ctx.createGain();
    var user = ctx.createGain();
    var trim = ctx.createGain();
    var duck = ctx.createGain();
    var medidor = ctx.createAnalyser();
    input.gain.value = 1;
    user.gain.value = 1;
    medidor.fftSize = 1024;
    medidor.smoothingTimeConstant = 0.4;
    input.connect(user);
    input.connect(medidor);
    user.connect(trim);
    trim.connect(duck);
    duck.connect(estado.master);
    var bed = {
      id: id,
      input: input,
      _user: user,
      _trim: trim,
      _duck: duck,
      _medidor: medidor,
      _gainDb: 0,
      _duckDb: null,
      _duckEnv: 0
    };
    bed.setGainDb = function (db) {
      if (typeof db !== 'number' || !isFinite(db)) error('setGainDb de la cama espera un número en dB.');
      if (db < -90) db = -90;
      if (db > 18) db = 18;
      bed._gainDb = db;
      rampa(ctx, user.gain, dbALineal(db), ctx.currentTime > 0 ? 0.012 : 0);
      return db;
    };
    bed.setDuckDb = function (db) {
      if (db == null) { bed._duckDb = null; return null; }
      if (typeof db !== 'number' || !isFinite(db)) error('setDuckDb espera null o un número de 0 a -40 dB.');
      if (db > 0) db = -db;
      if (db < -40) db = -40;
      if (db > 0) db = 0;
      bed._duckDb = db;
      return db;
    };
    rampa(ctx, trim.gain, dbALineal(recorteEscena(estado)), 0);
    estado.camas.push(bed);
    estado.porCama[id] = bed;
    return {
      id: id,
      input: input,
      setGainDb: function (db) { return bed.setGainDb(db); },
      setDuckDb: function (db) { return bed.setDuckDb(db); }
    };
  }

  function profundidadCama(estado, bed) {
    if (bed._duckDb != null) return bed._duckDb;
    var sc = ESCENAS[estado.escenaId];
    return sc ? sc.bedDuck : 0;
  }

  function actualizarCamas(estado) {
    var speech = sueloMedidor(rmsAnalizador(estado.analizadorVoz));
    estado.speechDb = speech;
    var habla = speech > -40;
    var ahora = estado.ctx.currentTime || 0;
    for (var i = 0; i < estado.camas.length; i++) {
      var bed = estado.camas[i];
      var meta = habla ? profundidadCama(estado, bed) : 0;
      var env = bed._duckEnv;
      var tau = meta < env ? 0.020 : 0.350;
      var k = 1 - Math.exp(-0.02 / tau);
      env = env + (meta - env) * k;
      if (Math.abs(env) < 0.05) env = 0;
      bed._duckEnv = env;
      var lin = dbALineal(env);
      if (ahora > 0) {
        try { bed._duck.gain.setTargetAtTime(lin, ahora, 0.008); } catch (e) {}
      } else {
        bed._duck.gain.value = lin;
      }
    }
  }

  function publicarMedidores(estado) {
    if (!estado.oyentes.length) return;
    var mics = {};
    var beds = {};
    var i, m, med, b;
    for (i = 0; i < estado.micros.length; i++) {
      m = estado.micros[i];
      med = m._med || {};
      mics[m.id] = {
        inDb: sueloMedidor(med.inDb),
        outDb: sueloMedidor(med.outRmsDb),
        gateOpen: (typeof med.puerta === 'number' && isFinite(med.puerta)) ? med.puerta : 0,
        deEssDb: (typeof med.deEssDb === 'number' && isFinite(med.deEssDb)) ? med.deEssDb : 0
      };
    }
    for (i = 0; i < estado.camas.length; i++) {
      b = estado.camas[i];
      beds[b.id] = { inDb: sueloMedidor(rmsAnalizador(b._medidor)), gainDb: b._gainDb };
    }
    var paquete = {
      mics: mics,
      beds: beds,
      masterDb: sueloMedidor(rmsAnalizador(estado.analizador)),
      speechDb: sueloMedidor(estado.speechDb)
    };
    for (i = 0; i < estado.oyentes.length; i++) {
      try { estado.oyentes[i](paquete); } catch (e) {}
    }
  }

  function fijarBleed(estado, activo) {
    estado.bleed = !!activo;
    for (var i = 0; i < estado.micros.length; i++) {
      var mic = estado.micros[i];
      if (!mic.nodo) continue;
      var p = mic.nodo.parameters.get('gateThresholdDb');
      if (p) rampa(estado.ctx, p, umbralEfectivo(estado, mic._params.gateThresholdDb), estado.ctx.currentTime > 0 ? 0.012 : 0);
    }
  }

  function aplicarRecorteCamas(estado) {
    var db = recorteEscena(estado);
    var lin = dbALineal(db);
    for (var i = 0; i < estado.camas.length; i++) {
      rampa(estado.ctx, estado.camas[i]._trim.gain, lin, estado.ctx.currentTime > 0 ? 0.02 : 0);
    }
  }

  function fijarEscena(estado, id) {
    var sc = ESCENAS[id];
    if (!sc || !sc.params) error('escena desconocida «' + id + '».');
    estado.escenaId = id;
    fijarBleed(estado, sc.bleed);
    estado.duck.profundidadDb = sc.crossDuck;
    estado.duck.activo = sc.crossDuck !== 0;
    for (var i = 0; i < estado.micros.length; i++) aplicarEscenaAMicro(estado, estado.micros[i]);
    aplicarRecorteCamas(estado);
    return id;
  }

  function soltarCamas(estado) {
    for (var i = 0; i < estado.camas.length; i++) {
      var b = estado.camas[i];
      try { b.input.disconnect(); } catch (e) {}
      try { b._user.disconnect(); } catch (e) {}
      try { b._trim.disconnect(); } catch (e) {}
      try { b._duck.disconnect(); } catch (e) {}
    }
    estado.camas = [];
    estado.porCama = {};
  }

  function crearEstudio(motor) {
    var estado = motor._estado;
    var studio = {
      scene: estado.escenaId,
      usingWorklet: estado.ctx._lvModo === 'worklet',
      master: {
        output: estado.monitor,
        gain: estado.master,
        connect: function (nodo) {
          if (!nodo || typeof nodo.connect !== 'function') error('master.connect espera un AudioNode.');
          estado.monitor.connect(nodo);
        }
      },
      addMic: function (id) {
        return vistaMicro(añadirMicroSync(estado, id));
      },
      addBed: function (id) {
        return añadirCama(estado, id);
      },
      setScene: function (id) {
        studio.scene = fijarEscena(estado, id);
        return studio.scene;
      },
      setBleedGuard: function (activo) {
        fijarBleed(estado, activo);
        return estado.bleed;
      },
      meters: function (cb) {
        if (typeof cb !== 'function') error('meters espera una función.');
        estado.oyentes.push(cb);
        return function () {
          estado.oyentes = estado.oyentes.filter(function (f) { return f !== cb; });
        };
      },
      destroy: function () {
        estado.cerrado = true;
        estado.oyentes = [];
        if (estado.reloj) clearInterval(estado.reloj);
        if (estado.relojMed) clearInterval(estado.relojMed);
        if (estado.grabacion) { try { estado.grabacion.abortar(); } catch (e) {} }
        estado.micros.slice().forEach(function (m) {
          try { quitarMicro(estado, m.id); } catch (e) {}
        });
        soltarCamas(estado);
        try { estado.monitor.disconnect(); } catch (e) {}
      }
    };
    return studio;
  }

  var fichaPublica = Object.freeze(FICHA.map(function (f) {
    return Object.freeze({
      nombre: f.nombre,
      unidad: f.unidad,
      util: Object.freeze(f.util.slice()),
      duro: Object.freeze(f.duro.slice()),
      defecto: f.defecto,
      nota: f.nota
    });
  }));

  function micConstraints(op) {
    op = op || {};
    return {
      echoCancellation: !!op.bleedGuard,
      noiseSuppression: false,
      autoGainControl: false,
      channelCount: 1
    };
  }

  function create(audioContext) {
    if (!audioContext || typeof audioContext.createGain !== 'function') error('create espera un AudioContext.');
    var motor = crear({ contexto: audioContext, salida: false });
    return motor.listo.then(function () { return crearEstudio(motor); });
  }

  var API = {
    version: '1.0.0',
    FICHA: fichaPublica,
    PARAMETROS: Object.freeze(PARAMETROS.slice()),
    scenes: Object.freeze(LISTA_ESCENAS.map(function (sc) {
      return Object.freeze({ id: sc.id, name: sc.name, blurb: sc.blurb });
    })),
    crear: crear,
    create: create,
    micConstraints: micConstraints,
    autoPrueba: autoPrueba,
    restriccionesMicro: function () { return micConstraints({ bleedGuard: true }); }
  };

  global.LVPodcastAudio = API;
})(typeof window !== 'undefined' ? window : globalThis);
