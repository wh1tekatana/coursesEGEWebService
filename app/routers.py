from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ученики
@router.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    if student.course_id:
        db_student.course_id = student.course_id
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    return db_student

@router.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    for var, value in vars(student).items():
        setattr(db_student, var, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    db.delete(db_student)
    db.commit()
    return db_student

# курсы
@router.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.dict())
    if course.teacher_id:
        teacher = db.query(models.Teacher).filter(models.Teacher.id == course.teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Учитель не найден")
        db_course.teacher = teacher
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return db_course

@router.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Курс не найден")
    for var, value in vars(course).items():
        setattr(db_course, var, value)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}", response_model=schemas.Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Курс не найден")
    db.delete(db_course)
    db.commit()
    return db_course

# учителя
@router.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(**teacher.dict())
    if teacher.courses:
        for course_id in teacher.courses:
            course = db.query(models.Course).filter(models.Course.id == course_id).first()
            if not course:
                raise HTTPException(status_code=404, detail=f"Курс с ID - {course_id} не найден")
            db_teacher.courses.append(course)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    return db_teacher

@router.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    for var, value in vars(teacher).items():
        setattr(db_teacher, var, value)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.delete("/teachers/{teacher_id}", response_model=schemas.Teacher)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Учитель не найден")
    db.delete(db_teacher)
    db.commit()
    return db_teacher

# экзамены
@router.post("/exams/", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    db_exam = models.Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@router.get("/exams/{exam_id}", response_model=schemas.Exam)
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    db_exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    return db_exam

@router.put("/exams/{exam_id}", response_model=schemas.Exam)
def update_exam(exam_id: int, exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    db_exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    for var, value in vars(exam).items():
        setattr(db_exam, var, value)
    db.commit()
    db.refresh(db_exam)
    return db_exam

@router.delete("/exams/{exam_id}", response_model=schemas.Exam)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    db_exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Экзамен не найден")
    db.delete(db_exam)
    db.commit()
    return db_exam
