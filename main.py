from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, Employee
from config.db_config import DB_CONFIG
import logging
import psycopg2
from psycopg2 import OperationalError
import re

def init_db():
    try:
        engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()

    except Exception as e:
        logging.error(f"Ошибка подключения к БД: {str(e)}")
        raise

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^(\+7|8)?[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    return re.match(pattern, phone) is not None

def add_employee(session):
    print("\nДобавление нового сотрудника")
    last_name = input("Фамилия: ").strip()
    first_name = input("Имя: ").strip()
    surname = input("Отчество: ").strip()
    organization = input("Организация: ").strip()
    position = input("Должность: ").strip()
    phone = input("Телефон: ").strip()
    email = input("Email: ").strip()

    if not last_name or not first_name:
        print("Ошибка: обязательно заполните поля Фамилия и Имя")
        return

    if email and not validate_email(email):
        print("Ошибка: неверный формат email")
        return

    if phone and not validate_phone(phone):
        print("Ошибка: неверный формат телефона")
        return

    try:
        new_employee = Employee(
            last_name=last_name,
            first_name=first_name,
            surname=surname,
            organization=organization,
            position=position,
            phone=phone,
            email=email
        )
        session.add(new_employee)
        session.commit()
        print("Сотрудник успешно добавлен!")

    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка: {str(e)}")

def show_employees(session):
    print("\nСписок сотрудников:")
    employees = session.query(Employee).all()

    for emp in employees:
        print(f"ID: {emp.employee_id}")
        print(f"ФИО: {emp.last_name} {emp.first_name} {emp.surname}")
        print(f"Организация: {emp.organization}")
        print(f"Должность: {emp.position}")
        print(f"Телефон: {emp.phone}")
        print(f"Email: {emp.email}")
        print("-" * 40)

def main():
    global session
    try:
        session = init_db()
        while True:
            print("\nСистема учета сотрудников")
            print("1. Добавить сотрудника")
            print("2. Показать список сотрудников")
            print("3. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                add_employee(session)

            elif choice == '2':
                show_employees(session)

            elif choice == '3':
                print("До свидания!")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
