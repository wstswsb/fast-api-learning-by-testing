import os
import uuid

import httpx
import pytest

port = os.getenv("PORT")


@pytest.mark.parametrize(
    "url",
    (
        f"http://127.0.0.1:{port}/documents/",
        f"http://127.0.0.1:{port}/documents/{uuid.uuid4()}",
        f"http://127.0.0.1:{port}/presentations/",
        f"http://127.0.0.1:{port}/presentations/{uuid.uuid4()}",
        f"http://127.0.0.1:{port}/overridden_vehicles/vehicles/",
        f"http://127.0.0.1:{port}/overridden_vehicles/vehicles/{uuid.uuid4()}",
    ),
)
def test_routing(url: str):
    response = httpx.get(url, timeout=1)

    assert response.status_code == 200
