import datetime

from agenda.domain import Task


def event_tasks():
    # You will need to get tasks for today from your calendar source, whatever
    # that is.
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tasks = [
        Task('Go to shops', today, True),
        Task('Haircut', today.replace(hour=11, minute=30), False),
        Task('Exercise', today, True)
    ]
    return tasks
