from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.DB.people import get_employees, add_employee
from application.salary import calculate_salary
from models.models import Base
from config.db_config import DB_CONFIG
import logging

def init_db():
    try:
        # Добавляем параметр для автоматического создания БД
        connection_string = (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

        engine = create_engine(connection_string)

        # Создаем все таблицы в БД
        Base.metadata.create_all(engine)

        # Создаем фабрику сессий
        Session = sessionmaker(bind=engine)
        return Session()

    except Exception as e:
        logging.error(f"Ошибка подключения к БД: {str(e)}")
        raise

def main():
    session = init_db()
    try:
        while True:
            print("\nСистема учета сотрудников")
            print("1. Добавить сотрудника")
            print("2. Показать список сотрудников")
            print("3. Посчитать зарплату сотрудника")
            print("4. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                add_employee(session)

            elif choice == '2':
                get_employees(session)

            elif choice=='3':
                employee_id = input("Введите ID сотрудника для расчетов ")
                calculate_salary(session,int(employee_id))

            elif choice == '4':
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