from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


config_vacancy_association = Table(
    "config_vacancy_association",
    Base.metadata,
    Column("config_id", Integer, ForeignKey("configs.id"), primary_key=True),
    Column("vacancy_id", Integer, ForeignKey("vacancies.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    lang = Column(String(3), default="eng")
    is_premium = Column(Boolean, default=False)


class Config(Base):
    __tablename__ = "configs"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    title = Column(String(500))
    lang = Column(String(50))
    exp_years = Column(Integer())
    region = Column(String(50), nullable=True)
    salary_usd = Column(Integer(), nullable=True)
    eng_lvl = Column(String(20), nullable=True)
    search_words = Column(String(500), nullable=True)
    refresh_time_min = Column(Integer())
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    vacancies = relationship("Vacancy", secondary=config_vacancy_association, back_populates="configs")


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer(), primary_key=True)
    url = Column(String(300), unique=True)
    title = Column(String(500))
    date = Column(String(500))
    location = Column(String(200))
    company_name = Column(String(200))
    description = Column(String(700))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    configs = relationship(Config, secondary=config_vacancy_association, back_populates="vacancies")
