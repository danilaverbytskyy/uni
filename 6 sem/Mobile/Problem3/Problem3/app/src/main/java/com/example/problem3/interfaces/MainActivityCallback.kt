package com.example.problem3.interfaces

import com.example.problem3.NamesOfFragment
import com.example.problem3.data.Student

interface MainActivityCallback {
    fun newTitle(_title: String)
    fun showFragment(fragmentType:NamesOfFragment,student: Student?=null)
}