from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import os
from dotenv import load_dotenv

# load from .env
load_dotenv()

engine = create_engine(
 f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
 f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
 f"{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server",isolation_level="AUTOCOMMIT"
)

# engine = create_engine(
#     f"mssql+pyodbc://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
#     "&Trusted_Connection=yes"
# )

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
