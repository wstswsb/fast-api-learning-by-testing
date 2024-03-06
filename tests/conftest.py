import os

import pytest


@pytest.fixture
def url_base() -> str:
    return f"http://127.0.0.1:{os.getenv('PORT')}"


@pytest.fixture()
def ws_url_base() -> str:
    return f"ws://127.0.0.1:{os.getenv('PORT')}"
