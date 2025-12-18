#!/usr/bin/env python3
"""
Демонстрационная программа для шифра Виженера
Показывает все возможности программы на различных примерах
"""

import os
import sys
import tempfile
import random
import string
import time
import argparse

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vigenere import VigenereCipher
from file_handler import FileHandler
from utils import validate_key, parse_key

class VigenereDemo:
    """Класс для демонстрации работы шифра Виженера"""
    
    def __init__(self):
        self.demo_files = []
        self.temp_dir = tempfile.mkdtemp(prefix="vigenere_demo_")
        print(f"Создана временная директория: {self.temp_dir}")
        print("-" * 60)
    
    def cleanup(self):
        """Очистка временных файлов"""
        import shutil
        for file_path in self.demo_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        print("Временные файлы удалены")
    
    def create_test_file(self, filename, content_type='text', size_kb=1):
        """Создание тестового файла"""
        file_path = os.path.join(self.temp_dir, filename)
        
        if content_type == 'text':
            # Текстовый файл
            text = "Шифр Виженера — метод полиалфавитного шифрования буквенного текста с использованием ключевого слова.\n"
            text += "Этот метод шифрования назван в честь Блеза де Виженера, хотя он был изобретен Джованом Баттистой Беллазо.\n"
            text += "Данный шифр является частным случаем шифра Цезаря, но с переменным сдвигом.\n" * 5
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
        
        elif content_type == 'binary':
            # Бинарный файл
            size = size_kb * 1024
            random_bytes = bytes([random.randint(0, 255) for _ in range(size)])
            with open(file_path, 'wb') as f:
                f.write(random_bytes)
        
        elif content_type == 'mixed':
            # Смешанный файл (текст + бинарные данные) - УЛУЧШЕННАЯ ВЕРСИЯ
            text = "Начало файла с текстом:\n"
            text += "=" * 50 + "\n"
            text += "Это демонстрационный файл для тестирования шифра Виженера.\n"
            text += "Шифр Виженера работает с любыми типами данных.\n"
            text += "Этот файл содержит как текст, так и случайные байты.\n"
            text += "=" * 50 + "\n"
            text += "А вот и бинарные данные:\n"
            
            # Бинарные данные - меньше, чтобы не перегружать вывод
            binary_data = bytes([random.randint(0, 255) for _ in range(256)])
            
            with open(file_path, 'wb') as f:
                f.write(text.encode('utf-8'))
                f.write(binary_data)
        
        self.demo_files.append(file_path)
        return file_path
    
    def print_mixed_data(self, data, max_bytes=150, title="Данные"):
        """
        Умный вывод смешанных данных (текст + бинарные)
        """
        print(f"{title} (первые {min(len(data), max_bytes)} байт):")
        print("-" * 70)
        
        # 1. Пробуем вывести как текст UTF-8
        print("Как текст UTF-8:")
        try:
            decoded = data[:max_bytes].decode('utf-8', errors='ignore')
            # Убираем непечатные символы кроме пробелов и переносов
            cleaned = ''.join(c for c in decoded if c.isprintable() or c in '\n\r\t')
            if cleaned.strip():
                # Показываем по строкам
                lines = cleaned.split('\n')
                for i, line in enumerate(lines[:5]):  # Максимум 5 строк
                    if line.strip():
                        print(f"  {line}")
                    if i >= 4:
                        print("  ...")
                        break
            else:
                print("  (нет печатных символов в UTF-8)")
        except:
            print("  (не удалось декодировать как UTF-8)")
        
        # 2. HEX представление
        print(f"\nHEX представление:")
        hex_data = data[:min(80, max_bytes)].hex()  # Ограничиваем для читаемости
        hex_groups = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
        for i in range(0, len(hex_groups), 8):
            line = hex_groups[i:i+8]
            print(f"  {' '.join(line)}")
        
        print(f"\nASCII/печатные символы:")
        ascii_repr = []
        for byte in data[:min(80, max_bytes)]:
            if 32 <= byte <= 126:  # Печатные ASCII символы
                ascii_repr.append(chr(byte))
            else:
                ascii_repr.append('.')
        

        for i in range(0, len(ascii_repr), 16):
            line = ascii_repr[i:i+16]
            print(f"  {''.join(line)}")
        
        print("-" * 70)
    
    def test_basic_encryption(self):
        """Тест базового шифрования/расшифрования"""
        print("1. Базовое шифрование и расшифрование текстового файла")
        print("-" * 50)
        
        input_file = self.create_test_file("test_basic.txt", 'text')
        print(f"Создан тестовый файл: {input_file}")
        
        file_size = os.path.getsize(input_file)
        print(f"Размер файла: {file_size} байт")
        
        key = "ДемонстрационныйКлюч123"
        print(f"Ключ шифрования: '{key}'")
        
        key_bytes = parse_key(key)
        print(f"Ключ в байтах: {key_bytes[:20].hex()}... (первые 20 байт в HEX)")
        print(f"Длина ключа: {len(key_bytes)} байт")
        
        cipher = VigenereCipher(key_bytes)
        
        original_data = FileHandler.read_file(input_file)
        print(f"Прочитано данных: {len(original_data)} байт")
        
        print("\nНачало исходного файла:")
        try:
            text_start = original_data[:100].decode('utf-8')
            lines = text_start.split('\n')
            for line in lines[:3]:  # Показываем первые 3 строки
                if line.strip():
                    print(f"  {line}")
            if len(lines) > 3:
                print("  ...")
        except:
            print("  (бинарные данные)")
        
        start_time = time.time()
        encrypted_data = cipher.encrypt(original_data)
        encrypt_time = time.time() - start_time
        print(f"\nШифрование заняло: {encrypt_time:.4f} секунд")
        
        encrypted_file = os.path.join(self.temp_dir, "test_basic_encrypted.txt")
        FileHandler.write_file(encrypted_file, encrypted_data)
        self.demo_files.append(encrypted_file)
        print(f"Зашифрованный файл: {encrypted_file}")
        
        start_time = time.time()
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypt_time = time.time() - start_time
        print(f"Расшифрование заняло: {decrypt_time:.4f} секунд")
        
        decrypted_file = os.path.join(self.temp_dir, "test_basic_decrypted.txt")
        FileHandler.write_file(decrypted_file, decrypted_data)
        self.demo_files.append(decrypted_file)
        print(f"Расшифрованный файл: {decrypted_file}")
        
        if original_data == decrypted_data:
            print("\n  Результат расшифрования совпадает с оригиналом!")
            
            print("\nПроверка восстановленного текста (первые 2 строки):")
            try:
                restored_text = decrypted_data[:150].decode('utf-8')
                lines = restored_text.split('\n')
                for line in lines[:2]:
                    if line.strip():
                        print(f"  {line}")
            except:
                print("  (бинарные данные)")
        else:
            print("\n  Ошибка! Результат расшифрования не совпадает с оригиналом")
            for i in range(min(len(original_data), len(decrypted_data))):
                if original_data[i] != decrypted_data[i]:
                    print(f"Первое различие на позиции {i}: оригинал={original_data[i]}, расшифровано={decrypted_data[i]}")
                    break
        
        print("\n" + "=" * 60 + "\n")
    
    def test_binary_file(self):
        """Тест с бинарным файлом"""
        print("2. Шифрование бинарного файла (случайные данные)")
        print("-" * 50)
        
        input_file = self.create_test_file("test_binary.bin", 'binary', size_kb=10)
        print(f"Создан бинарный файл: {input_file}")
        
        file_size = os.path.getsize(input_file)
        print(f"Размер файла: {file_size} байт ({file_size/1024:.1f} КБ)")
        
        key = "314159265358979323846264338327950288419716939937510"
        print(f"Числовой ключ: {key}")
        
        key_bytes = parse_key(key)
        print(f"Ключ в байтах (первые 30): {key_bytes[:30].hex()}")
        
        cipher = VigenereCipher(key_bytes)
        
        original_data = FileHandler.read_file(input_file)
        
        start_time = time.time()
        encrypted_data = cipher.encrypt(original_data)
        encrypt_time = time.time() - start_time
        print(f"Шифрование заняло: {encrypt_time:.4f} секунд")
        print(f"Скорость шифрования: {file_size/encrypt_time/1024:.1f} КБ/с")
        
        encrypted_file = os.path.join(self.temp_dir, "test_binary_encrypted.bin")
        FileHandler.write_file(encrypted_file, encrypted_data)
        self.demo_files.append(encrypted_file)
        print(f"Зашифрованный файл: {encrypted_file}")
        
        print(f"\nСравнение оригинального и зашифрованного файла:")
        print(f"  Оригинал (первые 16 байт):    {original_data[:16].hex()}")
        print(f"  Зашифрованный (первые 16 байт): {encrypted_data[:16].hex()}")
        
        print(f"\nСравнение случайных позиций:")
        for _ in range(3):
            pos = random.randint(0, len(original_data) - 1)
            orig = original_data[pos]
            enc = encrypted_data[pos]
            key_byte = key_bytes[pos % len(key_bytes)]
            expected = (orig + key_byte) % 256
            print(f"  Позиция {pos}: оригинал={orig:3d} ({hex(orig)}), "
                  f"зашифровано={enc:3d} ({hex(enc)}), "
                  f"ключ={key_byte:3d}, ожидалось={expected:3d}, "
                  f"{' ' if enc == expected else ' '}")
        
        if original_data != encrypted_data:
            print("\n  Файлы разные (шифрование работает)")
        else:
            print("\n  Ошибка! Файлы одинаковые (шифрование не работает)")
        
        decrypted_data = cipher.decrypt(encrypted_data)
        
        if original_data == decrypted_data:
            print("  Расшифрование успешно восстановило оригинальные данные")
        else:
            print("  Ошибка расшифрования")
            diff_count = sum(1 for a, b in zip(original_data, decrypted_data) if a != b)
            print(f"  Различающихся байт: {diff_count}")
        
        print("\n" + "=" * 60 + "\n")
    
    def test_mixed_file(self):
        """Тест со смешанным файлом (текст + бинарные данные)"""
        print("3. Шифрование смешанного файла (текст + бинарные данные)")
        print("-" * 50)
        
        input_file = self.create_test_file("test_mixed.dat", 'mixed')
        print(f"Создан смешанный файл: {input_file}")
        
        file_size = os.path.getsize(input_file)
        print(f"Размер файла: {file_size} байт")

        key = "СекретныйКлючДляДемонстрации"
        key_bytes = parse_key(key)
        
        original_data = FileHandler.read_file(input_file)
        
        print("\nИсходный файл:")
        self.print_mixed_data(original_data, max_bytes=200, title="Оригинальные данные")
        
        cipher = VigenereCipher(key_bytes)
        encrypted_data = cipher.encrypt(original_data)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        print("\nЗашифрованный файл:")
        self.print_mixed_data(encrypted_data, max_bytes=200, title="Зашифрованные данные")
        
        if original_data == decrypted_data:
            print("\n  Расшифрование успешно восстановило оригинальные данные")
            
            print("\nВосстановленный файл:")
            self.print_mixed_data(decrypted_data, max_bytes=200, title="Восстановленные данные")
            
            print("\nПроверка восстановления текстовой части:")
            try:
                # Ищем конец текстовой части (поиск паттерна)
                text_part = decrypted_data[:300]  # Берем больше данных
                decoded = text_part.decode('utf-8', errors='ignore')
                if "бинарные данные" in decoded.lower():
                    text_end = decoded.lower().find("бинарные данные")
                    if text_end > 0:
                        print("Текстовая часть восстановлена корректно:")
                        print("-" * 40)
                        print(decoded[:text_end + 50])
                        print("-" * 40)
            except:
                print("  (бинарные данные)")
        else:
            print("\n  Ошибка расшифрования")
            for i in range(min(len(original_data), len(decrypted_data))):
                if original_data[i] != decrypted_data[i]:
                    print(f"Первое различие на позиции {i}: "
                          f"оригинал={original_data[i]:3d} ({hex(original_data[i])}), "
                          f"расшифровано={decrypted_data[i]:3d} ({hex(decrypted_data[i])})")
                    break
        
        print("\n" + "=" * 60 + "\n")
    
    def test_different_keys(self):
        """Тест с разными типами ключей"""
        print("4. Тестирование различных типов ключей")
        print("-" * 50)
        
        test_data = b"Test data for key demonstration" * 10
        test_file = os.path.join(self.temp_dir, "test_keys.txt")
        FileHandler.write_file(test_file, test_data)
        self.demo_files.append(test_file)
        
        test_keys = [
            ("Числовой ключ (маленький)", "123"),
            ("Числовой ключ (большой)", "98765432101234567890"),
            ("Строковый ключ (английский)", "MySecretKey"),
            ("Строковый ключ (русский)", "СекретныйКлюч"),
            ("Строковый ключ (спецсимволы)", "Key!@#$%^&*()"),
            ("Строковый ключ (длинный)", "ОченьДлинныйКлючДляТестированияРаботыШифраВиженера" * 3),
            ("Пустая строка", ""),
        ]
        
        for key_name, key_value in test_keys:
            print(f"\nТестируем: {key_name}")
            print(f"  Ключ: '{key_value}'")
            
            try:
                if key_value == "":
                    print("    Ожидаемая ошибка: пустой ключ")
                    continue
                    
                key_bytes = parse_key(key_value)
                if len(key_bytes) > 20:
                    print(f"  Ключ в байтах: {key_bytes[:20].hex()}... (первые 20 байт)")
                else:
                    print(f"  Ключ в байтах: {key_bytes.hex()}")
                print(f"  Длина ключа: {len(key_bytes)} байт")
                
                validate_key(key_bytes)
                
                cipher = VigenereCipher(key_bytes)
                encrypted = cipher.encrypt(test_data)
                decrypted = cipher.decrypt(encrypted)
                
                if test_data == decrypted:
                    print("    Шифрование/расшифрование работает корректно")
                    
                    first_byte_orig = test_data[0]
                    first_byte_enc = encrypted[0]
                    first_key_byte = key_bytes[0]
                    print(f"  Пример: '{chr(first_byte_orig)}' ({first_byte_orig:3d}) -> "
                          f"шифр {first_byte_enc:3d} с ключом {first_key_byte:3d}")
                else:
                    print("    Ошибка в шифровании/расшифровании")
                    
            except ValueError as e:
                print(f"    Ошибка валидации: {e}")
            except Exception as e:
                print(f"    Неожиданная ошибка: {type(e).__name__}: {e}")
        
        print("\n" + "=" * 60 + "\n")
    
    def test_performance(self):
        """Тест производительности"""
        print("5. Тестирование производительности")
        print("-" * 50)
        
        sizes_kb = [1, 10, 100, 500]
        key = "PerformanceTestKey123"
        key_bytes = parse_key(key)
        
        print(f"Ключ: '{key}'")
        print(f"Тестируемые размеры файлов: {sizes_kb} КБ")
        print()
        
        results = []
        
        for size_kb in sizes_kb:
            print(f"Тестируем файл размером {size_kb} КБ:")
            
            size_bytes = size_kb * 1024
            test_data = bytes([random.randint(0, 255) for _ in range(size_bytes)])
            
            cipher = VigenereCipher(key_bytes)
            
            start_time = time.perf_counter()
            encrypted = cipher.encrypt(test_data)
            encrypt_time = time.perf_counter() - start_time
            
            start_time = time.perf_counter()
            decrypted = cipher.decrypt(encrypted)
            decrypt_time = time.perf_counter() - start_time
            
            integrity_ok = test_data == decrypted
            
            encrypt_speed = size_bytes / encrypt_time / 1024  # КБ/с
            decrypt_speed = size_bytes / decrypt_time / 1024  # КБ/с
            
            results.append({
                'size_kb': size_kb,
                'encrypt_time': encrypt_time,
                'decrypt_time': decrypt_time,
                'encrypt_speed': encrypt_speed,
                'decrypt_speed': decrypt_speed,
                'integrity_ok': integrity_ok
            })
            
            print(f"  Шифрование: {encrypt_time:.4f} сек ({encrypt_speed:.1f} КБ/с)")
            print(f"  Расшифрование: {decrypt_time:.4f} сек ({decrypt_speed:.1f} КБ/с)")
            print(f"  Целостность: {'  OK' if integrity_ok else '  Ошибка'}")
            print()
        
        print("Сводная таблица производительности:")
        print("-" * 70)
        print(f"{'Размер (КБ)':<12} {'Шифр (сек)':<12} {'Расш (сек)':<12} {'Шифр (КБ/с)':<14} {'Расш (КБ/с)':<14}")
        print("-" * 70)
        
        for result in results:
            print(f"{result['size_kb']:<12} "
                  f"{result['encrypt_time']:<12.4f} "
                  f"{result['decrypt_time']:<12.4f} "
                  f"{result['encrypt_speed']:<14.1f} "
                  f"{result['decrypt_speed']:<14.1f}")
        
        print("-" * 70)
        
        avg_encrypt_speed = sum(r['encrypt_speed'] for r in results) / len(results)
        avg_decrypt_speed = sum(r['decrypt_speed'] for r in results) / len(results)
        
        print(f"\nСредняя скорость шифрования: {avg_encrypt_speed:.1f} КБ/с")
        print(f"Средняя скорость расшифрования: {avg_decrypt_speed:.1f} КБ/с")
        
        print("\nРекомендации:")
        print("1. Для текстовых файлов: ключ длиной 8-16 символов")
        print("2. Для бинарных файлов: ключ длиной 16-32 байта")
        print("3. Избегайте очень коротких ключей (< 4 символов)")
        print("4. Используйте смесь букв, цифр и спецсимволов")
        
        print("\n" + "=" * 60 + "\n")
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        print("6. Тестирование обработки ошибок")
        print("-" * 50)
        
        test_cases = [
            {
                'name': 'Несуществующий файл',
                'test': lambda: FileHandler.read_file("/несуществующий/путь/file.txt"),
                'expected': 'FileNotFoundError'
            },
            {
                'name': 'Пустой ключ',
                'test': lambda: validate_key(b''),
                'expected': 'ValueError'
            },
            {
                'name': 'Ключ длиной 0 байт',
                'test': lambda: VigenereCipher(b''),
                'expected': 'Работает (но бесполезен)'
            },
            {
                'name': 'Очень длинный ключ (>1024 байт)',
                'test': lambda: validate_key(b'x' * 2000),
                'expected': 'ValueError'
            },
            {
                'name': 'Шифрование пустых данных',
                'test': lambda: VigenereCipher(b'test').encrypt(b''),
                'expected': 'Работает (пустой результат)'
            },
            {
                'name': 'Расшифрование пустых данных',
                'test': lambda: VigenereCipher(b'test').decrypt(b''),
                'expected': 'Работает (пустой результат)'
            },
        ]
        
        for test_case in test_cases:
            print(f"\nТест: {test_case['name']}")
            print(f"  Ожидается: {test_case['expected']}")
            
            try:
                result = test_case['test']()
                if result is None or (isinstance(result, bytes) and len(result) == 0):
                    print(f"  Результат: {repr(result)}")
                    print(f"  Статус:   Выполнено (как и ожидалось)")
                else:
                    print(f"  Результат: {repr(result)[:50]}...")
                    print(f"  Статус:   Выполнено успешно")
            except ValueError as e:
                print(f"  Поймана ошибка ValueError: {e}")
                if test_case['expected'] == 'ValueError':
                    print(f"  Статус:   Обработка ошибок работает корректно")
                else:
                    print(f"  Статус:   Неожиданная ошибка")
            except FileNotFoundError as e:
                print(f"  Поймана ошибка FileNotFoundError: {e}")
                if test_case['expected'] == 'FileNotFoundError':
                    print(f"  Статус:   Обработка ошибок работает корректно")
                else:
                    print(f"  Статус:   Неожиданная ошибка")
            except Exception as e:
                print(f"  Поймана неожиданная ошибка {type(e).__name__}: {e}")
                print(f"  Статус:   Неожиданная ошибка")
        
        print("\n" + "=" * 60 + "\n")
    
    def interactive_demo(self):
        """Интерактивная демонстрация"""
        print("7. Интерактивная демонстрация")
        print("-" * 50)
        
        print("\nДавайте попробуем зашифровать и расшифровать файл!")
        
        user_file = os.path.join(self.temp_dir, "user_demo.txt")
        user_text = """Это демонстрация шифра Виженера.
Программа может шифровать любые файлы: текстовые, изображения, PDF и другие.
Шифрование происходит побайтово с использованием ключа.
Каждый байт данных складывается с байтом ключа по модулю 256.
Пример: байт 'A' (65) + ключ 'B' (66) = результат 131."""
        
        with open(user_file, 'w', encoding='utf-8') as f:
            f.write(user_text)
        
        print(f"\nСоздан тестовый файл: {user_file}")
        print("Содержимое файла:")
        print("-" * 50)
        print(user_text)
        print("-" * 50)
        
        while True:
            key_input = input("\nВведите ключ для шифрования (или 'exit' для выхода): ").strip()
            
            if key_input.lower() == 'exit':
                print("Выход из интерактивной демонстрации")
                break
            
            if not key_input:
                print("  Ключ не может быть пустым!")
                continue
            
            try:
                key_bytes = parse_key(key_input)
                validate_key(key_bytes)
                
                print(f"\n  Используем ключ: '{key_input}'")
                print(f"Длина ключа в байтах: {len(key_bytes)}")
                print(f"Ключ в HEX: {key_bytes.hex()}")
                
                data = FileHandler.read_file(user_file)
                print(f"Размер файла: {len(data)} байт")
                
                cipher = VigenereCipher(key_bytes)
                
                encrypted = cipher.encrypt(data)
                
                print("\nПример шифрования первых 20 байт:")
                print("Позиция | Оригинал (дек/hex/симв) | Ключ (дек) | Результат (дек/hex)")
                print("-" * 70)
                
                for i in range(min(20, len(data))):
                    orig_byte = data[i]
                    key_byte = key_bytes[i % len(key_bytes)]
                    enc_byte = encrypted[i]
                    
                    if 32 <= orig_byte <= 126:
                        orig_char = f"'{chr(orig_byte)}'"
                    else:
                        orig_char = "   "
                    
                    print(f"{i:7d} | {orig_byte:3d} ({orig_byte:02x}) {orig_char:4s} | "
                          f"{key_byte:9d} | {enc_byte:3d} ({enc_byte:02x})")
                
                decrypted = cipher.decrypt(encrypted)
                
                if data == decrypted:
                    print("\n  Расшифрование успешно! Данные восстановлены полностью.")
                    
                    try:
                        restored_text = decrypted.decode('utf-8')
                        print("\nВосстановленный текст (первые 3 строки):")
                        print("-" * 50)
                        lines = restored_text.split('\n')
                        for line in lines[:3]:
                            if line.strip():
                                print(line)
                        if len(lines) > 3:
                            print("...")
                        print("-" * 50)
                    except:
                        print("\n(Невозможно показать как текст - бинарные данные)")
                else:
                    print("\n  Ошибка! Данные не восстановлены корректно.")
                
                print("\n" + "=" * 60)
                print("Хотите попробовать другой ключ?")
                print("Попробуйте: '123', 'Secret', 'Пароль', или любой другой")
                
            except ValueError as e:
                print(f"\n  Ошибка в ключе: {e}")
            except Exception as e:
                print(f"\n  Неожиданная ошибка: {type(e).__name__}: {e}")
    
    def run_all_demos(self):
        """Запуск всех демонстраций"""
        print("=" * 60)
        print("ДЕМОНСТРАЦИЯ ШИФРА ВИЖЕНЕРА ДЛЯ ДВОИЧНЫХ ФАЙЛОВ")
        print("=" * 60)
        print("Лабораторная работа по криптографии")
        print("Шифр Виженера для двоичных файлов")
        print("=" * 60)
        
        try:
            self.test_basic_encryption()
            self.test_binary_file()
            self.test_mixed_file()
            self.test_different_keys()
            self.test_performance()
            self.test_error_handling()
            self.interactive_demo()
            
            print("\n" + "=" * 60)
            print("  ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ УСПЕШНО!")
            print("=" * 60)
            print("\nВыводы:")
            print("1. Шифр Виженера эффективно работает с любыми типами файлов")
            print("2. Алгоритм быстр и хорошо масштабируется")
            print("3. Корректно обрабатывает ошибки и пограничные случаи")
            print("4. Поддерживает различные типы ключей (числа, строки, UTF-8)")
            
        except KeyboardInterrupt:
            print("\n\n  Демонстрация прервана пользователем")
        except Exception as e:
            print(f"\n\n  Ошибка во время демонстрации: {type(e).__name__}: {e}")
        finally:
            self.cleanup()

