"""
Реализация шифра Виженера для двоичных данных
Работа в кольце вычетов по модулю 256
"""

class VigenereCipher:
    """
    Класс для шифрования методом Виженера
    """
    
    def __init__(self, key):
        """
        Инициализация шифра с ключом
        
        Аргументы:
            key: bytes - ключ шифрования в виде байтов
        """
        self.key = key
        self.key_length = len(key)
    
    def encrypt(self, data):
        """
        Шифрование данных
        
        Аргументы:
            data: bytes - исходные данные для шифрования
        
        Возвращает:
            bytes - зашифрованные данные
        """
        if not data:
            return b''
        
        encrypted = bytearray(len(data))
        
        for i, byte in enumerate(data):
            # Операция сложения по модулю 256
            key_byte = self.key[i % self.key_length]
            encrypted[i] = (byte + key_byte) % 256
        
        return bytes(encrypted)
    
    def decrypt(self, data):
        """
        Расшифрование данных
        
        Аргументы:
            data: bytes - зашифрованные данные
        
        Возвращает:
            bytes - расшифрованные данные
        """
        if not data:
            return b''
        
        decrypted = bytearray(len(data))
        
        for i, byte in enumerate(data):
            key_byte = self.key[i % self.key_length]
            decrypted[i] = (byte - key_byte) % 256
        
        return bytes(decrypted)