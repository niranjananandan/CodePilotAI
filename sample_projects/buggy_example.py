def get_first_item(items):
    if not items:
        raise ValueError("items cannot be empty")

    return items[0]