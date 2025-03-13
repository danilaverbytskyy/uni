package com.example.problem2

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity2 : AppCompatActivity() {
    private lateinit var etName: EditText
    private lateinit var etMiddleName: EditText
    private lateinit var etSurname: EditText
    private lateinit var etPhone: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        etName = findViewById(R.id.etName)
        etMiddleName = findViewById(R.id.etMName)
        etSurname = findViewById(R.id.etSName)
        etPhone = findViewById(R.id.etPhone)

        val name = intent.getStringExtra("name") ?: ""
        val middleName = intent.getStringExtra("middleName") ?: ""
        val surname = intent.getStringExtra("surname") ?: ""
        val phone = intent.getStringExtra("phone") ?: ""

        etName.setText(name)
        etMiddleName.setText(middleName)
        etSurname.setText(surname)
        etPhone.setText(phone)
    }
    override fun onBackPressed() {

        if (validateFields()) {
            val name = etName.text.toString()
            val middleName = etMiddleName.text.toString()
            val surname = etSurname.text.toString()
            val phone = etPhone.text.toString()

            val resultIntent = Intent()
            resultIntent.putExtra("name", name)
            resultIntent.putExtra("middleName", middleName)
            resultIntent.putExtra("surname", surname)
            resultIntent.putExtra("phone", phone)
            super.onBackPressedDispatcher.onBackPressed()
            setResult(RESULT_OK, resultIntent)
            finish()
        } else {
            showError("Пожалуйста, заполните все поля корректно")
        }
    }

    private fun validateFields(): Boolean {
        val name = etName.text.toString()
        val middleName = etMiddleName.text.toString()
        val surname = etSurname.text.toString()
        val phone = etPhone.text.toString()

        if (name.isEmpty() || middleName.isEmpty() || surname.isEmpty() || phone.isEmpty()) {
            return false
        }
        if (!phone.matches(Regex("\\d+"))) {
            return false
        }
        return true
    }

    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}