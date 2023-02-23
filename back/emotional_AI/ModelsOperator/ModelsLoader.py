import os, sys
from typing import List
import logging
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter("%(asctime)s [%(process)d] [%(levelname)s] %(message)s",datefmt="[%Y-%m-%d %H:%M:%S %z]")
# handler.setFormatter(formatter)
# logger.addHandler(handler)


def load_models(env_names: List[str]=None):
    if env_names is None:
        env_names = os.getenv("MODELNAME")
    if isinstance(env_names, str):
        env_names = [env_names]
    for env in env_names:
        # remote and local names of models
        # all local models stored in models_bucket dir
        rem_model_name = os.getenv(env, default="sismetanin/xlm_roberta_large-ru-sentiment-rusentiment")
        loc_model_name = f"/models_bucket/{rem_model_name.split('/')[-1]}"
        if os.path.exists(loc_model_name):
            print(f'Model {loc_model_name} found on disk ....')
            continue
        else:
            st = time.time()
            print("Downloading {} model and saving it at {}".format(rem_model_name, loc_model_name))
            tokenizer = AutoTokenizer.from_pretrained(rem_model_name)
            model = AutoModelForSequenceClassification.from_pretrained(rem_model_name)
            print("Model {} has been loaded in {:.2} sec".format(rem_model_name, time.time()-st))
            st = time.time()
            model.save_pretrained(loc_model_name)
            tokenizer.save_pretrained(loc_model_name)
            print("Model and tokenizer have been saved in {:.2} sec".format(time.time()-st))