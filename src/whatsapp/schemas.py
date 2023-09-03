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


class WhatsappMessageIN(BaseModel):
    object: WhatsappObjectTypeEnum
    entry: List[Entry]


class WrongMessageType(Exception):
    pass


class MessageProductEnum(str, Enum):
    whatsapp = "whatsapp"


class TypeEnum(str, Enum):
    image = "image"
    text = "text"


class TextObject(BaseModel):
    preview_url: str
    body: str


class MimeTypeEnum(str, Enum):
    image_png = "image/png"


class WhatsappMediaTypeEnum(str, Enum):
    image_png = "image"
    contact = "contact"
    audio = "audio"
    document = "document"
    image = "image"
    location = "location"
    sticker = "sticker"
    text = "text"
    video = "video"


class WhatsappMediaResource(BaseModel):
    path: str
    mime_type: MimeTypeEnum
    whatsapp_type: WhatsappMediaTypeEnum


class WhatsappResponseId(BaseModel):
    id: str


class ImageUploadError(Exception):
    pass


class RecipientTypeEnum(str, Enum):
    individual = "individual"


class WhatsappDocumentProvider(BaseModel):
    name: str


class WhatsappMediaLink(BaseModel):
    link: str
    provider: Optional[WhatsappDocumentProvider]


class WhatsappTextObject(BaseModel):
    preview_url: Optional[bool] = None
    body: str


class WhatsappMessageOUT(BaseModel):
    """ Construct this object to send a message to whatsapp
    """
    messaging_product: Optional[str] = "whatsapp"  ## it's always whatsapp
    recipient_type: Optional[RecipientTypeEnum] = RecipientTypeEnum.individual
    type: WhatsappMediaTypeEnum
    to: str

    text: Optional[WhatsappTextObject] = None

    ## This fields need to be uploaded first and then the id added here
    audio: Optional[WhatsappResponseId] = None
    document: Optional[WhatsappResponseId | WhatsappMediaLink] = None
    video: Optional[WhatsappResponseId] = None
    image: Optional[WhatsappResponseId | WhatsappMediaLink] = None
    sticker: Optional[WhatsappResponseId | WhatsappMediaLink] = None


class WhatsappContact(BaseModel):
    input: str
    wa_id: str


class WhatsappMessageResponse(BaseModel):
    messaging_product: str
    contacts: List[WhatsappContact]
    messages: List[WhatsappResponseId]
