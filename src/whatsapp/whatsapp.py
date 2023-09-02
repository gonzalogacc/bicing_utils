import pprint
import httpx
import tempfile

import requests
from dotenv import load_dotenv
from starlette.datastructures import QueryParams

import logging as log

import os

from src.schemas import Coordinates
from src.whatsapp.schemas import LocationMessage, WhatsappMessageIN, WrongMessageType, WhatsappResponseId, \
    ImageUploadError, WhatsappMediaResource, WhatsappMessageResponse, WhatsappMessageOUT

load_dotenv()

ACTIVE_NUMBER_ID = os.getenv("MEDIA_ID", None)
META_TOKEN = os.getenv("META_TOKEN", None)

if ACTIVE_NUMBER_ID is None:
    raise Exception("No active number ID set")

if META_TOKEN is None:
    raise Exception("No meta token set")


class WhatsappClient:

    def __init__(self):
        self._http_client = self._make_httpx_client()

    @staticmethod
    def _make_httpx_client():
        headers = {
            "Authorization": f"Bearer {META_TOKEN}",
        }

        return httpx.Client(
            base_url="https://graph.facebook.com/v17.0/",
            headers=headers
        )

    @staticmethod
    def verify_webhook(query_params: QueryParams):
        """ Endpoint to verify the webhook
        """
        print("----- VERIFYING WEBHOOK -----")
        if 'hub.mode' not in query_params or \
                'hub.challenge' not in query_params or \
                'hub.verify_token' not in query_params:
            print("Error: missing params")
            return "Error", 500

        mode = query_params['hub.mode']
        challenge = int(query_params['hub.challenge'])
        token = query_params['hub.verify_token']

        ## TODO:  verif secret from secret manager
        if mode == 'subscribe' and token == 'verif':
            print(f'Webhook verified!!! {challenge}')
            return challenge
        else:
            raise Exception()

    @staticmethod
    def process_location_message(message: WhatsappMessageIN) -> Coordinates:
        if message.entry[0].changes[0].value.messages[0].type != "location":
            raise WrongMessageType("Messaage is not a location")

        latitude = message.entry[0].changes[0].value.messages[0].location.latitude
        longitude = message.entry[0].changes[0].value.messages[0].location.longitude
        return Coordinates(latitude=latitude, longitude=longitude)

    def send_message(self, message_out: WhatsappMessageOUT):
        headers = {"Content-Type": "application/json"}
        response = self._http_client.post(
            f"/{ACTIVE_NUMBER_ID}/messages",
            json=message_out.model_dump())

        if response.status_code == 200:
            print("OK")
            print(response.text)
            return WhatsappMessageResponse(**response.json())
        else:
            print(response.text)
            raise Exception("Message exception")

        # curl - X POST \
        #         'https://graph.facebook.com/v17.0/FROM_PHONE_NUMBER_ID/messages' \
        #         - H
        # 'Authorization: Bearer ACCESS_TOKEN' \
        # - H
        # 'Content-Type: application/json' \
        # - d
        # '
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
        return None

    def send_image(self):
        return None

    def upload_image(self, media_resource: WhatsappMediaResource):
        files = {"file": (media_resource.name, open(media_resource.path, "rb"), media_resource.mime_type)}
        data = {"type": "image/png", "messaging_product": "whatsapp"}
        response = self._http_client.post(
           f"/{ACTIVE_NUMBER_ID}/media",
           data=data,
           files=files)
        if response.status_code == 200:
            return WhatsappResponseId(**response.json())
        else:
            log.error(response.text)
            print(response.text)
            raise ImageUploadError("Error uploading the image")


##def send_message(
##        message_text, 
##        recipient_number, 
##        size=None, 
##        message_type='text',
##        preview_url=False
##    ):
##    """ Send a message and save the message metadata to the database
##    """ 
##    ## 
##    url = f"https://graph.facebook.com/v16.0/{ACTIVE_NUMBER_ID}/messages"
##    headers = {'Content-Type': 'application/json; charset=utf-8'}
##    
##
##
##    data = {
##      "messaging_product": "whatsapp",
##      "recipient_type": "individual",
##      "to": recipient_number,
##      "type": "image",
##      "image": {
##          }
##      "text": { 
##        "preview_url": preview_url,
##        "body": message_chunk.encode('utf-8', 'replace').decode('utf-8')
##        }
##    }
##    message_response = POST_meta_request(url, add_headers=headers, json=data)
##    message = message_response['messages'][0]
##    print(f"Message sent --> {message}")
##
##        contact = wat.ContactIN(
##            wa_id=recipient_number,
##        )
##        user = uf.get_or_create_user(contact, ses)
##
##        ## Todos los mensajes de respuesta van a quedar con el mismo response to y ordenados por id (int)
##        message['wasmid'] = message['id']
##        message['timestamp'] = datetime.now().timestamp()
##        message['type'] = message_type
##        message['text'] = dict(body=message_text)
##        message['response_to'] = response_to
##        message['direction'] = 'outbound'
##        
##        ## Setup size
##        if size is not None: message['size'] = size
##        else: message['size'] = dict(size=len(message_text), units='chars')
##
##    return True


# def _extract_coordinates(message):
#     """ Extract coordinates from message
#     """
#     if "location" not in message:
#         raise Exception("No location in message")
#
#     latitude = message['location']['latitude']
#     longitude = message['location']['longitude']
#     return latitude, longitude


# def process_webhook(
#         data: dict,
# ):
#     print("----- PROCESS WEBHOOK -----")
#     print(data)
#     print("---------------------------")
#     for entry in data['entry']:
#         for change in entry['changes']:
#             print(f"Field --> {change['field']}")
#
#             value = change['value']
#             metadata = value['metadata']
#
#             if 'messages' in value:
#
#                 ################ Process User
#                 contacts = value['contacts']
#
#                 for message in value['messages']:
#                     if message['type'] != 'location':
#                         continue
#
#                     print(f"Message is -------> {message}")
#                     latitude, longitude = _extract_coordinates(message)
#                     print(f"Latitude is {latitude} and longitude is {longitude}")
#
#                     map_string = bicing.find_bikes(latitude, longitude)
#
#                     with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
#                         ## Upload media file
#                         tmp.write(map_string)
#                         image_id = upload_image(tmp.name)
#
#
#
#
#             elif 'statuses' in value:
#                 for status in value['statuses']:
#                     print(f"Status is -------> {status}")
#
#             else:
#                 print("No messages or statuses")
#
#             ## Detect the change type the triggered the webhook to process
#             # detect_change_type(change)
#
#     ## Process user
#     print("----------END WEBHOOK----------")
#     ## Return OK to webhook
#
#     return True
