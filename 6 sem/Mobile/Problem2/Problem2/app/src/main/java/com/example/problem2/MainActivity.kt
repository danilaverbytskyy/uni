package com.example.problem2

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider

class MainActivity : AppCompatActivity() {
    private lateinit var btnAdd: Button
    private lateinit var btnEdit: Button
    private lateinit var btnNext: ImageButton
    private lateinit var btnPrev: ImageButton
    private lateinit var contactTextView: TextView

    private val contactsViewModel: ContactViewModel by lazy {
        ViewModelProvider(this).get(ContactViewModel::class.java)
    }

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        btnAdd = findViewById(R.id.bAdd)
        btnEdit = findViewById(R.id.bEdit)
        btnPrev = findViewById(R.id.ibPrev)
        btnNext = findViewById(R.id.ibNext)
        contactTextView = findViewById(R.id.tvContact)

        updateContact()

        btnAdd.setOnClickListener {
            val intent = Intent(this, MainActivity2::class.java)
            resultLauncher.launch(intent)
        }

        btnEdit.setOnClickListener {
            val intent = Intent(this, MainActivity2::class.java)
            intent.putExtra("name", contactsViewModel.currentContact.name)
            intent.putExtra("middleName", contactsViewModel.currentContact.mName)
            intent.putExtra("surname", contactsViewModel.currentContact.sName)
            intent.putExtra("phone", contactsViewModel.currentContact.number)
            resultLauncher.launch(intent)
        }

        btnNext.setOnClickListener {
            contactsViewModel.moveToNext()
            updateContact()
        }

        btnPrev.setOnClickListener {
            contactsViewModel.moveToPrev()
            updateContact()
        }
    }

    private val resultLauncher: ActivityResultLauncher<Intent> =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == Activity.RESULT_OK) {
                val data: Intent? = result.data
                val name = data?.getStringExtra("name") ?: ""
                val middleName = data?.getStringExtra("middleName") ?: ""
                val surname = data?.getStringExtra("surname") ?: ""
                val phone = data?.getStringExtra("phone") ?: ""

                val updatedContact = Contact(name, middleName, surname, phone)
                contactsViewModel.updateContact(updatedContact)
                updateContact()
            }
        }

    private fun updateContact() {
        contactTextView.text = contactsViewModel.currentContactText
    }
}