import pytest
import sys
import os
import json
from typing import Any
from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_config import get_db
from router.users_router import router


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py



def start_application():
    app = FastAPI()
    app.include_router(router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./db/local_sqlite/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create an app instance
    """
    _app = start_application()
    yield _app



@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


def test_tc0001_get_all(client):
    td_first_record = 0
    td_role = "villian"
    td_id = 1
    td_username = "darth.vader"
    td_email = "darth.vader@gmail.com"
    td_expected_record_count = 3

    response = client.get(f"/users/v1")

    assert response.status_code == 200
    assert response.json()[td_first_record]["id"] == td_id
    assert response.json()[td_first_record]["role"] == td_role
    assert response.json()[td_first_record]["username"] == td_username
    assert response.json()[td_first_record]["email"] == td_email
    assert len(response.json()) == td_expected_record_count



def test_tc0002_get_by_username(client):
    td_role = "villian"
    td_id = 1
    td_username = "darth.vader"
    td_email = "darth.vader@gmail.com"

    response = client.get(f"/users/v1/{td_username}")

    assert response.status_code == 200
    assert response.json()["id"] == td_id
    assert response.json()["role"] == td_role
    assert response.json()["username"] == td_username
    assert response.json()["email"] == td_email


def test_tc0003_get_by_username(client):
    td_username = "this.is.bad"
    td_message = "username not found. Please check your parameter and try again"

    response = client.get(f"/users/v1/{td_username}")

    assert response.status_code == 404
    assert response.json()["detail"] == td_message


def test_tc0004_post(client):
    td_role = "hero"
    td_username = "bat.man"
    td_email = "batman@gmail.com"
    td_header_location = "users/v1/bat.man"


    response = client.post("/users/v1", data=json.dumps(dict(
        username=td_username,
        email=td_email,
        role=td_role
    )), content='application/json')


    assert response.status_code == 201
    assert response.headers["Location"] == td_header_location
    assert response.json()["username"] == td_username
    assert response.json()["email"] == td_email
    assert response.json()["role"] == td_role

    get_response = client.get(f'/users/v1/{td_username}')
    
    assert isinstance(get_response.json()["id"], int)

    assert get_response.json()["username"] == td_username
    assert get_response.json()["email"] == td_email
    assert get_response.json()["role"] == td_role


def test_tc0005_post_empty_username(client):
    td_username = ""
    td_email = ""
    td_role = ""
    td_message = "username field cannot be empty. Please check your payload and try again"

    response = client.post('/users/v1/', data=json.dumps(dict(
        username=td_username,
        email=td_email,
        role=td_role
    )), content='application/json')

    assert response.status_code == 400
    assert response.json()["detail"] == td_message


def test_tc0006_post_empty_email(client):
    td_username = "test"
    td_email = ""
    td_role = ""
    td_message = "email field cannot be empty. Please check your payload and try again"

    response = client.post('/users/v1/', data=json.dumps(dict(
        username=td_username,
        email=td_email,
        role=td_role
    )), content='application/json')

    assert response.status_code == 400
    assert response.json()["detail"] == td_message


def test_tc0007_post_empty_role(client):
    td_username = "test"
    td_email = "role@gmail.com"
    td_role = ""
    td_message = "role field cannot be empty. Please check your payload and try again"

    response = client.post('/users/v1/', data=json.dumps(dict(
        username=td_username,
        email=td_email,
        role=td_role
    )), content='application/json')

    assert response.status_code == 400
    assert response.json()["detail"] == td_message


def test_tc0008_put(client):
    td_id = 1
    td_role = "test_role"
    td_username = "darth.vader"
    td_email = "test@gmail.com"
    td_payload = '{"email": "test@gmail.com", "role": "test_role" }'

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')
  
    assert response.status_code == 204 
    
    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.json()["id"] == td_id
    assert get_response.json()["username"] == td_username
    assert get_response.json()["email"] == td_email
    assert get_response.json()["role"] == td_role


def test_tc0009_put_update_email(client):
    td_id = 2
    td_role = "hero"
    td_username = "thor.odinson"
    td_email = "thor.odinson@gmail.com"
    td_payload = '{"email": "thor.odinson@gmail.com"}'

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')    

    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.json()["id"] == td_id
    assert get_response.json()["username"] == td_username
    assert get_response.json()["email"] == td_email
    assert get_response.json()["role"] == td_role


def test_tc0010_put_update_role(client):
    td_id = 3
    td_role = "college student"
    td_username = "jason.pham"
    td_email = "jason@gmail.com"
    td_payload = '{"role": "college student"}'

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')    

    get_response = client.get(f'/users/v1/{td_username}')

    assert get_response.json()["id"] == td_id
    assert get_response.json()["username"] == td_username
    assert get_response.json()["email"] == td_email
    assert get_response.json()["role"] == td_role


def test_tc0011_no_body(client):
    td_username = "darth.vader"
    td_payload = '{}'
    td_message = "request body cannot be empty. Please check your payload and try again"

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')    

    assert response.status_code == 400
    assert response.json()["detail"] == td_message


def test_tc0012_put_bad_username(client):
    td_username = "this.not.found"
    td_payload = '{"email": "test@gmail.com", "role": "test_role" }'
    td_message = "username not found. Please use Post to create a user record"

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')    

    assert response.status_code == 404
    assert response.json()["detail"] == td_message


def test_tc0013_empty_fields(client):
    td_username = "darth.vader"
    td_payload = '{"email": "", "role": "" }'
    td_message = "request body fields cannot be empty. Please check your payload and try again"

    response = client.put('/users/v1/' + td_username, data=td_payload, content='application/json')    

    assert response.status_code == 400
    assert response.json()["detail"] == td_message


def test_tc0014_delete(client):
    td_username = "delete.user"
    td_email = "delete@gmail.com"
    td_role = "tester"

    response = client.post('/users/v1', data=json.dumps(dict(
        username=td_username,
        email=td_email,
        role=td_role
    )), content='application/json')
  
    response = client.delete('/users/v1/' + td_username)
    assert response.status_code == 204


    td_message = "username not found. Please check your parameter and try again"

    response = client.get(f"/users/v1/{td_username}")

    assert response.status_code == 404
    assert response.json()["detail"] == td_message
