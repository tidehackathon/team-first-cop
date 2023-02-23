import os, sys
from typing import List,Tuple
import logging
import time
import json
from numpy.lib.npyio import loads
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class ModelsHandler:
    env_to_loc_name = staticmethod(lambda env: f"/models_bucket/{os.getenv(env).split('/')[-1]}")
    _env_names = ['DET_EMOTION_MODEL', 'DET_TOPICS_MODEL', 'DET_APPROP_MODEL']
    
    def __init__(self, env_name:str="DET_EMOTION_MODEL", device:str='cpu', logger=None):
        """
        Initialize start model, tokenizer and label for desired model_state
        """
        torch.set_grad_enabled(False)
        logger.info(ModelsHandler.env_to_loc_name(env_name))
        logger.info(self._get_labels(env_name))
        self._model_name = ModelsHandler.env_to_loc_name(env_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        logger.info("TOKENIZER")
        self.model = AutoModelForSequenceClassification.from_pretrained(self._model_name).to(device)
        logger.info("MODEL")
        self.labels = self._get_labels(env_name)
        self.device = device
        
    

    def predict(self, messages: List[str], logger) -> Tuple[List[str], List[float], float]:
        """
        Feed messages to model and return triplet of predicted labels, logits and spent time 
        """
        st = time.time()
        with torch.no_grad():
            inputs = self.tokenizer(messages, max_length=512, padding=True, truncation=True, return_tensors='pt').to(self.device)
            out = self.model(**inputs).logits
            logits = torch.nn.functional.softmax(out, dim=1)
            predicted = torch.argmax(logits, dim=1).numpy()
        logger.info([inputs, out, logits, predicted])
        labels = []
        for pred in predicted:
            if isinstance(self.labels, dict):
                pred=str(pred)
            labels.append(self.labels[pred])
        return labels, logits.numpy().tolist(), time.time()-st


    async def set_env(self, env_name:str="DET_EMOTION_MODEL"):
        """
        Set new model, tokenizer and labels for desired model_state
        """
        self._model_name = ModelsHandler.env_to_loc_name(env_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self._model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        self.labels = self._get_labels(env_name)


    async def set_device(self, device:str="cpu"):
        self.device = device
        self.model.to(device)


    def _get_labels(self, env_name):
        if env_name=="DET_EMOTION_MODEL":
            return np.array(['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
        elif env_name=="DET_TOPICS_MODEL":
            with open('/id2topic_sens.json', 'r') as f: 
                return json.load(f)
        elif env_name=="DET_APPROP_MODEL":
            return np.array(['no', 'yes'])
        