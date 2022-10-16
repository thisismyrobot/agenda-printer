import datetime

import mock

from agenda.domain import Task


@mock.patch('agenda.services.calendar.event_tasks', lambda: sample_tasks())
@mock.patch('agenda.bom_xml', lambda: open('tests/forecast.xml').read())
def test_full_day_print(webapp):
    output = webapp.get('/print').text
    assert output == """--------------------------------

\x1bE\x01Good Morning!\x1bE\x00

Expect a max of 19 C, possible
shower.

\x1bE\x01Today:\x1bE\x00
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 00:15 TEST: Daily odd...
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 11:30 Dev Day
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Daily repeat
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Daily repeat...
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Span 1
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Span 2
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Span 3
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Today once-off
\x1d!1\x1b%\x01A\x1b%\x00\x1d!\x00 TEST: Weekly repeat

--------------------------------



"""


@mock.patch('agenda.services.calendar.event_tasks', lambda: [])
@mock.patch('agenda.bom_xml', lambda: open('tests/forecast.xml').read())
def test_full_day_print_no_tasks(webapp):
    output = webapp.get('/print').text
    assert output == """--------------------------------

\x1bE\x01Good Morning!\x1bE\x00

Expect a max of 19 C, possible
shower.

No TODOs today :)

--------------------------------



"""


def sample_tasks():
    return [
        Task('Dev Day', datetime.time(11, 30, 0), False),
        Task('TEST: Daily odd repeat with time', datetime.time(0, 15, 0), False),
        Task('TEST: Daily repeat', datetime.time(0, 0, 0), True),
        Task('TEST: Daily repeat starts today', datetime.time(0, 0, 0), True),
        Task('TEST: Span 1', datetime.time(0, 0, 0), True),
        Task('TEST: Span 2', datetime.time(0, 0, 0), True),
        Task('TEST: Span 3', datetime.time(0, 0, 0), True),
        Task('TEST: Today once-off', datetime.time(0, 0, 0), True),
        Task('TEST: Weekly repeat', datetime.time(0, 0, 0), True),
    ]
