from urllib import request

import pytest
from httpx import QueryParams

from src.whatsapp.schemas import WebhookObject
from src.whatsapp.whatsapp import verify_webhook


def test_webhook_object():
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgWM0VCMDcwOTVGNDA5ODBGMjREMkY1QQA=', 'timestamp': '1693437013', 'text': {'body': 'hola'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
    wo = WebhookObject(**raw)
    assert wo.entry[0].id == 104246805978102


def test_endpoint_verification():
    ## URL
    webhook_get = "hub.mode=subscribe&hub.challenge=78185524&hub.verify_token=verif"
    query_params = QueryParams(
    )
    response = verify_webhook()
    pass