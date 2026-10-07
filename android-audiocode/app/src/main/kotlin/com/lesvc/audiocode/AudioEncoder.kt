package com.lesvc.audiocode

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import kotlin.math.PI
import kotlin.math.sin

class AudioEncoder(
    private val sampleRate: Int = 44100
) {
    @Volatile
    private var playing = false

    fun stop() {
        playing = false
    }

    fun playNibbles(nibbles: List<Int>) {
        playing = true
        val symbolSamples = sampleRate * DualToneSets.SYMBOL_MS / 1000
        val gapSamples = sampleRate * DualToneSets.GAP_MS / 1000

        val chunks = ArrayList<ShortArray>()
        // Precámbulo
        repeat(DualToneSets.PREAMBLE_COUNT) {
            chunks.add(dualTone(DualToneSets.PREAMBLE_A, DualToneSets.PREAMBLE_B, symbolSamples))
            chunks.add(silence(gapSamples))
        }
        // Datos
        for (n in nibbles) {
            if (!playing) break
            val (lo, hi) = DualToneSets.freqsForNibble(n)
            chunks.add(dualTone(lo, hi, symbolSamples))
            chunks.add(silence(gapSamples))
        }

        val total = chunks.sumOf { it.size }
        val pcm = ShortArray(total)
        var pos = 0
        for (c in chunks) {
            System.arraycopy(c, 0, pcm, pos, c.size)
            pos += c.size
        }

        val minBuf = AudioTrack.getMinBufferSize(
            sampleRate,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT
        )
        val track = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(sampleRate)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()
            )
            .setBufferSizeInBytes(maxOf(minBuf, pcm.size * 2))
            .setTransferMode(AudioTrack.MODE_STATIC)
            .build()

        try {
            track.write(pcm, 0, pcm.size)
            track.play()
            val durationMs = (pcm.size * 1000L) / sampleRate + 50
            var waited = 0L
            while (playing && waited < durationMs) {
                Thread.sleep(40)
                waited += 40
            }
        } finally {
            try {
                track.stop()
            } catch (_: Exception) {
            }
            track.release()
            playing = false
        }
    }

    private fun silence(n: Int): ShortArray = ShortArray(n)

    private fun dualTone(f1: Float, f2: Float, n: Int): ShortArray {
        val out = ShortArray(n)
        val amp = 0.32 // evitar clipping al sumar dos senos
        val fade = minOf(n / 10, sampleRate / 100) // ~10 ms fade
        for (i in 0 until n) {
            val t = i.toDouble() / sampleRate
            var s = amp * (sin(2.0 * PI * f1 * t) + sin(2.0 * PI * f2 * t))
            // Envelope suave
            val env = when {
                i < fade -> i.toDouble() / fade
                i > n - fade -> (n - i).toDouble() / fade
                else -> 1.0
            }
            s *= env
            out[i] = (s * Short.MAX_VALUE).toInt().coerceIn(Short.MIN_VALUE.toInt(), Short.MAX_VALUE.toInt()).toShort()
        }
        return out
    }
}
