package com.lesvc.audiocode

object Crc16 {
    fun compute(data: ByteArray): Int {
        var crc = 0xFFFF
        for (b in data) {
            crc = crc xor (b.toInt() and 0xFF)
            for (i in 0 until 8) {
                val lsb = crc and 1
                crc = crc ushr 1
                if (lsb != 0) crc = crc xor 0xA001
            }
        }
        return crc and 0xFFFF
    }
}
