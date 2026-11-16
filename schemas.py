from pydantic import AliasPath, BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    department_name: str = Field(min_length=1, max_length=255)


class DepartmentOut(DepartmentCreate):
    model_config = ConfigDict(from_attributes=True)

    department_id: int


class StudentCreate(BaseModel):
    student_name: str = Field(min_length=1, max_length=255)
    department_id: int


class StudentOut(StudentCreate):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    student_id: int
    department_name: str = Field(
        validation_alias=AliasPath("department", "department_name")
    )