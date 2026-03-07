from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, create_engine
from os import environ

load_dotenv()

engine = create_engine(environ.get("DATABASE_URI", ""))

SQLModel.metadata.create_all(engine)

TABLE_CONSTRUCTORS = []


def register_table_constructor(table_constructor):
    TABLE_CONSTRUCTORS.append(table_constructor)
    return table_constructor


def construct_tables():
    with Session(engine) as session:
        for ctor in TABLE_CONSTRUCTORS:
            ctor(session)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
