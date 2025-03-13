package com.example.problem2

import androidx.lifecycle.ViewModel

class ContactViewModel : ViewModel() {
    val contactList: MutableList<Contact> = mutableListOf(
        Contact("Иван", "Иванович", "Иванов", "12345678901"),
        Contact("Данила", "Алексеевич", "Вербицкий", "78423698756"),
        Contact("Эмилия", "Павловна", "Постушная", "76995345979"),
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

    fun addContact(contact: Contact) {
        currentIndex=0
        contactList.addFirst(contact)
    }
}