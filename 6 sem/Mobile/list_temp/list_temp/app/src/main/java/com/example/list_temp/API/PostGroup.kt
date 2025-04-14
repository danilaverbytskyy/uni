package com.example.list_temp.API

import com.example.list_temp.data.Group
import com.google.gson.annotations.SerializedName

class PostGroup (
    @SerializedName("action") val action: Int,
    @SerializedName("group") val group: Group
)