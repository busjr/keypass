import random
import string

# def generate_pass(length, ):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     password = ''.join(random.choice(characters) for _ in range(16))
#     return password

def generate_pass(length, en_latter, ru_latter, lower, upper, special, number):
    characters = ''

    if en_latter:
        if lower:
            characters += string.ascii_lowercase
        if upper:
            characters += string.ascii_uppercase

    if ru_latter:
        ru_lower = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        ru_upper = ru_lower.upper()
        if lower:
            characters += ru_lower
        if upper:
            characters += ru_upper

    if number:
        characters += string.digits

    if special:
        characters += string.punctuation

    if not characters:
        return ''

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

