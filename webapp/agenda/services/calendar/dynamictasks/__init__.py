# Applies dynamic wording to matched tasks.
import datetime

from .tasks import walking_plan

DYNAMIC_TASKS = (
    walking_plan.WalkingPlan,
)


def update(tasks):
    updated_tasks = []
    for task in tasks:
        updated = False
        updated_task = None
        for dynamic_task in DYNAMIC_TASKS:
            updater = dynamic_task(task)
            updated = updater.process()
            if updated:
                updated_task = updater.updated_task
                break

        updated_tasks.append(updated_task if updated else task)

    return updated_tasks
