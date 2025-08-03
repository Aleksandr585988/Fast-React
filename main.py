from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
def serve_ui():
    return FileResponse(os.path.join("static", "index.html"))


# Список студентов (имитация базы данных)
students = [
    {"id": 1, "name": "Alex", "age": 23, 'marks': [4, 3, 1, 4, 2, 2, 3], "info": "hobbies kar"},
    {"id": 2, "name": "Maria", "age": 35, 'marks': [4, 5, 1, 4, 5, 2, 5], "info": "hobbies cosmo"},
    {"id": 3, "name": "John", "age": 40, 'marks': [4, 5, 1, 4, 5, 2, 5], "info": "hobbies sport"}
]

Student_not_found = HTTPException(status_code=404, detail="Student not found")
No_marks_student = HTTPException(status_code=400, detail="No marks available for this student")

class Student(BaseModel):
    id: int
    name: str
    marks: list[int]

# Главная страница
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/students")
def add_student(student: Student):
    if any(s["id"] == student.id for s in students):
        raise HTTPException(status_code=400, detail="Student with this ID already exists")
    students.append(student.model_dump())
    return {"message": "Student added successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            del students[i]
            return {"message": "Student deleted"}
    raise Student_not_found

# Эндпоинт: получить список всех студентов
@app.get("/students")
def get_students():
    return students

# Эндпоинт: получить студента по NAME
@app.get("/students/name/{student_name}")
def get_student_by_name(student_name: str) -> dict:
    for student in students:
        if student["name"].lower() == student_name.lower():
            return student
    raise Student_not_found

# Эндпоинт: получить среднюю оценку по NAME
@app.get("/students/{student_name}/marks")
def get_student_marks(student_name: str) -> float:
    student = get_student_by_name(student_name)

    if student is None:
        raise Student_not_found

    if not student.get("marks"):
        raise No_marks_student

    return sum(student["marks"]) / len(student["marks"])

# Эндпоинт: Получить студента по ID
@app.get("/students/id/{student_id}")
def get_student_by_id(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


