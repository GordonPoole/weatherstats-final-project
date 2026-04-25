import io
import pytest

from web_app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        yield client


def login(client, password="wrongpassword"):
    return client.post(
        "/login",
        data={
            "username": "admin",
            "password": password
        },
        follow_redirects=True
    )


def test_login_success(client):
    response = login(client)

    assert response.status_code == 200
    assert b"Upload" in response.data or b"CSV" in response.data


def test_login_failure(client):
    response = login(client, password="badpassword")

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data


def test_upload_csv_after_login(client):
    login(client)

    data = {
        "file": (
            io.BytesIO(
                b"Location,MinTemp,MaxTemp,Rainfall,Humidity3pm\nSydney,10,25,2,60"
            ),
            "weather.csv"
        )
    }

    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"WeatherStats" in response.data


def test_city_insights(client):
    login(client)

    with client.session_transaction() as sess:
        sess["uploaded_file"] = "uploaded_weather.csv"

    response = client.get("/city_insights?city=Sydney")

    assert response.status_code == 200


def test_logout(client):
    login(client)

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data