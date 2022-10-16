import sys

import flask_webtest
import httpretty
import pytest

# Allow imports
sys.path.insert(0, '.')
import agenda


@pytest.fixture
def webapp():
    testapp = flask_webtest.TestApp(agenda.app)
    testapp.app.debug = True
    return testapp


@pytest.fixture(scope='function', autouse=True)
def control_outgoing():
    httpretty.enable(verbose=True, allow_net_connect=False)
    yield
    httpretty.disable()
    httpretty.reset()
