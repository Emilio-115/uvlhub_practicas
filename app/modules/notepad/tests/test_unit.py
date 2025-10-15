import pytest
from app import db
from app.modules.notepad.models import Notepad
from app.modules.auth.models import User
from app.modules.conftest import login, logout


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        notepad = Notepad(user_id=user_test.id, title="Test title",body="This is the testing body of the notepad")
        db.session.add(notepad)
        db.session.commit()

    yield test_client


def test_get_notepad_page(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Delete" in response.data, "The expected content is not present on the page"

    logout(test_client)


