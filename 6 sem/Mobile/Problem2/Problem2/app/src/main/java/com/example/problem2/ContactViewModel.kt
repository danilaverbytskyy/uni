package com.example.problem2

import androidx.lifecycle.ViewModel

class ContactViewModel : ViewModel() {
    private val contactList = mutableListOf(
        Contact("Иван", "Иванович", "Иванов", "1234567890"),
        Contact("Данила", "Алексеевич", "Вербицкий", "79782263905"),
        Contact("Эмилия", "Алексеевна", "Постушная", "79782263905")
    )

    private var currentIndex = 0

    val currentContact: Contact get() = contactList[currentIndex]
    val currentContactText: String get() = contactList[currentIndex].sName+" "+contactList[currentIndex].name[0]+"."+
            contactList[currentIndex].mName[0]+"."

    fun moveToNext() {
        currentIndex = (currentIndex + 1) % contactList.size
    }

    fun moveToPrev() {
        currentIndex = (contactList.size + currentIndex - 1) % contactList.size
    }

    fun updateContact(contact: Contact) {
        contactList[currentIndex] = contact
    }
}