package com.example.smart_home_window

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class AutomaticMode : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.automatic_mode)

        val manualButton = findViewById<Button>(R.id.manual_button_A)
        val smartButton = findViewById<Button>(R.id.smart_button_A)

        manualButton.setOnClickListener{
            val intent = Intent(this, ManualMode::class.java).also {
                startActivity(it)
            }
        }
        smartButton.setOnClickListener{
            val intent = Intent(this, SmartMode::class.java).also {
                startActivity(it)
            }
        }
    }
}