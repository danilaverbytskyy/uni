package com.example.list_temp.API

import com.example.list_temp.data.Student
import com.google.gson.annotations.SerializedName

class PostStudent (
    @SerializedName("action") val action: Int,
    @SerializedName("student") val student: Student
)