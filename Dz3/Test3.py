import subprocess
import pytest
from checkout import checkout
import yaml
from conftest import update_stat_file
import os

with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)

class TestPositive:
    archive_type = data.get("archive_type")

    def test_step1(self):
        assert checkout("cat /etc/os-release", "jammy"), "Test-1 Fail"

    def test_step2(self):
        assert checkout("cat /etc/os-release", "22.04.1"), "Test-2 Fail"

    def test_step3(self):
        assert checkout("cat /etc/os-release", "NAME"), "Test-3 Fail"

    def test_step4(self, make_folder, make_files, update_stat_file,):
        assert checkout(f'cd {data.get("folder_in")}; 7z a -t {self.archive_type} {data.get("folder_out")}apxuv', "Ok"), "Test-4 Fail"

    def test_step5(self, make_folder, make_files, update_stat_file):
        assert checkout(f'cd {data.get("folder_out")}; 7z x -t {self.archive_type} ./apxuv.7z', "Ok"), "Test-5 Fail"

    def test_step6(self, make_folder, make_files, update_stat_file):
        assert checkout(f'cd {data.get("folder_out")}; 7z d -t {self.archive_type} ./apxuv.7z file1.txt', "Ok"), "Test-6 Fail"


    def test_step7(self, make_folder, make_files, update_stat_file):
        command = f'cd {data.get("folder_out")}; 7z l -t {self.archive_type} ./apxuv.7z'
        result = checkout(command, "")

        print(result)

if __name__ == "__main__":
    pytest.main(["-vv", "--setup-show"])