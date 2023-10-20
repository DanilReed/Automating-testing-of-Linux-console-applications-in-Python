import subprocess
import pytest
from checkout import checkout

folder_in = "/home/ub/in/"
folder_out = "/home/ub/out/"
folder_ext = "/home/ub/ext/"

def test_step1():
    assert checkout(f'cd {folder_in}; 7z a {folder_out}apxuv', "Ok"), "Test-1 Fail"

def test_step2():
    assert checkout( f'cd {folder_out}; 7z x ./apxuv.7z', "Ok"), "Test-3 Fail"

def test_step3():
    assert checkout( f'cd {folder_out}; 7z d ./apxuv.7z file1.txt', "Ok"), "Test-2 Fail"


def test_step4():
    command = f'cd {folder_out}; 7z l ./apxuv.7z'
    result = checkout(command, "")

    print(result)


def test_step5():
    # Ожидаемый хеш CRC32 для файла file2.txt
    expected_crc32 = "6FDB3795"

    # Выполняем команду для расчета хеша (h) для файла внутри архива
    result = checkout(f'cd {folder_out}; 7z h ./apxuv.7z file2.txt', "")

    # Парсим вывод, чтобы найти строку с хешем
    lines = result.split('\n')
    hash_line = None
    for line in lines:
        if "CRC32" in line:
            hash_line = line
            break

    assert hash_line is not None, "CRC32 hash not found in the output."

    # Извлекаем фактический хеш из строки
    actual_crc32 = hash_line.split()[-1]

    # Сравниваем ожидаемый и фактический хеши
    assert actual_crc32 == expected_crc32, "CRC32 hash does not match."
