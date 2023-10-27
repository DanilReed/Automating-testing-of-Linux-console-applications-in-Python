import time
import pytest
import yaml
from sshcheckout import ssh_checkout
import paramiko
from datetime import datetime

with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folder():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')
    # checkout(f'rm -r {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")}', '')
@pytest.fixture()
def make_files():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],f'cd {data.get("folder_in")}; touch file1.txt file2.txt file3.txt', '')

# Функция для создания файла stat.txt, если его нет
def create_stat_file_if_not_exists(ssh_client, stat_file_path):
    # Проверяем наличие файла и создаем, если он не существует
    stdin, stdout, stderr = ssh_client.exec_command(f'test -e {stat_file_path} || touch {stat_file_path}')

    # Проверяем статус выполнения команды
    if stdout.channel.recv_exit_status() == 0:
        return True
    else:
        return False

@pytest.fixture()
def update_stat_file(data):
    try:
        # Создаем SSH-клиент
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся к удаленному серверу
        ssh_client.connect(hostname=data["ip"], username=data["user"], password=data["passwd"])

        # Определение пути к файлу `stat.txt` из конфигурации
        stat_file_path = data.get("stat_file_path")

        # Проверяем наличие файла и создаем, если он не существует
        if not create_stat_file_if_not_exists(ssh_client, stat_file_path):
            print(f"Failed to create {stat_file_path}")

        # Определяем текущее время
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Формируем строку для записи в файл
        stat_line = f"{current_time}"

        # Открываем файл stat.txt для записи и добавляем в него строку
        stdin, stdout, stderr = ssh_client.exec_command(f'echo "{stat_line}" >> {stat_file_path}')

        # Проверяем статус выполнения команды
        if stdout.channel.recv_exit_status() != 0:
            print("Failed to update stat file")

        # Закрываем SSH-соединение
        ssh_client.close()
    except Exception as e:
        print(f"Failed to update stat file: {e}")

@pytest.fixture()
def start_time():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

