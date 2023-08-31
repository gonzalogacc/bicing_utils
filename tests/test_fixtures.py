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
    #data = json.loads(open(os.path.join(os.getcwd(), "another_test.json")).read())
    return JSONResponse(data)


@pytest.fixture(scope="session")
def bicing_test_API():
    app = Starlette(routes=[
        Route("/", hello),
        Route("/es/get-stations", stations_response)
    ])
    yield TestClient(app)