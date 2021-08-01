def hyphen_decorator(func):
    def wrapper():
        result = func()
        print("-------------")
        return result
    return wrapper