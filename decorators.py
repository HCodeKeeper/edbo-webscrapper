def hyphen_decorator(func):
    def wrapper():
        func()
        print("-------------")
    return wrapper