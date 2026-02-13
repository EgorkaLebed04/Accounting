from sqlalchemy.orm import Session
from models.models import Employee
from utils.decorators import date_decorator

@date_decorator
def get_employees(session: Session):
    print("\nСписок сотрудников:")
    employees = session.query(Employee).all()

    for emp in employees:
        print(f"ID: {emp.employee_id}")
        print(f"ФИО: {emp.last_name} {emp.first_name} {emp.middle_name}")
        print(f"Дневная зарплата: {emp.salary:.2f} руб.")
        print("-" * 40)

@date_decorator
def add_employee(session):
    print("\nДобавление нового сотрудника")
    last_name = input("Фамилия: ").strip()
    first_name = input("Имя: ").strip()
    middle_name = input("Отчество: ").strip()

    if not last_name or not first_name:
        print("Ошибка: обязательно заполните поля Фамилия и Имя")
        return

    try:
        salary_input = input('Зарплата за смену: ').replace(',', '.')
        salary = float(salary_input)
    except ValueError:
        print("Некорректный ввод зарплаты.")
        return

    # Проверка на существование сотрудника с такой же фамилией и именем
    existing_employee = session.query(Employee).filter(
        Employee.last_name == last_name,
        Employee.first_name == first_name
    ).first()

    if existing_employee:
        print(f"⚠️  Сотрудник с фамилией '{last_name}' и именем '{first_name}' уже существует в базе данных.")
        confirm = input("Всё равно добавить? (да/нет): ").strip().lower()
        if confirm not in ['да', 'д', 'yes', 'y']:
            print("Добавление отменено.")
            return

    # Создание и добавление нового сотрудника
    try:
        new_employee = Employee(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            salary=salary
        )
        session.add(new_employee)
        session.commit()
        print("✅ Сотрудник успешно добавлен!")
    except Exception as e:
        session.rollback()
        print(f"❌ Произошла ошибка при добавлении сотрудника: {str(e)}")
