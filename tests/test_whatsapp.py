from urllib import request

import pytest
from httpx import QueryParams

from src.whatsapp.whatsapp import verify_webhook


def test_endpoint_verification():
    ## URL
    webhook_get = "hub.mode=subscribe&hub.challenge=78185524&hub.verify_token=verif"
    query_params = QueryParams(
    )
    response = verify_webhook()
    pass

def test_test_receive_message():
    pass