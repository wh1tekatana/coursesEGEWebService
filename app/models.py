from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="students")
    exams = relationship("Exam", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    duration = Column(Integer)  # Duration in days
    start_date = Column(DateTime)
    students = relationship("Student", back_populates="course")
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    courses = relationship("Course", back_populates="teacher")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    date = Column(DateTime)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="exams")
