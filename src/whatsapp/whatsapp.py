import pprint
import httpx
import tempfile
from dotenv import load_dotenv
from starlette.datastructures import QueryParams

from src import bicing
import os

from src.schemas import Coordinates
from src.whatsapp.schemas import LocationMessage, WhatsappMessage, WrongMessageType

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
        self.META_TOKEN = META_TOKEN
        self.ACTIVE_NUMBER_ID = ACTIVE_NUMBER_ID
    def _make_httpx_client(self):
        headers = {
            "Authorization": f"Bearer {META_TOKEN}",
            "Content-Type": "application/json"
        }

        return httpx.Client(
            base_url="https://graph.facebook.com/v17.0/",
            headers=headers
        )

    def process_location_message(self, message: WhatsappMessage) -> Coordinates:
        if message.entry[0].changes[0].value.messages[0].type != "location":
            raise WrongMessageType("Messaage is not a location")

        latitude = message.entry[0].changes[0].value.messages[0].location.latitude
        longitude = message.entry[0].changes[0].value.messages[0].location.longitude
        return Coordinates(latitude=latitude, longitude=longitude)

    def send_message(self):
        return None

    def send_image(self):
        return None

# def POST_meta_request(url, json, add_headers={}):
#     headers = {}
#     headers['Authorization'] = f"Bearer {META_TOKEN}"
#     headers['Content-Type'] = 'application/json'
#
#     for key, value in add_headers.items():
#         headers[key] = value
#
#     response = requests.post(url, headers=headers, json=json)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Error: {response.status_code} {response.text}")
    
def upload_image(image_path):
    #curl -X POST 'https://graph.facebook.com/v17.0/<MEDIA_ID>/media' \
    #    -H 'Authorization: Bearer <ACCESS_TOKEN>' \
    #    -F 'file=@"2jC60Vdjn/cross-trainers-summer-sale.jpg"' \
    #    -F 'type="image/jpeg"' \
    #    -F 'messaging_product="whatsapp"'

    headers = {}
    headers['Authorization'] = f"Bearer {META_TOKEN}"

    files = {'file': open('/Users/ggarcia/git_sources/bicing_utils/mapita.png', 'rb')}
    #data = {'type': (None, "image/png"), 'messaging_product': (None, "whatsapp")}
    data = {'type': "image/png", 'messaging_product': "whatsapp"}
    print(files)

    response = requests.post(
            f"https://graph.facebook.com/v17.0/{ACTIVE_NUMBER_ID}/media", 
            headers=headers,
            data=data,
            files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return response.text

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


def verify_webhook(query_params: QueryParams):
    """ Endpoint to verify the webhook
    """
    print("----- VERIFY WEBHOOK -----")
    print(query_params)
    print("----- VERIFY WEBHOOK -----")
    
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
        return "Error", 500

def _extract_coordinates(message):
    """ Extract coordinates from message
    """
    if "location" not in message:
        raise Exception("No location in message")

    latitude = message['location']['latitude']
    longitude = message['location']['longitude']
    return latitude, longitude

def process_webhook(
        data: dict,
    ):
    print("----- PROCESS WEBHOOK -----")
    print(data)
    print("---------------------------")
    ##### TODO: El 2xx tine que ir aca y spawnear esto en async or something
    for entry in data['entry']:
        for change in entry['changes']:
            print(f"Field --> {change['field']}")
            
            value = change['value']
            metadata = value['metadata']

            if 'messages' in value:
                
                ################ Process User
                contacts = value['contacts']

                for message in value['messages']:
                    if message['type'] != 'location':
                        continue

                    print(f"Message is -------> {message}")
                    latitude, longitude = _extract_coordinates(message)
                    print(f"Latitude is {latitude} and longitude is {longitude}")
                    
                    map_string = bicing.find_bikes(latitude, longitude)

                    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
                        ## Upload media file
                        tmp.write(map_string)
                        image_id = upload_image(tmp.name)




            elif 'statuses' in value:
                for status in value['statuses']:
                    print(f"Status is -------> {status}")

            else:
                print("No messages or statuses")

            ## Detect the change type the triggered the webhook to process
            #detect_change_type(change)

    ## Process user
    print("----------END WEBHOOK----------")
    ## Return OK to webhook

    return True

