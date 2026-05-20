from core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, text


class User(Base):
    """Sending List"""

    __tablename__ = "SendingList"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Login = Column(String(255))
    Name = Column(String(255))
    ChatID = Column(String(255), unique=True)
    RegDate = Column(Date, server_default=text("GETDATE()"))
    IsOn = Column(Boolean, default=True, nullable=False)


class Duties(Base):
    """Duties List"""

    __tablename__ = "DutySchedule"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True, autoincrement=True)
    WeekDay = Column(String(100))
    Date = Column(Date)
    Main = Column(String(100))
    Additional = Column(String(100))
    Vacation = Column(String(100))
    Comment = Column(String(1000))
    LoginMain = Column(String(100))
    LoginAdditional = Column(String(100))
