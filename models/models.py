from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    department_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    head_id = Column(Integer, ForeignKey('employees.employee_id'))

class Position(Base):
    __tablename__ = 'positions'
    position_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    base_salary = Column(DECIMAL(10, 2))
    bonus_percent = Column(DECIMAL(5, 2))

class Employee(Base):
    __tablename__ = 'employees'
    employee_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    patronymic = Column(String)
    birth_date = Column(Date)
    employment_date = Column(Date)
    position_id = Column(Integer, ForeignKey('positions.position_id'))
    department_id = Column(Integer, ForeignKey('departments.department_id'))

class Salary(Base):
    __tablename__ = 'salaries'
    salary_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    month = Column(Date)
    base_salary = Column(DECIMAL(10, 2))
    bonus = Column(DECIMAL(10, 2))
    award = Column(DECIMAL(10, 2))
    tax = Column(DECIMAL(10, 2))
    total = Column(DECIMAL(10, 2))
