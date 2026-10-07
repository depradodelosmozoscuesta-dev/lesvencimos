package com.lesvc.audiocode

import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder

class AudioDecoder(
    private val sampleRate: Int = 44100
) {
    private val detector = ToneDetector(sampleRate)

    @Volatile
    private var recording = false

    fun stop() {
        recording = false
    }

    /**
     * Graba [durationMs] y devuelve la lista de nibbles detectados tras el precámbulo.
     */
    fun recordAndDecode(durationMs: Int = 12_000): List<Int>? {
        val channel = AudioFormat.CHANNEL_IN_MONO
        val encoding = AudioFormat.ENCODING_PCM_16BIT
        val minBuf = AudioRecord.getMinBufferSize(sampleRate, channel, encoding)
        if (minBuf <= 0) return null

        val recorder = AudioRecord(
            MediaRecorder.AudioSource.MIC,
            sampleRate,
            channel,
            encoding,
            maxOf(minBuf, sampleRate) * 2
        )
        if (recorder.state != AudioRecord.STATE_INITIALIZED) {
            recorder.release()
            return null
        }

        val totalSamples = sampleRate * durationMs / 1000
        val pcm = ShortArray(totalSamples)
        recording = true
        recorder.startRecording()
        try {
            var offset = 0
            val chunk = ShortArray(minBuf.coerceAtLeast(2048))
            while (recording && offset < totalSamples) {
                val n = recorder.read(chunk, 0, minOf(chunk.size, totalSamples - offset))
                if (n > 0) {
                    System.arraycopy(chunk, 0, pcm, offset, n)
                    offset += n
                } else if (n < 0) {
                    break
                }
            }
        } finally {
            try {
                recorder.stop()
            } catch (_: Exception) {
            }
            recorder.release()
            recording = false
        }

        return decodeSamples(pcm)
    }

    fun decodeSamples(pcm: ShortArray): List<Int>? {
        val symbolSamples = sampleRate * DualToneSets.SYMBOL_MS / 1000
        val stepSamples = sampleRate * (DualToneSets.SYMBOL_MS + DualToneSets.GAP_MS) / 1000
        if (pcm.size < symbolSamples * 6) return null

        // Buscar precámbulo deslizante
        var start = -1
        val hop = symbolSamples / 4
        var i = 0
        while (i + symbolSamples <= pcm.size) {
            if (detector.isPreamble(pcm, i, symbolSamples)) {
                // Avanzar past PREAMBLE_COUNT symbols
                var p = i
                var count = 0
                while (p + symbolSamples <= pcm.size && count < DualToneSets.PREAMBLE_COUNT) {
                    if (detector.isPreamble(pcm, p, symbolSamples)) {
                        count++
                        p += stepSamples
                    } else {
                        // tolerancia: a veces el gap desplaza
                        p += hop
                    }
                }
                if (count >= DualToneSets.PREAMBLE_COUNT - 1) {
                    start = p
                    break
                }
            }
            i += hop
        }
        if (start < 0) {
            // Fallback: intentar desde el primer tono de datos detectable
            start = 0
        }

        val nibbles = mutableListOf<Int>()
        var pos = start
        var miss = 0
        while (pos + symbolSamples <= pcm.size) {
            val n = detector.detectNibble(pcm, pos, symbolSamples)
            if (n != null) {
                nibbles.add(n)
                miss = 0
                pos += stepSamples
            } else {
                miss++
                pos += hop
                if (nibbles.isNotEmpty() && miss > 8) break
            }
        }
        return if (nibbles.size >= 14) nibbles else null
    }
}
