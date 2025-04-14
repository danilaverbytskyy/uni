package com.example.list_temp.data

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey
import com.google.gson.annotations.SerializedName
import java.util.Date
import java.util.UUID

@Entity(tableName = "students",
    indices=[Index("id"), Index("group_id","id")],
    foreignKeys=[
        ForeignKey(
            entity = Group::class,
            parentColumns = ["id"],
            childColumns = ["group_id"],
            onDelete = ForeignKey.CASCADE
        )
    ])
data class Student(
    @SerializedName("id") @PrimaryKey val id: UUID = UUID.randomUUID(),
    @SerializedName("lastName") var lastName: String="",
    @SerializedName("firstName") var firstName: String="",
    @SerializedName("middleName") var middleName: String="",
    @SerializedName("birthDate") @ColumnInfo(name = "birth_date") var birthDate: Date = Date(),
    @SerializedName("groupId") @ColumnInfo(name = "group_id") var groupID: UUID?=null,
    @SerializedName("phone") var phone: String="",
    @SerializedName("sex") var sex : Int=0
){
    val shortName
        get()=lastName +
            (if(firstName.length>0) {" ${firstName.subSequence(0,1)}. "} else "") +
            (if(middleName.length>0) {" ${middleName.subSequence(0,1)}. "} else "")
}
