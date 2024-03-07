import asyncio
import uuid
from pprint import pformat
from typing import Annotated

import pydantic
from fastapi import (
    FastAPI,
    Request,
    Depends,
    Response,
    Cookie,
    BackgroundTasks,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from websockets.exceptions import ConnectionClosed

from routers import documents_router, presentations_router, vehicles_router

app = FastAPI()

security = HTTPBasic()

app.include_router(documents_router)
app.include_router(presentations_router)

# what if I override prefix? prefixes will concatenate
app.include_router(vehicles_router, prefix="/overridden_vehicles")


@app.get("/request")
def get_request(request: Request) -> str:
    formatted = pformat(dir(request))
    print(formatted)
    return formatted


@app.get("/response-pythonic")
def get_response_pythonic() -> dict[str, str]:
    return {"pythonic": "response"}


class ModelIn(BaseModel):
    field_1: str
    field_2: str
    field_3: str


class ModelOut(BaseModel):
    field_1: str
    field_2: str

    @pydantic.computed_field
    @property
    def comma_fields(self) -> str:
        return f"{self.field_1},{self.field_2}"


@app.post("/response-model/", response_model=ModelOut)
def get_response_with_response_model(model_in: ModelIn):
    return model_in


@app.get("/base-http-security/")
def get_base_http_security(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> dict[str, str]:
    # header (authorization: Basic base64encode(username:password) )
    return {"username": credentials.username, "password": credentials.password}


@app.get("/response-with-server-cookies/")
def get_response_with_server_cookies(response: Response):
    response.set_cookie(key="test-cookie-key", value="test-cookie-value")


@app.get("/response-with-client-cookies/")
def get_response_with_client_cookies(
    test_cookie: Annotated[str | None, Cookie()] = None
) -> dict[str, str]:
    return {"test_cookie": test_cookie}


@app.get("/background-error")
def start_background_error(background_tasks: BackgroundTasks):
    async def task(message: str):
        await asyncio.sleep(5)
        print("Task will finish now")
        raise ValueError(message)

    # After first task fail fastapi cancel all from this scope
    background_tasks.add_task(task, "oops")
    background_tasks.add_task(task, "oops")
    background_tasks.add_task(task, "oops")


@app.get("/background")
def start_background(background_tasks: BackgroundTasks):
    async def task(message: str):
        await asyncio.sleep(2)
        print(f"Correct task finish, message id {message}")

    background_tasks.add_task(task, "task1")
    background_tasks.add_task(task, "task2")


@app.middleware("http")
async def set_request_uuid_cookie(request: Request, call_next):
    request_uuid = str(uuid.uuid4())
    request.cookies["uuid"] = request_uuid
    response = await call_next(request)
    response.set_cookie("uuid", request_uuid)
    return response


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    print("trying to accept")
    await websocket.accept()
    try:
        for i in range(3):
            await websocket.send_text(f"response-{i}")
        await websocket.close()

    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
