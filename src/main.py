<<<<<<< HEAD
from fastapi import FastAPI, Request, HTTPException
import uvicorn
=======
import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from schemas.fub_webhook_schemas import EventSchema
from logs.logging_config import logger
from logs.logging_utils import log_server_start, log_server_stop


load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")
>>>>>>> dev


app = FastAPI()


<<<<<<< HEAD
@app.get("/")
def index():
=======
@app.on_event("startup")
async def startup_event():
    log_server_start()


@app.on_event("shutdown")
async def startup_event():
    log_server_stop()


@app.get("/")
async def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
>>>>>>> dev
    return {"success": True, "message": "Hello World"}


@app.post("/sms")
<<<<<<< HEAD
def sms(request: Request):
=======
async def sms(request: EventSchema):

    logger.info(f"{sms.__name__} -- SMS ENDPOINT TRIGGERED")
    logger.info(f"{sms.__name__} -- RECEIVED PAYLOAD - {dict(request)}")

>>>>>>> dev
    return {"success": True, "message": "Hello World", "data": request}


if __name__ == "__main__":
<<<<<<< HEAD
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
=======
    uvicorn.run(app=app, port=int(SERVER_PORT), host="127.0.0.1")
>>>>>>> dev
