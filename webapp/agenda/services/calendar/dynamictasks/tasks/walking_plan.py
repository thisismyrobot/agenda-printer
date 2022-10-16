# Walks a short distance on weekdays, a long distance on weekends, all based
# on seeing a task labelled "Exercise".
import datetime

from agenda.domain import Task


class WalkingPlan:
    def __init__(self, task):
        self._task = task
        self._updated_task = None

    @property
    def updated_task(self):
        return self._updated_task

    def process(self):
        if self._task.description != 'Exercise':
            return False

        is_weekend = datetime.date.today().isoweekday() in (6,7)
        description = f'Walk {5 if is_weekend else 3} km'
        self._updated_task = Task(
            description,
            self._task.start_time,
            self._task.any_time
        )
        return True
