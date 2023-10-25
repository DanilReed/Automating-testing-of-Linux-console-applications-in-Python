import os
import time
import pytest
import yaml
from checkout import checkout

with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folder():
    return checkout(f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')
    # checkout(f'rm -r {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')
@pytest.fixture()
def make_files():
    return checkout(f'cd {data.get("folder_in")}; touch file1.txt file2.txt file3.txt', '')

# Функция для создания файла stat.txt, если его нет
def create_stat_file_if_not_exists(stat_file_path):
    if not os.path.exists(stat_file_path):
        with open(stat_file_path, "w") as stat_file:
            stat_file.write("timestamp\n")

@pytest.fixture()
def update_stat_file():
    try:
        # Определение пути к файлу `stat.txt` из конфигурации
        stat_file_path = data.get("stat_file_path")

        # Проверяем наличие файла и создаем, если он не существует
        create_stat_file_if_not_exists(stat_file_path)

        # Определяем текущее время
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Формируем строку для записи в файл
        stat_line = f"{current_time}"

        # Открываем файл stat.txt для записи и добавляем в него строку
        with open(stat_file_path, "a") as stat_file:
            stat_file.write(stat_line + '\n')
    except Exception as e:
        print(f"Failed to update stat file: {e}")


