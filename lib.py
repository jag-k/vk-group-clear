from sys import stderr
from colorama import init, Style, Fore

from config import cfg
from vk_api import VkApi
from logging import basicConfig, debug, error
from datetime import date
from traceback import format_exc

today = date.today().isoformat()
basicConfig(filename="log-%s.log" % today, filemode="w", level=10)
init(True)
TASKS = []

# == VK API ==
vk_session = VkApi(
    login=cfg.get("vk", "login"), password=cfg.get("vk", "password"),
    # token=cfg.get("vk", "token")
)
vk_session.auth()
api = vk_session.get_api()
GROUP_ID = int(cfg.get("vk", "group_id"))


# == TASKS ==
def task(name: str):
    def decorator(func):
        TASKS.append((name, func))
        return func
    return decorator


def print_count(name: str, func_i: int, total_count: int, now_step: int):
    color = Fore.YELLOW
    end = ''
    if total_count <= now_step:
        color = Fore.GREEN
        end = '\n'
        count = Style.BRIGHT + " DONE!"
    elif total_count > 0:
        count = ": %d из %d" % (now_step, total_count)
    else:
        count = "..."

    print("\r" + color + "%d. Выполнение задачи '%s'%s" % (
        func_i + 1, name, count
    ), end=end, flush=True)


def run_tasks():
    print(Fore.GREEN + "Количество задач: %d" % len(TASKS))
    for i in range(len(TASKS)):
        t_name, t_func = TASKS[i]
        iterator = t_func()
        total_count = next(iterator)
        counter = 0
        print_count(t_name, i, total_count, counter)

        run = True
        while run:
            try:
                debug(next(iterator))
                counter += 1
                print_count(t_name, i, total_count, counter)
            except StopIteration:
                run = False
            except BaseException as err:
                print("\r")
                print("Ошибка! %s: %s" % (type(err).__name__, err), file=stderr)
                error(format_exc())

    print(Fore.GREEN + "Все задачи выполнены!")


if __name__ == '__main__':
    run_tasks()
