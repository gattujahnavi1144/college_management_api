from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Department, Student
from schemas import StudentCreate, StudentOut


router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("/", response_model=list[StudentOut])
def get_students(db: Annotated[Session, Depends(get_db)]):
    statement = (
        select(Student)
        .options(joinedload(Student.department))
        .order_by(Student.student_id)
    )
    return db.scalars(statement).all()


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Annotated[Session, Depends(get_db)]):
    department = db.get(Department, student.department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )

    new_student = Student(student_name=student.student_name, department=department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student