package com.example.list_temp.repository

import androidx.lifecycle.LiveData
import com.example.list_temp.data.Faculty
import com.example.list_temp.data.Group
import com.example.list_temp.data.Student
import kotlinx.coroutines.flow.Flow
import java.util.UUID

interface DBRepository {
    fun getFaculty(): Flow<List<Faculty>>
    suspend fun insertFaculty(faculty: Faculty)
    suspend fun updateFaculty(faculty: Faculty)
    suspend fun insertAllFaculty(facultyList:List<Faculty>)
    suspend fun deleteFaculty(faculty: Faculty)
    suspend fun deleteAllFaculty()

    fun getAllGroups():Flow<List<Group>>
    fun getFacultyGroups(facultyID: UUID):Flow<List<Group>>
    suspend fun insertGroup(group: Group)
    suspend fun deleteGroup(group: Group)
    suspend fun deleteAllGroups()

    fun getAllStudents():Flow<List<Student>>
    fun getGroupStudents(groupID:UUID):Flow<List<Student>>
    suspend fun insertStudent(student:Student)
    suspend fun deleteStudent(student: Student)
    suspend fun deleteAllStudents()

    fun updateFaculty(faculty: Faculty) {
        addFaculty(faculty)
    }

    fun deleteFaculty(faculty: Faculty) {
        myCoroutineScope.launch {
            listDB.deleteFaculty(faculty)
            setCurrentFaculty(0)
        }
    }

    var listOfStudent: LiveData<List<Student>> = listDB.getAllStudents().asLiveData()
    fun addStudent(student: Student) {
        myCoroutineScope.launch {
            listDB.deleteFaculty(faculty)
            setCurrentStudent(student)
        }
    }
}