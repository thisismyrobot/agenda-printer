import sys

import hupper
import waitress


def serve(args=sys.argv[1:]):
    """Run waitress, but reload with file system changes."""
    if '--reload' in args:
        reloader = hupper.start_reloader('test_server.serve')

    import agenda

    agenda.app.debug = True

    # Allow for template changes without manual restart.
    agenda.app.jinja_env.auto_reload = True

    waitress.serve(
        agenda.app,
        host='0.0.0.0',
        port=5000,
    )


if __name__ == '__main__':
    serve()
