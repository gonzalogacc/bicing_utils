from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.whatsapp import endpoints

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)

@app.get("/")
def ping():
    return {"Hello": "pong!"}

#@app.post("/bicing")
#def bicing(
#        latitude: float,
#        longitude: float,
#        ):
#    return dict(latitude=latitude, longitude=longitude)
