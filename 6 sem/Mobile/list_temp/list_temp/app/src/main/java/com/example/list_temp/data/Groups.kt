package com.example.list_temp.data

import com.google.gson.annotations.SerializedName

class Groups {
    @SerializedName("items") lateinit var items: List<Group>
}