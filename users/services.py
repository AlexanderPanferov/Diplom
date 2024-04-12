import random
import string
import time


def code_generation():
    """Генерация кода подтверждения для регистрации и авторизации"""
    code = ''.join(random.choices(string.digits, k=4))
    time.sleep(2)  # Имитация задержки отправки
    print(f"Код подтверждения: {code}")
    return code
