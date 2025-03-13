package com.example.problem3.repository

import androidx.lifecycle.MutableLiveData
import com.example.problem3.data.Faculty
import com.example.problem3.data.ListOfFaculty

class AppRepository {
    companion object{
        private var INSTANCE:AppRepository?=null
        fun getInstance():AppRepository{
            if(INSTANCE==null){
                INSTANCE=AppRepository()
            }
            return INSTANCE ?:
            throw IllegalArgumentException("Repository is not initialized")
        }
    }
}
var listOfFaculty:MutableLiveData<ListOfFaculty?> = MutableLiveData()
var faculty:MutableLiveData<Faculty?> = MutableLiveData()
fun addFaculty(faculty: Faculty){
    val listTmp=(listOfFaculty.value ?: ListOfFaculty()).apply{
        items.add(faculty)
    }
    listOfFaculty.postValue(listTmp)
    setCurrentFaculty(faculty)
}
fun getFacultyPosition(faculty: Faculty):Int= listOfFaculty.value?.items?.indexOfFirst {
    it.id==faculty.id} ?: -1
fun getFacultyPosition()= getFacultyPosition(faculty.value?:Faculty())
fun setCurrentFaculty(position:Int){
    if (listOfFaculty.value==null || position<0 ||
        (listOfFaculty.value?.items?.size!!<=position))
        return
    setCurrentFaculty(listOfFaculty.value?.items!![position])
}
fun setCurrentFaculty(_faculty:Faculty){
    faculty.postValue(_faculty)
}
fun updateFaculty(faculty: Faculty){
    val position= getFacultyPosition(faculty)
    if (position<0) addFaculty(faculty)
    else{
        val listTmp= listOfFaculty.value!!
        listTmp.items[position]=faculty
        listOfFaculty.postValue(listTmp)
    }
}
fun deleteFaculty(faculty: Faculty){
    var listTmp= listOfFaculty.value!!
    if (listTmp.items.remove(faculty)){
        listOfFaculty.postValue(listTmp)
    }
    setCurrentFaculty(0)
}