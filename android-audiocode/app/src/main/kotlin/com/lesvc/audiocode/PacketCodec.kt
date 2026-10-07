package com.lesvc.audiocode

object PacketCodec {
    const val VERSION = 1
    const val TYPE_TEXT = 1

    fun encodeTextWithPriority(text: String, priority: Int = 0): List<Int> {
        val payload = text.toByteArray(Charsets.UTF_8)

        val header = ByteArray(7)
        header[0] = VERSION.toByte()
        header[1] = TYPE_TEXT.toByte()
        header[2] = priority.toByte()
        header[3] = ((payload.size ushr 8) and 0xFF).toByte()
        header[4] = (payload.size and 0xFF).toByte()

        val crc = Crc16.compute(payload)
        header[5] = ((crc ushr 8) and 0xFF).toByte()
        header[6] = (crc and 0xFF).toByte()

        val packet = ByteArray(header.size + payload.size)
        System.arraycopy(header, 0, packet, 0, header.size)
        System.arraycopy(payload, 0, packet, header.size, payload.size)

        val nibbles = mutableListOf<Int>()
        for (b in packet) {
            val hi = (b.toInt() ushr 4) and 0x0F
            val lo = b.toInt() and 0x0F
            nibbles.add(hi)
            nibbles.add(lo)
        }
        return nibbles
    }

    fun decodeTextWithPriority(nibbles: List<Int>): DecodedPacket? {
        if (nibbles.size < 14) return null

        val bytes = ByteArray(nibbles.size / 2)
        var idx = 0
        for (i in nibbles.indices step 2) {
            if (i + 1 >= nibbles.size) break
            val hi = nibbles[i]
            val lo = nibbles[i + 1]
            bytes[idx++] = ((hi shl 4) or lo).toByte()
        }

        if (idx < 7) return null

        val version = bytes[0].toInt() and 0xFF
        val type = bytes[1].toInt() and 0xFF
        val priority = bytes[2].toInt() and 0xFF
        val length = ((bytes[3].toInt() and 0xFF) shl 8) or (bytes[4].toInt() and 0xFF)
        val crc = ((bytes[5].toInt() and 0xFF) shl 8) or (bytes[6].toInt() and 0xFF)

        val payloadStart = 7
        val payloadEnd = payloadStart + length
        if (payloadEnd > idx) return null

        val payload = bytes.copyOfRange(payloadStart, payloadEnd)
        val expectedCrc = Crc16.compute(payload)
        if (expectedCrc != crc) return null

        if (version != VERSION || type != TYPE_TEXT) return null

        return DecodedPacket(
            text = payload.toString(Charsets.UTF_8),
            priority = priority
        )
    }
}

data class DecodedPacket(
    val text: String,
    val priority: Int
)
