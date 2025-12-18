"""
Модуль для работы с файлами
"""

import os

class FileHandler:
    """
    Класс для чтения и записи файлов
    """
    
    @staticmethod
    def read_file(file_path):
        """
        Чтение файла в бинарном режиме
        
        Аргументы:
            file_path: str - путь к файлу
        
        Возвращает:
            bytes - содержимое файла
        
        Исключения:
            FileNotFoundError: если файл не существует
            IOError: если ошибка чтения файла
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except IOError as e:
            raise IOError(f"Ошибка чтения файла {file_path}: {str(e)}")
    
    @staticmethod
    def write_file(file_path, data):
        """
        Запись данных в файл в бинарном режиме
        
        Аргументы:
            file_path: str - путь к файлу
            data: bytes - данные для записи
        
        Исключения:
            IOError: если ошибка записи файла
        """
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
        except IOError as e:
            raise IOError(f"Ошибка записи файла {file_path}: {str(e)}")
    
    @staticmethod
    def generate_output_path(input_path, operation, suffix=None):
        """
        Генерация пути для выходного файла
        
        Аргументы:
            input_path: str - путь к входному файлу
            operation: str - операция ('encrypt' или 'decrypt')
            suffix: str - дополнительный суффикс (опционально)
        
        Возвращает:
            str - путь для выходного файла
        """
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        
        if suffix:
            new_name = f"{name}_{suffix}{ext}"
        else:
            if operation == 'encrypt':
                new_name = f"{name}_encrypted{ext}"
            else:  # decrypt
                new_name = f"{name}_decrypted{ext}"
        
        return os.path.join(dir_name, new_name)