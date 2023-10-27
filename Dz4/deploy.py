from sshcheckout import ssh_checkout, upload_files

def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11", "/home/ub/PycharmProjects/pythonProject/Test/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    output, success = ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                                   "Настраивается пакет")
    if not success:
        print("Ошибка при выполнении команды dpkg:")
        print(output)  # Вывести вывод команды для диагностики

    res.append(ssh_checkout("0.0.0.0", "user2", "11", "echo '11' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    print(res)
    return all(res)

if deploy():
    print("Деплой успешен")
else:
    print("Ошибка деплоя")
