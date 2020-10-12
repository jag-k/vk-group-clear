#!/usr/bin/env python3
from getpass import getpass
from warnings import filterwarnings
filterwarnings('ignore')

login = input("Введите свой логин от ВК: ")
password = getpass("Введите свой пароль: ")
group_id = int(input("Введите ID группы без `-` (НЕ ДОМЕН): "))

with open("config.ini", "w") as config:
    config.writelines((
        "[vk]\n",
        "login=%s\n" % login,
        "password=%s\n" % password,
        "group_id=%s\n" % group_id,
    ))

print("Данные записаны!")

from main import run_tasks

run_tasks()
