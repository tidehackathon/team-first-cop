from numpy.lib.arraysetops import isin
from requests import models
import requests
from ModelsOperator.ModelsHandler import ModelsHandler
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
import http3
import torch
import numpy as np



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
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Used device in runtime: {torch_device}")
logger.info(f"{os.getenv('MODELNAME')}")
model = ModelsHandler(
    env_name=os.getenv("MODELNAME"), 
    device=torch_device,
    logger=logger
)

class ChEnvRequest(BaseModel):
    new_env:str


@app.get("/label")
async def label_data(message: List[str]=Query([]),
                     source_lang: Optional[str]='') -> Dict[str, str]:
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
    logger.info(message)
    output = {
        'text': message,
        "source_lang": source_lang
    }

    try:
        outs = model.predict(message, logger)
    except Exception as e:
        logger.info(e)
        raise HTTPException(403, detail="Error: "+str(e))

    output['label'] = outs[0]
    output['logits'] = outs[1]
    output['calculation_time'] = outs[2]
    return output


@app.get('/modelname')
async def modelname():
    logger.info("MODELNAME call")
    return {"response": f"{model._model_name}"}


@app.post("/label")
async def label_data_post(request: Request):
    """
    Post method for labeling json object of messages list 
    :return:
    """
    logger.info("LABEL_POST call")
    data = await request.json()
    return await label_data(**data)

@app.post("/set_model_env")
async def set_env_post(request: ChEnvRequest):
    """
    Post method for labeling json object of messages list
    :param new_env: name of desired environment
    """
    logger.info("SET_MODEL_ENV call")
    if request.new_env not in model._env_names:
        raise HTTPException(status_code=404, detail=f"Environment {request.new_env} not found in {model._env_names}")
        # return JSONResponse(content=jsonable_encoder({"response":"Environment {request.new_env} not found in {model._env_names}"}))
    else:
        asyncio.create_task(
            model.set_env(request.new_env)
        )
        return JSONResponse(content=jsonable_encoder({"response":"model's setting up"}))