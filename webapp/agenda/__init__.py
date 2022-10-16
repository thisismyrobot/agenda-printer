import datetime
import io

import arrow
import flask

from agenda.services.printing.em5820 import EM5820
from agenda.services import calendar
from agenda.services.calendar import dynamictasks


UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'


app = flask.Flask(__name__)


@app.route('/')
def index():
    views = []
    errors = []
    for view in (intro, date, forecast, tasks):
        try:
            content = view()
            if content.strip() != '':
                views.append(content)
        except:
            errors.append(view.__name__)

    if len(errors) > 0:
        views.append(flask.render_template('errors.html', errors=errors))

    return '<br /><br />'.join(views)


@app.route('/print')
def print_data():
    html_page = index()
    printer_bytes = EM5820().print(html_page)
    return flask.send_file(
        io.BytesIO(printer_bytes),
        mimetype='application/octet-stream'
    )


@app.route('/intro.html')
def intro():
    return flask.render_template('intro.html')


@app.route('/date.html')
def date():
    local_now = arrow.now('Australia/Hobart')
    return flask.render_template(
        'date.html',
        day=local_now.strftime('%A'),
        date=local_now.format('Do')
    )


@app.route('/tasks.html')
def tasks():
    event_tasks = calendar.event_tasks()
    tasks = dynamictasks.update(event_tasks)

    task_viewmodels = []
    scheduled_tasks = [t for t in tasks if not t.any_time]
    any_time_tasks = [t for t in tasks if t.any_time]

    for task in sorted(scheduled_tasks, key=lambda t: t.start_time):
        task_viewmodels.append({
            'text': f'{task.start_time.hour:02}:{task.start_time.minute:02} {task.description}'
        })

    for task in sorted(any_time_tasks, key=lambda t: t.description):
        task_viewmodels.append({
            'text': task.description
        })

    return flask.render_template('tasks.html', tasks=task_viewmodels)


@app.route('/forecast.html')
def forecast():
    # You will have to use an API that works for where you are.
    precis = 'possible morning shower'
    max_temp = 23
    return flask.render_template('forecast.html', precis=precis.lower(), max_temp=max_temp)
