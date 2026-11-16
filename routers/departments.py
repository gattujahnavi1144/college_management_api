from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Department
from schemas import DepartmentCreate, DepartmentOut


router = APIRouter(prefix="/api/departments", tags=["Departments"])


@router.get("/", response_model=list[DepartmentOut])
def get_departments(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Department).order_by(Department.department_id)).all()


@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    department: DepartmentCreate, db: Annotated[Session, Depends(get_db)]
):
    new_department = Department(**department.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department