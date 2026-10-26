def safe_divide(a, b):
    if b == 0:
        raise ValueError("division by zero is not allowed")
    return a / b
