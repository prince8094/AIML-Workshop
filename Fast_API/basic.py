from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Student(BaseModel):
    name: str
    email: EmailStr
    age: int


@app.get("/students/{student_id}")
def get_student(student_id: int, course: str = "Python"):
    return {
        "student_id": student_id,
        "course": course
    }


@app.post("/students")
def create_student(student: Student):
    return {
        "message": "Student created",
        "student": student.model_dump()
    }