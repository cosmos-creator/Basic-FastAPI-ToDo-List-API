from fastapi import FastAPI, HTTPException, Depends
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

    statement = select(Task)
    return db.exec(statement).all()

# @app.post("/done/")
# def delete_task(key: TaskID):
    check_file()
    with open(file,"a+", encoding="utf-8") as tasks:
        tasks.seek(0)
        try:
            existing = json.load(tasks) # loads as a dict object
        except Exception as e:
            existing = {}
        
        tasks.truncate(0) # deltes file content, everything, makes file size 0

        if str(key.key) in existing:
            del existing[str(key.key)]
            json.dump(existing, tasks, indent=4,sort_keys=True)
        else:
            json.dump(existing, tasks, indent=4,sort_keys=True)
            raise HTTPException(status_code=404, detail="Task not found.")