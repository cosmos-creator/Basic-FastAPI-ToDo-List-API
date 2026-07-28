from sqlmodel import Field, SQLModel, create_engine, Session

class Task(SQLModel, table=True):
    # table=True stores the class metadate in SQLModel.metadata
    id: int | None = Field(default=None,primary_key=True)
    name: str 
    description: str | None = None

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# holds network connections to the db
engine = create_engine(sqlite_url)

def create_db_tables():

    SQLModel.metadata.create_all(engine)

def main():
    create_db_tables()
# this is executed when we call/run the file with python app.py
# and doesnt run when we import it
if __name__ == "__main__":
    main()