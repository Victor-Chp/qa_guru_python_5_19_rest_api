from pprint import pprint
import requests
from requests import Response


url = "https://reqres.in/api/"
url_users = url + "users"
url_resources = url + "unknown"
url_reg = url + "register"
url_login = url + "login"


def test_single_user():
    id = 2
    response: Response = requests.get(f'{url_users}/{id}')

    assert response.status_code == 200
    assert response.json()['data']['id'] == id


def test_list_resources():
    response: Response = requests.get(url_resources)

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] != ''
    assert response.json()['data'][0]['name'] != ''


def test_single_resource():
    id = 2
    response: Response = requests.get(f'{url_resources}/{id}')

    assert response.status_code == 200
    assert response.json()['data']['id'] != ''
    assert response.json()['data']['name'] != ''


def test_delete_user_id():
    params = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@gmail.com",
        "planet": "Earth",
    }

    response: Response = requests.post(url_users, params)
    id = response.json()["id"]

    response: Response = requests.delete(url_users, params=id)

    assert response.status_code == 204
    assert response.text == ""


def test_update_user_firstname():
    params = {
        "first_name": "Bill",
        "last_name": "MacDuck",
        "email": "billdac@gmail.com",
        "job": "Golden Store",
    }

    response: Response = requests.post(url_users, params)
    id = response.json()["id"]

    params["first_name"] = "George"

    response: Response = requests.put(f"{url_users}/{id}", json=params)

    assert response.status_code == 200
    assert response.json()["first_name"] == params["first_name"]


def test_register_successful():
    json_data = {"email": "eve.holt@reqres.in", "password": "pistole1233"}
    response: Response = requests.post(url_reg, json=json_data)

    assert response.status_code == 200


def test_register_unsuccessful():
    json_data = {"email": "sydney@fife"}
    response: Response = requests.post(url_reg, json=json_data)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_login_successful():
    json_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    response: Response = requests.post(url_login, json=json_data)

    assert response.status_code == 200
    assert response.json()["token"] != ""


def test_login_unsuccessful():
    json_data = {"email": "peter@klaven"}
    response: Response = requests.post(url_login, json=json_data)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_delayed_response():
    params = {"delay": 3}
    response: Response = requests.get(url_users, params)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] != ""


""" Тесты из урока (лекции) """


def test():
    response: Response = requests.get(
        "https://reqres.in/api/users", params={"page": 2, "per_page": 4}
    )
    print(response.status_code)
    print(response.text)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["page"] == 2
    assert response.json()["per_page"] == 4
    assert len(response.json()["data"]) == 4


def test2():
    response: Response = requests.get("https://reqres.in/api/users", params={"page": 2})
    print(response.status_code)
    print(response.text)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["page"] == 2
    assert len(response.json()["data"]) == 6


def test_requested_page_number():
    page = 2

    response: Response = requests.get(
        "https://reqres.in/api/users", params={"page": page}
    )

    assert response.status_code == 200
    assert response.json()["page"] == page


def test_users_list_default_lenght():
    default_users_count = 6
    response: Response = requests.get("https://reqres.in/api/users")

    assert len(response.json()["data"]) == default_users_count


def test_single_user_not_found():
    response = requests.get("https://reqres.in/api/users/23")

    assert response.status_code == 404
    assert response.text == "{}"


def test_create_user():
    name = "morpheus"
    job = "job"
    response = requests.post(
        "https://reqres.in/api/users", json={"name": "morpheus", "job": "leader"}
    )

    pprint(response.text)
    text = {
        "name": "morpheus",
        "job": "leader",
        "id": "849",
        "createdAt": "2023-06-08T17:41:10.783Z",
    }

    assert response.status_code == 201
    assert response.json()["name"] == name


def test_delete_user_returns_204():
    response = requests.delete("https://reqres.in/api/users/2")

    assert response.status_code == 204
    assert response.text == ""
