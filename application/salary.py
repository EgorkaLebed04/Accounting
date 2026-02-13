from models.models import Employee
from sqlalchemy.orm import Session
from utils.decorators import date_decorator


@date_decorator
def calculate_salary(session: Session, employee_id: int):
    employee = session.query(Employee).filter_by(employee_id=employee_id).first()

    base_salary = employee.salary
    job_day = int(input("Сколько отработал дней? "))
    if job_day == 1:
        day_word = "день"
    elif job_day in [2, 3, 4]:
        day_word="дня"
    else :
        day_word ="дней"
    total = int(base_salary) * job_day
    print(f"За {job_day} {day_word} {employee.last_name} {employee.first_name} получил(а): {total} рублей", end="\n")