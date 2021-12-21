package com.example.smart_home_window

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.SeekBar
import android.widget.TextView
import android.widget.Button
import android.widget.Toast


class ManualMode : AppCompatActivity()
{
    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.preferences, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when (item.itemId) {
            R.id.settings -> Toast.makeText(this, "Testing", Toast.LENGTH_SHORT).show()
        }
        return super.onOptionsItemSelected(item)
    }

    override fun onCreate(savedInstanceState: Bundle?)
    {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.manual_mode)

        val smartButton = findViewById<Button>(R.id.smart_button_M)
        val automaticButton = findViewById<Button>(R.id.automatic_button_M)

        smartButton.setOnClickListener{
            val intent = Intent(this, SmartMode::class.java).also {
                startActivity(it)
            }
        }
        automaticButton.setOnClickListener{
            val intent = Intent(this, AutomaticMode::class.java).also {
                startActivity(it)
            }
        }

        val blindsSeekBar = findViewById<SeekBar>(R.id.blinds_seekbar)
        val blindsVal = findViewById<TextView>(R.id.blinds_val)
        val windowSeekBar = findViewById<SeekBar>(R.id.window_seekbar)
        val windowVal = findViewById<TextView>(R.id.window_val)
        var blindsLevel: Int
        var windowLevel: Int
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
