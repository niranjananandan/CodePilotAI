def calculate_average(numbers):
    if not numbers:
        raise ValueError("Numbers list cannot be empty.")

    return sum(numbers) / len(numbers)