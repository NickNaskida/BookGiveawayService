import requests

from src.core import utils


test_user_email = "admin@gmail.com"
test_user_password = "admin"


def authenticate():
    api_url = utils.get_api_url()

    r = requests.post(
        f"{api_url}/auth/jwt/login",
        data={"username": test_user_email, "password": test_user_password},
    )

    assert r.status_code == 200
    assert r.json()["access_token"]

    return r.json()["access_token"]

