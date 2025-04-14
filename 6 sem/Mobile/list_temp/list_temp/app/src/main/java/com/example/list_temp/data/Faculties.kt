package com.example.list_temp.data

import com.google.gson.annotations.SerializedName

class Faculties {
    @SerializedName("items") lateinit var items: List<Faculty>
}