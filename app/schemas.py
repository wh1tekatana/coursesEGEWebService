from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExamBase(BaseModel):
    subject: str
    date: datetime

class ExamCreate(ExamBase):
    student_id: int

class Exam(ExamBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    phone: str

class StudentCreate(StudentBase):
    course_id: Optional[int] = None

class Student(StudentBase):
    id: int
    registration_date: datetime
    course_id: Optional[int]
    exams: List['Exam'] = []  # Используем строку для аннотации типа

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    title: str
    description: str
    duration: int
    start_date: datetime
    teacher_id: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    students: List['Student'] = []  # Используем строку для аннотации типа
    teacher_id: Optional[int]

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class TeacherCreate(TeacherBase):
    courses: Optional[List[int]] = []

    class Config:
        orm_mode = True

class Teacher(TeacherBase):
    id: int
    courses: List['Course'] = []  # Используем строку для аннотации типа

    class Config:
        orm_mode = True
