import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class WhatsappObjectTypeEnum(str, Enum):
    whatsapp_business_account = 'whatsapp_business_account'


class Profile(BaseModel):
    name: str


class Contact(BaseModel):
    profile: Profile
    wa_id: int


class MessageText(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(..., alias='from')
    id: str
    text: MessageText
    timestamp: datetime.datetime
    type: str

class Location(BaseModel):
    latitude: float
    longitude: float

class LocationMessage(BaseModel):
    from_: str = Field(..., alias='from')
    id: str
    location: Location
    timestamp: datetime.datetime
    type: str

class MessagingProductEnum(str, Enum):
    whatsapp = "whatsapp"


class MessageMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str



class ChangeValue(BaseModel):
    contacts: List[Contact]
    messages: List[Message] | List[LocationMessage]
    messaging_product: MessagingProductEnum
    metadata: MessageMetadata


class Changes(BaseModel):
    field: str
    value: ChangeValue


class Entry(BaseModel):
    id: int
    changes: List[Changes]


class WebhookObject(BaseModel):
    object: WhatsappObjectTypeEnum
    entry: List[Entry]


class LocationMessage(BaseModel):
    ## b'{"object":"whatsapp_business_account","entry":[{"id":"104246805978102","changes":[{"value":{"messaging_product":"whatsapp","metadata":{"display_phone_number":"34623508545","phone_number_id":"102033176202052"},"contacts":[{"profile":{"name":"Gonza"},"wa_id":"447472138610"}],"messages":[{"from":"447472138610","id":"wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgUM0FEMjcwQzBBRDVENDc5NDg4NzQA","timestamp":"1693442282","location":{"latitude":41.381469726562,"longitude":2.1878051757812},"type":"location"}]},"field":"messages"}]}]}'
    pass
## b'{"object":"whatsapp_business_account","entry":[{"id":"104246805978102","changes":[{"value":{"messaging_product":"whatsapp","metadata":{"display_phone_number":"34623508545","phone_number_id":"102033176202052"},"contacts":[{"profile":{"name":"Gonza"},"wa_id":"447472138610"}],"messages":[{"from":"447472138610","id":"wamid.HBgMNDQ3NDcyMTM4NjEwFQIAEhgUM0FBM0UwRjlEMzA5OTQ3OTVGODEA","timestamp":"1693439799","location":{"latitude":41.381469726562,"longitude":2.1878051757812},"type":"location"}]},"field":"messages"}]}]}'


