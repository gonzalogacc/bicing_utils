from fastapi import FastAPI, Depends, APIRouter, HTTPException, Request, BackgroundTasks
import json

from google.cloud import pubsub_v1
import base64
import os

import src.whatsapp.whatsapp as waf

from dotenv import load_dotenv
load_dotenv()

PUBSUB_PROJECT_ID = os.getenv("PUBSUB_PROJECT_ID", "bicing-prod")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "meta-wewebhook")

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
    return waf.verify_webhook(request.query_params)

@router.post('/meta_hook')
async def POST_meta_hook(
        request: Request, 
    ):
    """
    """
    print("----- META WEBHOOK -----")
    data = await request.body()
    try:
        print(data)
    except:
        return "OK", 200

    #publisher = pubsub_v1.PublisherClient()
    #topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)
    #
    #future = publisher.publish(topic_path, data)
    #print(future.result())
    #print(f"Published messages to {topic_path}.")
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

    #try:
    waf.process_webhook(json_data)
    #except Exception as e:
    #    print(e)
    #    return "OK", 200
    #return "OK", 200