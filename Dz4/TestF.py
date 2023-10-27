import pytest
from checkout import checkout
import yaml
from checkout import getout
from sshcheckout import ssh_checkout, upload_files


with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)

class TestPositive:
    archive_type = data.get("archive_type")
    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(getout("journalctl --since '{}'".format(starttime)))

    def test_step1(self, start_time):
        res = []
        upload_files(data["ip"], data["user"], data["passwd"],
                     "/home/ub/PycharmProjects/pythonProject/Test/p7zip-full.deb",
                     f"/home/{data['user']}/{data['pkgname']}.deb")
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -i /home/{data['user']}/{data['pkgname']}.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -s {data['pkgname']}",
                                "Status: install ok installed"))

        self.save_log(start_time, "log1.txt")
        return all(res)

    def test_step2(self, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],"cat /etc/os-release", "jammy"), "Test-2 Fail"
        self.save_log(start_time, "log2.txt")

    def test_step3(self, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],"cat /etc/os-release", "22.04.1"), "Test-3 Fail"
        self.save_log(start_time, "log3.txt")

    def test_step4(self, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],"cat /etc/os-release", "NAME"), "Test-4 Fail"
        self.save_log(start_time, "log4.txt")

    def test_step5(self, make_folder, make_files, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],f'cd {data.get("folder_in")}; 7z a -t{self.archive_type} {data.get("folder_out")}apxuv', "Ok"), "Test-5 Fail"
        self.save_log(start_time, "log5.txt")

    def test_step6(self, make_folder, make_files, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],f'cd {data.get("folder_out")}; 7z x -t{self.archive_type} ./apxuv.7z', "Ok"), "Test-6 Fail"
        self.save_log(start_time, "log6.txt")

    def test_step7(self, make_folder, make_files, start_time):
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],f'cd {data.get("folder_out")}; 7z d -t{self.archive_type} ./apxuv.7z file1.txt', "Ok"), "Test-7 Fail"
        self.save_log(start_time, "log7.txt")

    def test_step8(self, make_folder, make_files, start_time):
        command = f'cd {data.get("folder_out")}; 7z l -t{self.archive_type} ./apxuv.7z'
        result = checkout(command, "")
        print(result)
        self.save_log(start_time, "log8.txt")

    def test_step9(self, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -r /home/{data['user']}/{data['pkgname']}.deb",
                                "Удаляется"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -s {data['pkgname']}",
                                "Status: deinstall ok"))
        self.save_log(start_time, "log9.txt")
        assert all(res), "test9 FAIL"



class TestNegativ:
    archive_type = data.get("archive_type")

    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(getout("journalctl --since '{}'".format(starttime)))

    def test_neg_step1(self, start_time):
        res = []
        upload_files(data["ip"], data["user"], data["passwd"],
                     "/home/ub/PycharmProjects/pythonProject/Test/p7zip-full.deb",
                     f"/home/{data['user']}/{data['pkgname']}.deb")
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -i /home/{data['user']}/{data['pkgname']}.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -s {data['pkgname']}",
                                "Status: install ok installed"))

        self.save_log(start_time, "log1.txt")
        return all(res)

    def test_neg_step2(self, start_time): #Checking for input data errors
        assert not ssh_checkout(data["ip"], data["user"], data["passwd"],"cat /etc/os-release", "27.305.8"), "Test-2 Fail"
        self.save_log(start_time, "log2.txt")

    def test_neg_step3(self, make_folder, make_files, start_time): #Checking for invalid command parameters
        assert not ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f'cd {data.get("folder_in")}; RAR a -t{self.archive_type} {data.get("folder_out")}apxuv',
                            "Ok"), "Test-3 Fail"
        self.save_log(start_time, "log5.txt")

    def test_neg_step4(self, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -r /home/{data['user']}/{data['pkgname']}.deb",
                                "Удаляется"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"echo '{data['passwd']}' | sudo -S dpkg -s {data['pkgname']}",
                                "Status: deinstall ok"))
        self.save_log(start_time, "log9.txt")
        assert all(res), "test4 FAIL"

if __name__ == "__main__":
    pytest.main(["-vv", "--setup-show"])