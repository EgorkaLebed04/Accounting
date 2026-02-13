from models.models import Salary, Employee, Position
from sqlalchemy.orm import Session
from utils.decorators import date_decorator
from datetime import date


@date_decorator
def calculate_salary(session: Session, employee_id: int, month: date):
    employee = session.query(Employee).filter_by(employee_id=employee_id).first()
    position = session.query(Position).filter_by(position_id=employee.position_id).first()

    base_salary = position.base_salary
    bonus = base_salary * (position.bonus_percent / 100)
    tax = (base_salary + bonus) * 0.13  # Пример расчета НДФЛ
    total = base_salary + bonus - tax

    new_salary = Salary(
        employee_id=employee_id,
        month=month,
        base_salary=base_salary,
        bonus=bonus,
        award=0.00,  # Можно добавить логику расчета награды
        tax=tax,
        total=total
    )

    session.add(new_salary)
    session.commit()
    return new_salary