import os

import pytest
from httpx import Request
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient
import json


def hello(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Hello World!")


def stations_response(request: Request) -> JSONResponse:
    data = json.loads(open(os.path.join(os.getcwd(), "bicing_stations_response.json")).read())
    # data = json.loads(open(os.path.join(os.getcwd(), "another_test.json")).read())
    return JSONResponse(data)


@pytest.fixture(scope="session")
def bicing_test_API():
    app = Starlette(routes=[
        Route("/", hello),
        Route("/es/get-stations", stations_response)
    ])
    yield TestClient(app)


def uploaded_media(request) -> JSONResponse:
    return JSONResponse({"id": "1363181297589232"})


@pytest.fixture(scope="session")
def whatsapp_test_API():
    app = Starlette(routes=[
        Route("/", hello),
        Route("/102033176202052/media", uploaded_media, methods=["POST"])
    ])
    yield TestClient(app)
