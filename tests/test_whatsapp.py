import json
from urllib import request

import pytest
from httpx import QueryParams

from src.whatsapp.schemas import WhatsappMessageIN, WrongMessageType, WhatsappMediaResource, MimeTypeEnum, \
    WhatsappMediaTypeEnum, WhatsappTextObject, WhatsappMessageOUT
from src.whatsapp.whatsapp import WhatsappClient
from tests.test_fixtures import whatsapp_test_API

def test_webhook_object_SimpleMessage():
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgWM0VCMDcwOTVGNDA5ODBGMjREMkY1QQA=', 'timestamp': '1693437013', 'text': {'body': 'hola'}, 'type': 'text'}]}, 'field': 'messages'}]}]}
    wo = WhatsappMessageIN(**raw)
    assert wo.entry[0].id == 104246805978102

def test_webhook_object_LocationMessage():
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgUM0FEMjcwQzBBRDVENDc5NDg4NzQA', 'timestamp': '1693442282', 'location': {'latitude': 41.381469726562, 'longitude': 2.1878051757812}, 'type': 'location'}]}, 'field': 'messages'}]}]}
    wo = WhatsappMessageIN(**raw)
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
    coordinates = wac.process_location_message(WhatsappMessageIN(**raw))

    assert coordinates.longitude == 2.1878051757812
    assert coordinates.latitude == 41.381469726562

def test_extract_latlong_from_text_message():
    # get a Location message and extract the coordinates with the function
    raw = {'object': 'whatsapp_business_account', 'entry': [{'id': '104246805978102', 'changes': [{'value': {'messaging_product': 'whatsapp', 'metadata': {'display_phone_number': '34623508545', 'phone_number_id': '102033176202052'}, 'contacts': [{'profile': {'name': 'Gonza'}, 'wa_id': '447472138610'}], 'messages': [{'from': '447472138610', 'id': 'wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgWM0VCMDcwOTVGNDA5ODBGMjREMkY1QQA=', 'timestamp': '1693437013', 'text': {'body': 'hola'}, 'type': 'text'}]}, 'field': 'messages'}]}]}

    with pytest.raises(WrongMessageType) as error:
        wac = WhatsappClient()
        coordinates = wac.process_location_message(WhatsappMessageIN(**raw))

def test_upload_image_function_ok(whatsapp_test_API):
    media_resource = WhatsappMediaResource(
        name="mapita.png",
        path="/Users/ggarcia/git_sources/bicing_utils/mapita.png",
        mime_type=MimeTypeEnum.image_png,
        whatsapp_type=WhatsappMediaTypeEnum.image_png,
    )

    wc = WhatsappClient()
    wc._http_client = whatsapp_test_API
    response = wc.upload_image(media_resource)
    print(response)
    assert response.id == 1363181297589232

def test_send_whatsapp_message_OK(whatsapp_test_API):
    text_message = WhatsappMessageOUT(
        to = "+447472138610",
        type = WhatsappMediaTypeEnum.text,
        text = WhatsappTextObject(body="test message")
    )
    wc = WhatsappClient()
    wc._http_client = whatsapp_test_API
    response = wc.send_message(text_message)
    assert len(response.messages) > 0

# {
#     "messaging_product": "whatsapp",
#     "recipient_type": "individual",
#     "to": "PHONE_NUMBER",
#     "type": "text",
#     "text": { // the text object
#     "preview_url": false,
#     "body": "MESSAGE_CONTENT"
# }
# }'
