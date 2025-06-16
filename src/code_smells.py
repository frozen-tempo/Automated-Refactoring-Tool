def list_comprehension_with_condition(numbers):
    """Expected complexity: 2 (1 if in comprehension = 1 decision point + 1)"""
    return [x for x in numbers if x > 0]