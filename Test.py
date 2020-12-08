import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def login(client, email, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)



# def test_acceptingPickupTime.py():


# def test_changingUserPassword.py():


# def test_editUserInformation.py():


def test_login.py():
	rv = login(client, app.app.config['USERNAME'], app.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'] + 'x', flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


# def test_org_login.py():


# def test_rejectingPickupTime.py():


# def test_testchangingOrgPassword.py():


# def test_user_login.py():


# def test_user_profile.py():


# def test_viewOrganizationProfileAsUser.py():


# def test_viewOrganizationProfileLoggedOut.py():