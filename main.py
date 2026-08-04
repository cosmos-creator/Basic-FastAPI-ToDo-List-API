from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import create_db_tables, engine, Task, User
from sqlmodel import select, Session
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt
import os

# creates a bcrypt hashing tool
pwd_context = CryptContext(schemes=["bcrypt"])
TOKEN_TIME_IN_MIN = 30
SECRET_KEY = os.getenv("SECRET_KEY") # shh its a secret
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

def get_db():
    with Session(engine) as session:
        yield session

def hash_pass(password: str):
    return pwd_context.hash(password)

def create_token(data: dict):
    valid_till = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TIME_IN_MIN)
    data["exp"] = valid_till

    return jwt.encode(data, SECRET_KEY, "HS256")

def username_valid(username: str, db: Session):
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()

    return result is None

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token, SECRET_KEY, "HS256")
        username = data["sub"]

        statement = select(User).where(User.username == username)
        result = db.exec(statement).first()

        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail="invalid token")


app = FastAPI(lifespan=lifespan)


class UserRegister(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):

    if not username_valid(user_data.username, db):
        raise HTTPException(status_code=409, detail="username already taken")
    
    hashed_password = hash_pass(user_data.password)

    user = User(username=user_data.username, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "response": f"{user.username} created successfully"
    }
    

@app.get("/")
def view_task(db: Session = Depends(get_db)):
    statement = select(Task)
    tasks = db.exec(statement).all()
    if not tasks:
        return []
    else:
        return tasks

@app.post("/add")
def add_task(task: Task, db: Session = Depends(get_db)):
    task_meta = Task(name=task.name, description=task.description)

    db.add(task_meta)
    db.commit()
    db.refresh(task_meta)

    return task_meta


@app.delete("/delete")
def delete_task(id: int = Query(gt=0, default=1), db: Session = Depends(get_db)):

    statement = select(Task).where(Task.id == id)
    result = db.exec(statement)
    try:
        task = result.one()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found.")

    db.delete(task)
    db.commit()

    return task