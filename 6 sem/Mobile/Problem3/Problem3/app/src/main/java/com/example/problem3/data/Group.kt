package com.example.problem3.data

import java.util.UUID

data class Group(
    val id: UUID = UUID.randomUUID(),
    val name: String="",
    var facultyID: UUID?=null
)
