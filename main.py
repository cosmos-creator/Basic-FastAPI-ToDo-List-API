from fastapi import FastAPI, HTTPException, Depends, Query
from contextlib import asynccontextmanager
from database import create_db_tables, engine, Task
from sqlmodel import select, Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)

async def get_db():
    with Session(engine) as session:
        yield session

@app.get("/")
def view_task(db: Session = Depends(get_db)):
    statement = select(Task)
    tasks = db.exec(statement).all()
    if not tasks:
        raise HTTPException(status_code=200, detail="File was found but no tasks were there to show. Try adding new tasks.")
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