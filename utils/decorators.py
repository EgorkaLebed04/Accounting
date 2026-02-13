from datetime import datetime

def date_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Дата выполнения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return func(*args, **kwargs)
    return wrapper
