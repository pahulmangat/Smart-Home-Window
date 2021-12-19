package com.example.smart_home_window

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.SeekBar
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.manual_mode)

        val blindsSeekBar = findViewById<SeekBar>(R.id.blinds_seekbar)
        val blindsVal = findViewById<TextView>(R.id.blinds_val)
        var blindsLevel = 0
        val windowSeekBar = findViewById<SeekBar>(R.id.window_seekbar)
        val windowVal = findViewById<TextView>(R.id.window_val)
        var windowLevel = 0
        val percent = "%"

        blindsSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                blindsLevel = progress*10
                (blindsLevel.toString() + percent).also { blindsVal.text = it }
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }
        })
        windowSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                windowLevel = progress*10
                (windowLevel.toString() + percent).also { windowVal.text = it }
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }
        })
    }
}