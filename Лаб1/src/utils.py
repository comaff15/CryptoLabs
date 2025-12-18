"""
Вспомогательные функции для работы программы

"""

def validate_key(key_bytes):
    
    """
    Проверка корректности числового ключа
    
    Аргументы:
        key_bytes: bytes - ключ в виде байтов
    
    Возвращает:
        bool - True если ключ корректен
    """
    if not key_bytes:
        raise ValueError("Ключ не может быть пустым")
    if len(key_bytes) > 1024:
        raise ValueError("Ключ слишком длинный (максимум 1024 байта)")
    return True


def parse_key(key_str):
    """
    Преобразование строкового ключа в байты
    
    Аргументы:
        key_str: str - ключ в виде строки
    
    Возвращает:
        bytes - ключ в виде байтов
    """

    try:
        if key_str.isdigit():
            num = int(key_str)
            return num.to_bytes((num.bit_length() + 7) // 8, 'big')
    except:
        pass
    
    # Если не получилось как число, используем как строку
    return key_str.encode('utf-8')