from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# For SQLAlchemy: next line for 2.0, other line for 1.4
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base

import os
from constants import *
from server_cfg import GENERAL_SERVER_EXECUTION_MODE, API_DB_USERNAME, API_DB_PWD, API_DB_HOSTNAME, DB_ENGINE_ECHO

app = FastAPI()

PWD = API_DB_PWD

USERNAME = API_DB_USERNAME
DB_NAME= API_DB_USERNAME
DRIVER = "ODBC Driver 17 for SQL Server"

engine_stmt = "mssql+pyodbc://%s:%s@%s/%s?driver=%s" % (USERNAME, PWD, API_DB_HOSTNAME, DB_NAME, DRIVER)
# engine = create_engine(engine_stmt, echo=True, future=True, supports_comments=True)

engine = create_engine(engine_stmt, echo=DB_ENGINE_ECHO, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



class NoReturningBase():
    # Class to forbid default OUTPUT, solve occasional triggers issue
    # DML statement cannot have any enabled triggers if the statement contains an OUTPUT clause without INTO clause
    __table_args__ = {'implicit_returning': False}

    @classmethod
    def update_args(cls, table_args: dict):
        # Method tu update the parent __table_args__ dict
        # Used for
        newargs = table_args.copy()
        newargs.update(cls.__table_args__)
        return newargs
