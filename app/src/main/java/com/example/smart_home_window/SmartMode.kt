package com.example.smart_home_window

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.NumberPicker
import android.widget.TextView

class SmartMode : AppCompatActivity()
{
    override fun onCreate(savedInstanceState: Bundle?)
    {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.smart_mode)
        // Mode Switching
        val manualButton = findViewById<Button>(R.id.manual_button_S)
        val automaticButton = findViewById<Button>(R.id.automatic_button_S)
        // Temperature Selection
        val desiredTempText = findViewById<TextView>(R.id.desired_temp_text)
        val tempPicker = findViewById<NumberPicker>(R.id.temp_input)
        var temp = 0
        val tempUnit = findViewById<NumberPicker>(R.id.temp_unit)
        val unit = arrayOf("°C", "°F")
        var cOrF = "°C"

        // Mode Switching
        manualButton.setOnClickListener {
            val intent = Intent(this, ManualMode::class.java)
            startActivity(intent)
        }
        automaticButton.setOnClickListener {
            val intent = Intent(this, AutomaticMode::class.java)
            startActivity(intent)
        }

        // Temperature Selection
        tempPicker.minValue = 15
        tempPicker.maxValue = 30
        tempUnit.displayedValues = unit
        tempUnit.minValue = 0
        tempUnit.maxValue = unit.size-1
        tempPicker.setOnValueChangedListener { numberPicker, oldVal, newVal ->
            temp = newVal
            desiredTempText.setText(temp.toString())
            //desiredTempText.text = String.format("Desired Temperature: %s", temp)
            desiredTempText.append(cOrF)
        }

        tempUnit.setOnValueChangedListener { numberPicker, oldVal, newVal ->
            //desiredTempText.setText(String.format("Desired Temperature: %s", temp))
            if (tempUnit.value == 0)
            {
                tempPicker.minValue = 15
                tempPicker.maxValue = 30
            }
            if (tempUnit.value == 1)
            {
                tempPicker.minValue = 59
                tempPicker.maxValue = 86
            }
            cOrF = unit[newVal]
            desiredTempText.setText(temp.toString())
            desiredTempText.append(cOrF)
        }
    }
}