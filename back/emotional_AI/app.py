from requests import models
import requests
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import asyncio
from typing import Dict, Optional, Union, List
import uvicorn
import os
import sys
import logging
import time



logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(process)d] [%(levelname)s] %(message)s",datefmt="[%Y-%m-%d %H:%M:%S %z]")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def check_predictor():
#     predictors_ports = {
#         'DET_EMOTION_MODEL':'8010', 
#         'DET_TOPICS_MODEL':'8011',
#         'DET_APPROP_MODEL':'8012'
#     }
#     url = 'http://localhost'
#     r = requests.get(f'{url}/label?message={quote(text)}&source_lang={source_lang}')
#     translated_text = r.json()
predictors = {
    'DET_EMOTION_MODEL':'http://127.0.0.1:8010',
    'DET_TOPICS_MODEL':'http://127.0.0.1:8011',
    'DET_APPROP_MODEL':'http://127.0.0.1:8012'
}


# class LabelRequest(BaseModel):
#     message: str
#     source_lang: Optional[str] = None

# class ChEnvRequest(BaseModel):
#     new_env: str

class ChEnvRequest(BaseModel):
    url: str


@app.get("/label")
async def label_data(message: List[str]=Query([]),
                     source_lang: Optional[str]='',
                     env: Optional[str]='DET_EMOTION_MODEL') -> Dict[str, str]:
    """
        Method for detecting emotions of users messages list

        :param message: list of users messages
        :param source_lang: string value denotes messages language
        :param env: models name which should be used
        :type message: List[str]
        :type source_lang: Optional[str]
        
        :return: dictionary of values messages, source_lang, label
                 logits(denotes model confidence in output), and
                 calculation_time spent on result calculation
        :rtype: Dict[str, str]

    """
    # if env not in predictors.keys():
    #     raise HTTPException(status_code=404, detail=f"Environment \"{env}\" not found in {list(predictors.keys())}")
    # model = predictors[env]
    logger.info(message)
    # r = requests.post(f"{predictors[env]}/label", json={'message': message, "source_lang":source_lang})
    # response_data = r.json()
    return dict(requests.post(f"{predictors[env]}/label", json={'message': message, "source_lang":source_lang}).json())


@app.get('/')
async def home():
    logger.info("HOME call")
    return {"response": "Hello World"}


@app.post("/label")
async def label_data_post(request: Request):
    """
    Post method for labeling json object of messages list 
    :return:
    """
    logger.info("LABEL_POST call")
    data = await request.json()
    return await label_data(**data)

@app.post("/set_ip")
async def set_ip(request: Request):
    """
    Post method for labeling json object of messages list 
    :return:
    """
    logger.info("setip call")
    data = await request.json()
    predictors[data['env']] = data['ip']
    logger.info(predictors)

@app.get("/get_model")
async def get_model(request: ChEnvRequest):
    """
    Post method for labeling json object of messages list 
    :return:
    """
    logger.info("getmodel")
    r = requests.get(f"{request.url}/modelname").json()
    logger.info(r)
    return r