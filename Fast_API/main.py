from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from database import engine, SessionLocal, Base
from models import Student, User
from schemas import StudentCreate, UserCreate, UserLogin

from pwdlib import PasswordHash


app = FastAPI()

# Password hashing
password_hasher = PasswordHash.recommended()


# Create tables in MySQL
Base.metadata.create_all(bind=engine)


# Get database connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ---------------- HOME ----------------

@app.get("/")
def home():

    return {
        "message": "FastAPI + MySQL working"
    }


# ---------------- STUDENTS ----------------

@app.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student created successfully",
        "id": new_student.id,
        "name": new_student.name,
        "email": new_student.email,
        "age": new_student.age
    }


@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students


# ---------------- REGISTER ----------------

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    # Hash password
    password_hash = password_hasher.hash(
        user.password
    )

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account created successfully",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# ---------------- LOGIN ----------------

@app.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    # Verify password
    password_correct = password_hasher.verify(
        user.password,
        existing_user.password_hash
    )

    if not password_correct:
        return {
            "message": "Invalid email or password"
        }

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email
    }


# ---------------- LOGIN PAGE ----------------

@app.get("/login", response_class=HTMLResponse)
def login_page():

    with open("templates/login.html", "r") as file:
        return file.read()


# ---------------- REGISTER PAGE ----------------

@app.get("/register", response_class=HTMLResponse)
def register_page():

    with open("templates/register.html", "r") as file:
        return file.read()