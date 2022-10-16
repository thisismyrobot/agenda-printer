import datetime


class Task:
    def __init__(self, description, start_time, all_day):
        self._description = description
        self._start_time = start_time
        self._all_day = all_day

    def __hash__(self):
        return hash((
            self._description,
            self._start_time,
            self._all_day
        ))

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False

        return (other._description == self._description
            and other._start_time == self._start_time
            and other._all_day == self._all_day)

    @property
    def description(self):
        return self._description

    @property
    def start_time(self):
        return self._start_time

    @property
    def any_time(self):
        return self._all_day

    def __repr__(self):
        return f'{self._description} {self._start_time}'