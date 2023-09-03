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
    ImageUploadError, WhatsappMediaResource, WhatsappMessageResponse, WhatsappMessageOUT, WhatsappMediaTypeEnum, \
    WhatsappTextObject, MimeTypeEnum, WhatsappContact

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
            base_url=f"https://graph.facebook.com/v17.0/{ACTIVE_NUMBER_ID}",
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

    def message_sender(self, message: WhatsappMessageIN) -> WhatsappContact:
        return message.entry[0].changes[0].value.contacts[0]

    def send_message(self, message_out: WhatsappMessageOUT):
        headers = {"Content-Type": "application/json"}
        response = self._http_client.post(
            f"/messages",
            json=message_out.model_dump())

        if response.status_code == 200:
            return WhatsappMessageResponse(**response.json())
        else:
            log.error(response.text)
            raise Exception("Message exception")

    def send_image(self, to: str, image_path: str):
        ## Upload the image and get the code
        media_resource = WhatsappMediaResource(
            path=image_path,
            mime_type=MimeTypeEnum.image_png,
            whatsapp_type=WhatsappMediaTypeEnum.image_png,
        )
        image = self.upload_image(media_resource)

        ## Send the image
        text_message = WhatsappMessageOUT(
            to=f"+{to}",
            type=WhatsappMediaTypeEnum.image,
            image=WhatsappResponseId(id=image.id),
        )
        message = self.send_message(text_message)
        print(message)
        return None

    def upload_image(self, media_resource: WhatsappMediaResource):
        file_name = os.path.basename(media_resource.path)
        files = {"file": (file_name, open(media_resource.path, "rb"), media_resource.mime_type)}
        data = {"type": "image/png", "messaging_product": "whatsapp"}
        response = self._http_client.post(
            f"/media",
            data=data,
            files=files)
        if response.status_code == 200:
            return WhatsappResponseId(**response.json())
        else:
            log.error(response.text)
            print(response.text)
            raise ImageUploadError("Error uploading the image")