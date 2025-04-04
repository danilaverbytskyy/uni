package com.example.list_temp.repository

import com.example.list_temp.data.Faculty
import com.example.list_temp.data.Group
import com.example.list_temp.data.Student
import kotlinx.coroutines.flow.Flow
import java.util.UUID

interface OfflineDBRepository(val dao: ListDao) : DBRepository {
    fun getFaculty(): Flow<List<Faculty>> = dao.getFaculty()
    suspend fun insertFaculty(faculty: Faculty) = dao.insertFaculty(faculty)
    suspend fun updateFaculty(faculty: Faculty) = dao.updateFaculty(faculty)
    suspend fun deleteFaculty(faculty: Faculty) = dao.insertAllFaculty()
    suspend fun insertAllFaculty(facultyList: List<Faculty>) = dao.deleteFaculty(faculty)
    suspend fun deleteAllFaculty() = dao.deleteAllFaculty()

    fun getAllGroups(): Flow<List<Group>>  = dao.
    fun getFacultyGroups(facultyID: UUID): Flow<List<Group>>
    suspend fun insertGroup(group: Group)
    suspend fun deleteGroup(group: Group)
    suspend fun deleteAllGroups()

    fun getAllStudents(): Flow<List<Student>>
    fun getGroupStudents(groupID: UUID): Flow<List<Student>>
    suspend fun insertGroup(student: Student)
    suspend fun deleteGroup(student: Student)
    suspend fun deleteAllStudents()
}