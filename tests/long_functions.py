def add_numbers(a, b):
    return a + b


def calculate_factorial(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def find_max_in_list(numbers):
    if not numbers:
        return None
    max_value = numbers[0]
    for num in numbers:
        if num > max_value:
            max_value = num
    return max_value


def reverse_string(text):
    if not text:
        return ""
    reversed_text = ""
    for i in range(len(text) - 1, -1, -1):
        reversed_text += text[i]
    return reversed_text


def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for i in range(3, int(number ** 0.5) + 1, 2):
        if number % i == 0:
            return False
    return True


def count_vowels(text):
    if not text:
        return 0
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count


def fibonacci_sequence(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_num)
    return sequence


def calculate_grade_average(grades):
    if not grades:
        return 0
    
    total = 0
    count = 0
    
    for grade in grades:
        if grade < 0 or grade > 100:
            continue
        total += grade
        count += 1
    
    if count == 0:
        return 0
    
    average = total / count
    
    if average >= 90:
        letter_grade = "A"
    elif average >= 80:
        letter_grade = "B"
    elif average >= 70:
        letter_grade = "C"
    elif average >= 60:
        letter_grade = "D"
    else:
        letter_grade = "F"
    
    return {
        "average": round(average, 2),
        "letter_grade": letter_grade,
        "total_grades": count
    }


def sort_numbers(numbers):
    if not numbers:
        return []
    
    sorted_list = numbers.copy()
    n = len(sorted_list)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_list[j] > sorted_list[j + 1]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
    
    return sorted_list


def analyze_text_statistics(text):
    if not text:
        return {
            "character_count": 0,
            "word_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "average_word_length": 0
        }
    
    character_count = len(text)
    
    words = []
    current_word = ""
    for char in text:
        if char.isalnum():
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
    if current_word:
        words.append(current_word)
    
    word_count = len(words)
    
    sentence_count = 0
    for char in text:
        if char in ".!?":
            sentence_count += 1
    
    paragraph_count = 1
    for i in range(len(text) - 1):
        if text[i] == "\n" and text[i + 1] == "\n":
            paragraph_count += 1
    
    if word_count > 0:
        total_word_length = sum(len(word) for word in words)
        average_word_length = total_word_length / word_count
    else:
        average_word_length = 0
    
    return {
        "character_count": character_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "average_word_length": round(average_word_length, 2)
    }