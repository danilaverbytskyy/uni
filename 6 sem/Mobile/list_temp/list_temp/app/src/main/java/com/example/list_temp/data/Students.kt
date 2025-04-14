package com.example.list_temp.data

import com.google.gson.annotations.SerializedName

class Students {
    @SerializedName("items") lateinit var items: List<Student>
}