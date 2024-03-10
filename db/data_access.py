from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

from server_cfg import DB_ENGINE_ECHO, SQLITE_FILE_PATH


sqlite_url = f"sqlite:///{SQLITE_FILE_PATH}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=DB_ENGINE_ECHO, connect_args=connect_args)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session()-> Session:
    with Session(engine) as session:
        return session
