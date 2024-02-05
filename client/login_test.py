import json
import time

import requests

BASE_URL = "http://localhost:8000/api/"
BASE_HEADER = {"Content-Type": "application/json"}


def _prepare_header(token):
    header = BASE_HEADER.copy()
    header["Authorization"] = f"Bearer {token}"
    return header


def login() -> [str, str]:
    login_data = {"username": "client", "password": "CARINg123%"}
    response = requests.post(BASE_URL + "token/", data=json.dumps(login_data), headers=BASE_HEADER)
    return response


def refresh_login(refresh_token: str):
    refresh_data = {"refresh": refresh_token}
    response = requests.post(BASE_URL + "token/refresh/", data=json.dumps(refresh_data), headers=BASE_HEADER)
    return response


def get_patients(access_token: str) -> [dict, str]:
    response = requests.get(BASE_URL + "patients/", headers=_prepare_header(access_token))
    return response


def update_patient(access_token: str, url: str, update_data: dict) -> [dict, str]:
    response = requests.put(url, data=json.dumps(update_data), headers=_prepare_header(access_token))
    return response


def delete_patient(access_token: str, url: str) -> [dict, str]:
    response = requests.delete(url, headers=_prepare_header(access_token))
    return response


def add_patient(access_token: str) -> [dict, str]:
    data = {"first_name": "Hans", "last_name": "Meier", "birth_date": "1975-10-31"}
    response = requests.post(BASE_URL + "patients/", data=json.dumps(data), headers=_prepare_header(access_token))
    return response


def logout(refresh_token: str):
    data = {"refresh": refresh_token}
    response = requests.post(BASE_URL + "token/blacklist/", data=json.dumps(data), headers=BASE_HEADER)
    return response


def main():
    response = login()
    access_token = response.json()["access"]
    refresh_token = response.json()["refresh"]
    print(f"login: {response.json()}")

    response = add_patient(access_token)
    print(f"add: {response.json()}")

    time.sleep(18)

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = refresh_login(refresh_token)
    access_token = response.json()["access"]
    print(f"refresh: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    url = response.json()['results'][0]['url']
    update_data = {"first_name": "Harald",
                   "last_name": response.json()['results'][0]['last_name'],
                   "birth_date": response.json()['results'][0]['birth_date'],
                   }
    response = update_patient(access_token, url, update_data)
    print(f"update: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = delete_patient(access_token, url)
    print(f"delete: {response.status_code}")

    response = logout(refresh_token)
    print(f"logout: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = refresh_login(refresh_token)
    print(f"refresh: {response.json()}")


if __name__ == "__main__":
    main()
