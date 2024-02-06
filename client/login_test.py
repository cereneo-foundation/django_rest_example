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

    response = refresh_login(refresh_token)
    access_token = response.json()["access"]
    print_response("refresh", response)
    time.sleep(wait_time)

    response = logout(refresh_token)
    print_response("logout", response)
    time.sleep(wait_time)

    response = refresh_login(refresh_token)
    print_response("refresh", response)
    time.sleep(wait_time)


if __name__ == "__main__":
    main()
