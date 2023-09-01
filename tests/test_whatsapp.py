from urllib import request

import pytest
from httpx import QueryParams

from src.whatsapp.schemas import WhatsappMessage
from src.whatsapp.whatsapp import verify_webhook, WhatsappClient


def test_webhook_object_SimpleMessage():
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgWM0VCMDcwOTVGNDA5ODBGMjREMkY1QQA=', 'timestamp': '1693437013', 'text': {'body': 'hola'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
    wo = WhatsappMessage(**raw)
    assert wo.entry[0].id == 104246805978102

def test_webhook_object_LocationMessage():
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgUM0FEMjcwQzBBRDVENDc5NDg4NzQA', 'timestamp': '1693442282', 'location': {'latitude': 41.381469726562, 'longitude': 2.1878051757812}, 'type': 'location'}]}, 'field': 'messages'}]}]}
    wo = WhatsappMessage(**raw)
    assert wo.entry[0].changes[0].value.messages[0].location.latitude == 41.381469726562
    assert wo.entry[0].changes[0].value.messages[0].location.longitude == 2.1878051757812

def test_endpoint_verification():
    ## URL
    webhook_get = "hub.mode=subscribe&hub.challenge=78185524&hub.verify_token=verif"
    query_params = QueryParams(
    )
    response = verify_webhook()
    pass

def test_extract_latlong_from_message():
    # get a Location message and extract the coordinates with the function
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgUM0FEMjcwQzBBRDVENDc5NDg4NzQA', 'timestamp': '1693442282', 'location': {'latitude': 41.381469726562, 'longitude': 2.1878051757812}, 'type': 'location'}]}, 'field': 'messages'}]}]}
    wac = WhatsappClient()
    coordinates = wac.process_location_message(WhatsappMessage(**raw))

    assert coordinates.longitude == 2.1878051757812
    assert coordinates.latitude == 41.381469726562

