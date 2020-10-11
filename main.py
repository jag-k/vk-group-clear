from pprint import pprint
from vk_api.vk_api import VkApiMethod

from lib import task, run_tasks, api, GROUP_ID, debug

user_id = api.account.getProfileInfo()["id"]
g: VkApiMethod = api.groups


@task("Закрытие группы")
def close_group():
    yield -1
    g.edit(
        group_id=GROUP_ID,
        access=2,
    )


@task("Удаление прав у модераторов")
def remove_managers():
    members = g.get_members(
        group_id=GROUP_ID,
        filter="managers"
    )
    yield members['count']
    for m in members['items']:
        m_id = m["id"]
        if m_id == user_id or m['role'] == "creator":
            yield
        else:
            g.edit_manager(
                group_id=GROUP_ID,
                user_id=m_id,

            )
            yield


@task("Получение пользователей")
def get_members():
    members = g.get_members(
        group_id=GROUP_ID,
    )
    yield members['count']
    for m in members['items']:
        if m == 173996641:
            yield m
        else:
            debug(m)
            yield g.removeUser(
                group_id=GROUP_ID,
                user_id=m
            )


@task("Удаление постов со стены")
def get_members():
    wall = api.wall.get(
        owner_id=-GROUP_ID,
        count=1,
    )
    max_count = wall['count']
    yield max_count
    for offset in range(0, max_count+1, 100):
        wall = api.wall.get(
            owner_id=-GROUP_ID,
            offset=offset,
            count=100
        )
        for w in wall['items']:
            yield api.wall.delete(
                owner_id=-GROUP_ID,
                post_id=w['id']
            )


@task("Удаление изображений")
def get_members():
    images = api.photos.getAll(
        owner_id=-GROUP_ID,
        count=1,
    )
    max_count = images['count']
    yield max_count
    for offset in range(0, max_count+1, 200):
        images = api.photos.getAll(
            owner_id=-GROUP_ID,
            offset=offset,
            count=200
        )
        for i in images['items']:
            yield api.photos.delete(
                owner_id=-GROUP_ID,
                photo_id=i['id']
            )


if __name__ == '__main__':
    run_tasks()
