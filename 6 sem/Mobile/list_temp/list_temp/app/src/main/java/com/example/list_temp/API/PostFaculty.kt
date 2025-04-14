package com.example.list_temp.API

import com.example.list_temp.data.Faculty
import com.google.gson.annotations.SerializedName

class PostFaculty (
    @SerializedName("action") val action: Int,
    @SerializedName("faculty") val faculty: Faculty
)