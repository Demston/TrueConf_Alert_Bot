import os
from dotenv import load_dotenv
# from contextlib import contextmanager
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base  # scoped_session


# load from .env
load_dotenv()

engine = create_async_engine(
 f"mssql+aioodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
 f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
 f"{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server", isolation_level="AUTOCOMMIT"
)

# engine = create_engine(
#     f"mssql+pyodbc://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
#     "&Trusted_Connection=yes"
# )

Base = declarative_base()

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
