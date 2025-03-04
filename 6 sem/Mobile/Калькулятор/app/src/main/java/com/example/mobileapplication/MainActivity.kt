package com.example.mobileapplication

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private var firstNumber: Double = 0.0
    private var operation: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val inputField: EditText = findViewById(R.id.numberInputField)
        val signField: TextView = findViewById(R.id.signField)
        val resultField: TextView = findViewById(R.id.resultField)


        val btnAC: Button = findViewById(R.id.buttonAC)
        val btnEquals: Button = findViewById(R.id.buttonEquals)

        val numberButtons = listOf(
            R.id.buttonZero, R.id.buttonOne, R.id.buttonTwo, R.id.buttonThree,
            R.id.buttonFour, R.id.buttonFive, R.id.buttonSix, R.id.buttonSeven,
            R.id.buttonEight, R.id.buttonNine
        )

        numberButtons.forEachIndexed { index, buttonId ->
            findViewById<Button>(buttonId).setOnClickListener {
                inputField.append(index.toString())
            }
        }

        findViewById<Button>(R.id.buttonDot).setOnClickListener {
            if (!inputField.text.contains(".")) {
                inputField.append(".")
            }
        }

        findViewById<Button>(R.id.buttonPlus).setOnClickListener { setOperation(inputField, signField, resultField, "+") }
        findViewById<Button>(R.id.buttonMinus).setOnClickListener { setOperation(inputField, signField, resultField, "-") }
        findViewById<Button>(R.id.buttonMultiple).setOnClickListener { setOperation(inputField, signField, resultField, "*") }
        findViewById<Button>(R.id.buttonDivide).setOnClickListener { setOperation(inputField, signField, resultField, "/") }

        btnAC.setOnClickListener {
            inputField.text.clear()
            resultField.text = ""
            signField.text = ""
            firstNumber = 0.0
            operation = ""
        }

        btnEquals.setOnClickListener {
            if (operation.isNotEmpty() && inputField.text.isNotEmpty()) {
                val secondNumber = inputField.text.toString().toDouble()
                val result = calculate(firstNumber, secondNumber, operation)
                resultField.text = if (operation == "/" && secondNumber == 0.0) "Деление на 0" else result.toString()
                inputField.text.clear()
                signField.text = ""
                operation = ""
            }
        }
    }

    private fun setOperation(inputField: EditText, signField: TextView, resultField: TextView, op: String) {
        if (inputField.text.isNotEmpty()) {
            firstNumber = inputField.text.toString().toDouble()
            operation = op
            signField.text = op
            resultField.text = firstNumber.toString()
            inputField.text.clear()
        }
    }

    private fun calculate(a: Double, b: Double, op: String): Double {
        return when (op) {
            "+" -> a + b
            "-" -> a - b
            "*" -> a * b
            "/" -> if (b != 0.0) a / b else Double.NaN
            else -> 0.0
        }
    }
}
