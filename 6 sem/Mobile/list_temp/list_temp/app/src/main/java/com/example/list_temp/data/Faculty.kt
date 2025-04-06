package com.example.list_temp.data

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey
import java.util.UUID

@Entity(
    indices = [Index("id")]
)
data class Faculty(
    @PrimaryKey val id : UUID = UUID.randomUUID(),
    @ColumnInfo (name = "faculty_name") var name: String = ""
)
