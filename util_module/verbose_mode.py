def verbose_decorator(func, message=None):

    def wrapper(*args, **kwargs):
        if message is None:
            m = ":::RUNNING FUNCTION: " + str(func.__name__).upper() + ":::"
        else:
            m = message

        print(m)
        func(*args, **kwargs)
        print(":::DONE:::")

    return wrapper
