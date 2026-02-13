from sqlalchemy.orm import Session
from models.models import Employee
from utils.decorators import date_decorator

@date_decorator
def get_employees(session: Session):
    return session.query(Employee).all()
