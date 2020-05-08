'''
If a finally clause is present, the finally clause will execute as the 
last task before the try statement completes.
'''


def fun(a, b):
    print("Inside function")
    try:
        return a/b
    except ZeroDivisionError:
        print("ZeroDivisionError")
    else:
        print("Inside else")
    finally:
        print("Inside the finally")

    
def merge(*args: dict, **kwargs: dict):
    print(type(args))
    print(type(kwargs))
    for mappable in args:
        if set(mappable) & set(kwargs):  # Intersection of keys
            raise ValueError(
                "Found duplicate keys in merge: {}".format(set(mappable) & set(kwargs))
            )
        kwargs.update(mappable)
    return kwargs


def headline(text: str, align: bool = True) -> str:
    if align:
        return f"{text.title()}\n{'-' * len(text)}"
    else:
        return f" {text.title()} ".center(50, "o")

if __name__ == "__main__":
    print(fun(10, 0))
    print(fun(20, 30))

    a = {1: 2, 3: 4}
    b = {10: 20, 11:22}
    merge(a, b)

    print(headline("Python type checking", align=True))
    print(headline("Python type checking", align="left"))  # Still evaluates to True
    print(headline("Python type checking", align="center"))  # These are only hints, not enforced