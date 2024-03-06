import base64

import httpx
import pytest

import websockets
import os


def test_get_with_response_model(url_base: str):
    model_in = {
        "field_1": "string_1",
        "field_2": "string_2",
        "field_3": "string_3",
    }

    response = httpx.post(
        f"{url_base}/response-model/",
        json=model_in,
        timeout=0.5,
    )

    assert response.status_code == 200
    assert response.json() == {
        "field_1": "string_1",
        "field_2": "string_2",
        "comma_fields": "string_1,string_2",
    }


def test_basic_authentication__correct(url_base: str):
    username = "ivan"
    password = "ivan-password"

    payload = base64.b64encode(f"{username}:{password}".encode("utf8"))
    token = b"Basic " + payload
    response = httpx.get(
        f"{url_base}/base-http-security/",
        headers={"Authorization": token},
        timeout=0.5,
    )

    assert response.status_code == 200
    assert response.json() == {"username": username, "password": password}


def test_basic_authentication__missed_header(url_base: str):
    response = httpx.get(f"{url_base}/base-http-security/", timeout=0.5)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_response_with_server_cookies(url_base: str):
    response = httpx.get(f"{url_base}/response-with-server-cookies/", timeout=0.5)

    assert response.status_code == 200
    assert response.cookies.get("test-cookie-key") == "test-cookie-value"


def test_get_response_with_client_cookies(url_base: str):
    response = httpx.get(
        f"{url_base}/response-with-client-cookies/",
        cookies={"test_cookie": "test-value"},
        timeout=0.3,
    )

    assert response.status_code == 200
    assert response.json() == {"test_cookie": "test-value"}


@pytest.mark.asyncio
async def test_websocket(ws_url_base):
    async with websockets.connect(f"{ws_url_base}/ws", open_timeout=0.5) as ws:
        responses = [response async for response in ws]
    assert responses == ["response-0", "response-1", "response-2"]
