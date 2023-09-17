from fastapi import FastAPI, Depends, APIRouter, HTTPException, Request, BackgroundTasks
import json

# from google.cloud import pubsub_v1
import base64
import os

from google.cloud import pubsub_v1

from src.bicing import BicingClient
from src.google_maps import get_static_map, Marker, MarkerTypeEnum
from src.schemas import ResourceEnum
from src.whatsapp.whatsapp import WhatsappClient

from dotenv import load_dotenv

from src.whatsapp.schemas import WhatsappMessageIN

load_dotenv()

PUBSUB_PROJECT_ID = os.getenv("PUBSUB_PROJECT_ID", "bicing-replacement")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "bicing-prod")

router = APIRouter(
    tags=["whatsapp"],
)


@router.get("/ping")
async def ping():
    return "pong"


@router.get('/meta_hook')
def GET_meta_hook(
        request: Request
):
    """
    Have to return OK to this call to subscribe webhook in meta
    hub.mode=subscribe&hub.challenge=1918437135&hub.verify_token=verificacion
    """
    wac = WhatsappClient()
    try:
        print(request)
        return wac.verify_webhook(request.query_params)
    except:
        raise HTTPException("verification error")


@router.post('/meta_hook')
async def POST_meta_hook(
        request: Request,
):
    """
    """
    print("----- META WEBHOOK -----")
    data = await request.body()
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)

    future = publisher.publish(topic_path, data)
    print(future.result())
    print(f"Published messages to {topic_path}.")
    return "OK", 200


@router.post('/pubsub_hook')
async def meta_hook(
        request: Request,
):
    """
    hub.mode=subscribe&hub.challenge=1918437135&hub.verify_token=verificacion
    El webhook siempre va a devolver 200, el processing se hace en un background taask
    """
    print("----------------pubsub webhook--------------------")
    data = json.loads(await request.body())
    decoded_data = base64.b64decode(data['message']['data'])
    json_data = json.loads(decoded_data)
    print("--------------------------------------------------")

    ## TODO: process the extra messages whatsapp send after a message
    try:
        print("----- MESSAGE WEBHOOK -----")
        wc = WhatsappClient()
        was_message = WhatsappMessageIN(**json_data)
        coordinates = wc.process_location_message(was_message)
        user = wc.message_sender(was_message)
        bc = BicingClient()
        stations = bc.find_closest(ResourceEnum.electrical_bikes, coordinates)

        bikes = [Marker(latitude=station.latitude, longitude=station.longitude, label=station.electrical_bikes, marker_type=MarkerTypeEnum.station) for station in stations]
        bikes.append(Marker(longitude=coordinates.longitude, latitude=coordinates.latitude, marker_type=MarkerTypeEnum.own))
        outfile = get_static_map(markers=bikes)
        wc.send_image(user.wa_id, outfile)

        print("----- MESSAGE WEBHOOK -----")

    except:

        return "OK", 200
