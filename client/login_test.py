import json
import time

import requests

BASE_URL = "http://localhost:8000/"
BASE_HEADER = {"Content-Type": "application/json"}


def _prepare_header(token):
    header = BASE_HEADER.copy()
    header["Authorization"] = f"Bearer {token}"
    return header


def login() -> [str, str]:
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(BASE_URL + "auth/token/", data=json.dumps(login_data), headers=BASE_HEADER)
    return response


def refresh_login(refresh_token: str):
    refresh_data = {"refresh": refresh_token}
    response = requests.post(BASE_URL + "auth/token/refresh/", data=json.dumps(refresh_data), headers=BASE_HEADER)
    return response


def logout(refresh_token: str):
    data = {"refresh": refresh_token}
    response = requests.post(BASE_URL + "auth/token/blacklist/", data=json.dumps(data), headers=BASE_HEADER)
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


def print_response(method, response):
    status = response.status_code
    json = "none"
    try:
        json = response.json()
    except Exception as e:
        pass
    print(f"{method}: {json} ({status})")


def main():
    wait_time = 0.1

    response = login()
    print_response("login", response)
    access_token = response.json()["access"]
    refresh_token = response.json()["refresh"]
    time.sleep(wait_time)

    response = add_patient(access_token)
    print_response("add", response)
    time.sleep(wait_time)

    response = get_patients(access_token)
    print_response("patients", response)
    time.sleep(wait_time)

    response = refresh_login(refresh_token)
    access_token = response.json()["access"]
    print_response("refresh", response)
    time.sleep(wait_time)

    response = get_patients(access_token)
    print_response("patients", response)
    time.sleep(wait_time)

    url = response.json()['results'][0]['url']
    update_data = {"first_name": "Harald",
                   "last_name": response.json()['results'][0]['last_name'],
                   "birth_date": response.json()['results'][0]['birth_date'],
                   }
    response = update_patient(access_token, url, update_data)
    print_response("update", response)
    time.sleep(wait_time)

    response = get_patients(access_token)
    print_response("patients", response)
    time.sleep(wait_time)

    response = delete_patient(access_token, url)
    print_response("delete", response)
    time.sleep(wait_time)

    response = logout(refresh_token)
    print_response("logout", response)
    time.sleep(wait_time)

    response = get_patients(access_token)
    print_response("patients", response)
    time.sleep(wait_time)

    response = refresh_login(refresh_token)
    print_response("refresh", response)
    time.sleep(wait_time)


if __name__ == "__main__":
    main()
