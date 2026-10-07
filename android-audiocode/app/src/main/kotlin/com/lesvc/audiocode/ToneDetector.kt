package com.lesvc.audiocode

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sqrt

class ToneDetector(private val sampleRate: Int) {

    fun goertzelMagnitude(samples: ShortArray, offset: Int, length: Int, freq: Float): Double {
        if (length <= 0 || offset < 0 || offset + length > samples.size) return 0.0
        val k = (0.5 + length * freq / sampleRate).toInt()
        val w = (2.0 * PI * k) / length
        val cosine = cos(w)
        val coeff = 2.0 * cosine
        var s0 = 0.0
        var s1 = 0.0
        var s2 = 0.0
        val end = offset + length
        for (i in offset until end) {
            s0 = samples[i].toDouble() + coeff * s1 - s2
            s2 = s1
            s1 = s0
        }
        val real = s1 - s2 * cosine
        val imag = s2 * Math.sin(w)
        return sqrt(real * real + imag * imag) / length
    }

    fun bestLowHigh(samples: ShortArray, offset: Int, length: Int): Pair<Int, Int>? {
        var bestLow = -1
        var bestLowMag = 0.0
        DualToneSets.LOW.forEachIndexed { idx, f ->
            val m = goertzelMagnitude(samples, offset, length, f)
            if (m > bestLowMag) {
                bestLowMag = m
                bestLow = idx
            }
        }
        var bestHigh = -1
        var bestHighMag = 0.0
        DualToneSets.HIGH.forEachIndexed { idx, f ->
            val m = goertzelMagnitude(samples, offset, length, f)
            if (m > bestHighMag) {
                bestHighMag = m
                bestHigh = idx
            }
        }
        // Umbral relativo al ruido: ambos tonos deben estar presentes
        val floor = 8.0
        if (bestLowMag < floor || bestHighMag < floor) return null
        return bestLow to bestHigh
    }

    fun isPreamble(samples: ShortArray, offset: Int, length: Int): Boolean {
        val a = goertzelMagnitude(samples, offset, length, DualToneSets.PREAMBLE_A)
        val b = goertzelMagnitude(samples, offset, length, DualToneSets.PREAMBLE_B)
        return a > 8.0 && b > 8.0
    }

    fun detectNibble(samples: ShortArray, offset: Int, length: Int): Int? {
        val pair = bestLowHigh(samples, offset, length) ?: return null
        val n = DualToneSets.nibbleForLowHigh(pair.first, pair.second)
        return if (n in 0..15) n else null
    }
}