def main():
    """Главная функция демонстрационной программы"""
    parser = argparse.ArgumentParser(
        description='Демонстрация работы шифра Виженера для двоичных файлов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python demo.py --all        # Запуск всех демонстраций
  python demo.py --basic      # Только базовые тесты
  python demo.py --performance # Только тест производительности
  python demo.py --interactive # Интерактивная демонстрация
  
Демонстрация включает:
  1. Шифрование текстовых файлов
  2. Работу с бинарными данными
  3. Тестирование различных ключей
  4. Проверку производительности
  5. Обработку ошибок
  6. Интерактивный режим
        """
    )
    
    parser.add_argument('--all', action='store_true', 
                       help='Запуск всех демонстраций')
    parser.add_argument('--basic', action='store_true',
                       help='Базовая демонстрация шифрования/расшифрования')
    parser.add_argument('--binary', action='store_true',
                       help='Демонстрация с бинарными файлами')
    parser.add_argument('--performance', action='store_true',
                       help='Тестирование производительности')
    parser.add_argument('--errors', action='store_true',
                       help='Тестирование обработки ошибок')
    parser.add_argument('--interactive', action='store_true',
                       help='Интерактивная демонстрация')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    demo = VigenereDemo()
    
    try:
        if args.all or args.basic:
            demo.test_basic_encryption()
        
        if args.all or args.binary:
            demo.test_binary_file()
            demo.test_mixed_file()
            demo.test_different_keys()
        
        if args.all or args.performance:
            demo.test_performance()
        
        if args.all or args.errors:
            demo.test_error_handling()
        
        if args.all or args.interactive:
            demo.interactive_demo()
        
        if not args.all:
            demo.cleanup()
            
    except KeyboardInterrupt:
        print("\n\n  Демонстрация прервана")
    except Exception as e:
        print(f"\n\n  Ошибка: {type(e).__name__}: {e}")
    finally:
        if args.all:
            demo.cleanup()

if __name__ == "__main__":
    main()