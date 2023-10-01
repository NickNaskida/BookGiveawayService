import pytest
import requests

from src.core import utils
from tests.utils.auth import authenticate
from tests.utils.random_data import random_author


def post_to_add_author(name, auth_token=None):
    url = utils.get_api_url()
    r = requests.post(
        f"{url}/authors", json={"full_name": name},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return r


def get_author_by_id(author_id):
    url = utils.get_api_url()
    r = requests.get(f"{url}/authors/{author_id}")
    return r


@pytest.mark.usefixtures("restart_api")
def test_get_all_authors():
    url = utils.get_api_url()
    r = requests.get(f"{url}/authors")
    assert r.status_code == 200
    assert len(r.json()) > 0


@pytest.mark.usefixtures("restart_api")
def test_create_author():
    auth_token = authenticate()

    name = random_author()
    post_r = post_to_add_author(name, auth_token)
    assert post_r.status_code == 201
    assert post_r.json()["full_name"] == name

    get_r = get_author_by_id(post_r.json()["id"])
    assert get_r.status_code == 200
    assert get_r.json()["full_name"] == name


@pytest.mark.usefixtures("restart_api")
def test_create_author_unauthorized():
    name = random_author()
    post_r = post_to_add_author(name)
    assert post_r.status_code == 401
    assert post_r.json()["detail"] == "Unauthorized"


# Other tests
