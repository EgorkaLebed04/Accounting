import datetime

def date_decorator(func):
    def wrapper():
        print(datetime.date.today())
        func()
    return wrapper