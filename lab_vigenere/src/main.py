"""
Главный модуль программы для шифрования/расшифрования файлов
с использованием шифра Виженера

Цель работы: изучение классических криптографических алгорит- мов одноалфавитных подстановок, многоалфавитных подстановок и перестановок для защиты открытых текстов.
Задание. Написать программу, которая шифрует/расшифровывает файл с помощью шифра, который соответствует индивидуальному варианту.
Вариант

4. Шифр Виженера с числовым ключом для двоичных файлов. Алфавит кольцо вычетов по модулю 

Входные данные: любой файл (двоичный или текстовый), ключ шифрования/расшифрования и режим шифрования.
Выходные данные: зашифрованный или расшифрованный файл. Методические указания. Теоретический материал для выполнения

"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vigenere import VigenereCipher
from file_handler import FileHandler
from utils import validate_key, parse_key

def main():
    """
    Основная функция программы
    """
    parser = argparse.ArgumentParser(
        description='Шифрование и расшифрование файлов с использованием шифра Виженера',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Примеры использования:
                Шифрование: python main.py input.txt --key "12345" --encrypt
                Расшифрование: python main.py input_encrypted.txt --key "12345" --decrypt
                С указанием выходного файла: python main.py input.txt --key "secret" --encrypt -o output.bin
        """
    )
    
    parser.add_argument('input_file', help='Путь к входному файлу')
    
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--encrypt', '-e', action='store_true', 
                          help='Режим шифрования')
    mode_group.add_argument('--decrypt', '-d', action='store_true', 
                          help='Режим расшифрования')
    
    parser.add_argument('--key', '-k', required=True, 
                       help='Ключ шифрования (число или строка)')
    
    parser.add_argument('--output', '-o', 
                       help='Путь к выходному файлу (опционально)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Подробный вывод информации')
    
    args = parser.parse_args()
    
    try:
        if not os.path.exists(args.input_file):
            print(f"Ошибка: Файл '{args.input_file}' не найден")
            sys.exit(1)
        
        if args.verbose:
            print(f"Используемый ключ: {args.key}")
        
        key_bytes = parse_key(args.key)
        validate_key(key_bytes)
        
        if args.verbose:
            print(f"Ключ в байтах: {key_bytes}")
            print(f"Длина ключа: {len(key_bytes)} байт")
        
        cipher = VigenereCipher(key_bytes)
        
        if args.verbose:
            print(f"Чтение файла: {args.input_file}")
        
        file_size = os.path.getsize(args.input_file)
        if args.verbose:
            print(f"Размер файла: {file_size} байт")
        
        data = FileHandler.read_file(args.input_file)
        
        if args.encrypt:
            if args.verbose:
                print("Выполнение шифрования...")
            result = cipher.encrypt(data)
            operation = 'encrypt'
        else:  # decrypt
            if args.verbose:
                print("Выполнение расшифрования...")
            result = cipher.decrypt(data)
            operation = 'decrypt'
        
        if args.output:
            output_path = args.output
        else:
            output_path = FileHandler.generate_output_path(args.input_file, operation)
        
        if args.verbose:
            print(f"Запись результата в: {output_path}")
        
        FileHandler.write_file(output_path, result)
        
        print(f"Операция {'шифрования' if args.encrypt else 'расшифрования'} завершена успешно!")
        print(f"Входной файл: {args.input_file}")
        print(f"Выходной файл: {output_path}")
        print(f"Размер обработанных данных: {len(data)} байт")
        
    except ValueError as e:
        print(f"Ошибка в ключе: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Ошибка файла: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()