import datetime

from agenda.domain import Task


def test_tasks_are_only_unique_by_name():
    tasks = set([
        Task('Do something', datetime.time(11, 15, 13), False),
        Task('Do something', datetime.time(11, 15, 13), False),
        Task('Do something else', datetime.time(11, 15, 13), False),
        Task('Do something else again', datetime.time(0, 0, 0), False),
        Task('Do something else again', datetime.time(0, 0, 0), True),
        Task('Do something else again', datetime.time(0, 0, 0), True),
    ])

    assert len(tasks) == 4
