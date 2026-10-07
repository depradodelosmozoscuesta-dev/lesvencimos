package com.lesvc.audiocode

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : AppCompatActivity() {

    private lateinit var messageEdit: EditText
    private lateinit var priorityEdit: EditText
    private lateinit var encodeButton: Button
    private lateinit var recordButton: Button
    private lateinit var resultText: TextView

    private val encoder = AudioEncoder()
    private val decoder = AudioDecoder()
    private val scope = CoroutineScope(Dispatchers.Main + Job())
    private var busy = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        messageEdit = findViewById(R.id.messageEdit)
        priorityEdit = findViewById(R.id.priorityEdit)
        encodeButton = findViewById(R.id.encodeButton)
        recordButton = findViewById(R.id.recordButton)
        resultText = findViewById(R.id.resultText)

        encodeButton.setOnClickListener { onEncode() }
        recordButton.setOnClickListener { onRecord() }
    }

    private fun onEncode() {
        if (busy) {
            Toast.makeText(this, "Espera a que termine…", Toast.LENGTH_SHORT).show()
            return
        }
        val text = messageEdit.text?.toString()?.trim().orEmpty()
        if (text.isEmpty()) {
            Toast.makeText(this, "Escribe un mensaje", Toast.LENGTH_SHORT).show()
            return
        }
        val priority = priorityEdit.text?.toString()?.toIntOrNull() ?: 0
        val nibbles = PacketCodec.encodeTextWithPriority(text, priority.coerceIn(0, 255))
        setBusy(true)
        resultText.text = "Reproduciendo ${nibbles.size} nibbles…"
        scope.launch {
            withContext(Dispatchers.IO) {
                encoder.playNibbles(nibbles)
            }
            resultText.text = "Reproducido.\nMensaje: \"$text\"\nPrioridad: $priority\nNibbles: ${nibbles.size}"
            setBusy(false)
        }
    }

    private fun onRecord() {
        if (busy) {
            Toast.makeText(this, "Espera a que termine…", Toast.LENGTH_SHORT).show()
            return
        }
        if (!ensureMicPermission()) return
        setBusy(true)
        resultText.text = "Escuchando 12 s… acerca el otro móvil o el altavoz."
        scope.launch {
            val nibbles = withContext(Dispatchers.IO) {
                decoder.recordAndDecode(12_000)
            }
            if (nibbles == null) {
                resultText.text = "Resultado: no se detectó trama válida.\nPrueba más cerca, sube volumen, menos ruido."
            } else {
                val decoded = PacketCodec.decodeTextWithPriority(nibbles)
                if (decoded == null) {
                    resultText.text = "Resultado: tonos oídos (${nibbles.size} nibbles) pero CRC/paquete inválido.\n${nibbles.take(40)}"
                } else {
                    resultText.text = "Resultado:\n\"${decoded.text}\"\nPrioridad: ${decoded.priority}"
                }
            }
            setBusy(false)
        }
    }

    private fun setBusy(v: Boolean) {
        busy = v
        encodeButton.isEnabled = !v
        recordButton.isEnabled = !v
    }

    private fun ensureMicPermission(): Boolean {
        val ok = ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) ==
            PackageManager.PERMISSION_GRANTED
        if (ok) return true
        ActivityCompat.requestPermissions(
            this,
            arrayOf(Manifest.permission.RECORD_AUDIO),
            REQ_MIC
        )
        Toast.makeText(this, "Concede permiso de micrófono y pulsa de nuevo", Toast.LENGTH_LONG).show()
        return false
    }

    override fun onDestroy() {
        encoder.stop()
        decoder.stop()
        super.onDestroy()
    }

    companion object {
        private const val REQ_MIC = 1001
    }
}
