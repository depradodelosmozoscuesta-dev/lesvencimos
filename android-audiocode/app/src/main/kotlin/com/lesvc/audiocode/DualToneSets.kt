package com.lesvc.audiocode

/**
 * 16 símbolos (nibble 0..15) = par de tonos (baja × alta), estilo DTMF ampliado.
 * Precámara: 1800+2100 Hz repetido para sincronizar.
 */
object DualToneSets {
    val LOW = floatArrayOf(697f, 770f, 852f, 941f)
    val HIGH = floatArrayOf(1209f, 1336f, 1477f, 1633f)

    const val PREAMBLE_A = 1800f
    const val PREAMBLE_B = 2100f

    /** Duración de cada símbolo en ms (tono activo). */
    const val SYMBOL_MS = 90
    /** Silencio entre símbolos en ms. */
    const val GAP_MS = 30
    /** Nº de símbolos de precámbulo al inicio. */
    const val PREAMBLE_COUNT = 4

    fun freqsForNibble(nibble: Int): Pair<Float, Float> {
        val n = nibble and 0x0F
        return LOW[n / 4] to HIGH[n % 4]
    }

    fun nibbleForLowHigh(lowIdx: Int, highIdx: Int): Int {
        if (lowIdx !in 0..3 || highIdx !in 0..3) return -1
        return lowIdx * 4 + highIdx
    }

    fun allTargetFreqs(): FloatArray {
        return floatArrayOf(
            LOW[0], LOW[1], LOW[2], LOW[3],
            HIGH[0], HIGH[1], HIGH[2], HIGH[3],
            PREAMBLE_A, PREAMBLE_B
        )
    }
}
