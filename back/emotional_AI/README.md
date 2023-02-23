# Docker

The developed application will be delivered using [docker] (https://www.docker.com/) REST -API Technologies: data that need to be marked in the form of a request to the ari, which returns the marking result depending on the task. Three containers for the following tasks are implemented in total:
- Recognition of emotional color - *module Det_emotion_model *
- recognition of the potential context of the message - *DET_TOPICS_Model module *
- Estimation of the degree of "specificity" message from 0 to 1 - *module DET_Approp_model *

## First launch

To start the applications, you must first make a Srip Bilder in the Docker Image Console for Master (accepts ARI inquiries) and workrs. Since all the models used, as well as libraries for the environment, the file will be loaded at the first start, the file can be about 10-15 minutes.

```
build_container.sh
```

This script uses the processor as a computing unit and RAM to store models, but these settings can be changed. Two models were disconnected as a demonstration example to reduce the load on the system.

## Use

After the script has been working out two docker Image, one for the main (Master) and the second for the handler. All requests are sent to the Master Container. By default, the standard access address - 127.0.0.1.1:8228 Therefore, to check the correctness of installation can be go Launch returns "Hello World" message. To use the pre -defined precursor, it is necessary to use the HTTP: // Lcalhost: 8228/Label

The server request format has the following JSON format:
```
{
    "message": ["msg1", "msg2", ...],
    "source_lang": None,
    "env": DET_EMOTION_MODEL
}
```

The MESSAGE parameter is a list of messages in text format that needs to be classified; Source_lang - the language of the source, by default NULL, since the practical feasibility will be acquired in the future; ENV is a variable that is responsible for the name of the message handler, is set in accordance with the three values above.

The result of such a post request, regardless of the problem and language, will be the result in the following format:

```
{
    "text": message,
    "source_lang": source_lang,
    "env": env,
    "label": ["POSITIVE", "NEGATIVE", ...],
    "logits": [[0.01, 0.9, 0.3]],
    "calculation_time": 0.4213123
}
```

Accordingly, the following new data are added here: labels - labels of emotions in the order of appropriate input; Logits - an array of arrays of numbers with a floating point that characterize the network confidence in response; Calculation_time - the time spent on the processing of incoming messages with a worcker.

Examples of requests to recognize emotional coloring are given below:

```
from numpy.lib.utils import source
import requests
import pprint
from requests.utils import quote

url = 'http://localhost:8228'
#####################################
# Messages
messages = [
    'Я люблю дарить улыбку, ', 
    "на Чаки очень похож ))))",
    "красава братан",
    "Ты не бабник, нет - не льсти себе. ты - курицалюб",
    "пьяная рожа"
]
# Message language is not required
source_lang='ru'
# Choosing a model that should be used for a task,
# default 'Det_emotion_model'
env_names = ['DET_EMOTION_MODEL', 'DET_TOPICS_MODEL', 'DET_APPROP_MODEL']
env = env_names[1]
#####################################
# r = requests.post(url+"/set_ip", json={'env': env, "ip":'http://172.19.0.2:8011'})
# Option 1: Get requests for each individual message
for text in messages:
    r = requests.get(f'{url}/label?message={quote(text)}&source_lang={source_lang}&env={env}')
    translated_text = r.json()
    print(text,"\n=>RESPONSE:")
    pprint.pprint(translated_text, sort_dicts=False)
    print("\n")


# Option 2: Post request that sends an array of messages
print("\nPost request that sends all sentences at once")
r = requests.post(url+"/label", json={'message': messages, "source_lang":source_lang, 'env': env})
response_data = r.json()
pprint.pprint(response_data, sort_dicts=False)

r = requests.post(f'{url}/set_model_env', json={'new_env':'DET_TOPICS_MODEL'})
response_data = r.json()
pprint.pprint(response_data, sort_dicts=False)
```

As a result of the execution was received, for the Get request one message:

```
Я люблю дарить улыбку,  
=>RESPONSE:
{'text': ['Я люблю дарить улыбку, '],
 'source_lang': 'ru',
 'label': ['POSITIVE'],
 'logits': [[0.005161006469279528, 0.015147444792091846, 0.9796915650367737]],
 'calculation_time': 0.4088881015777588}


на Чаки очень похож )))) 
=>RESPONSE:
{'text': ['на Чаки очень похож ))))'],
 'source_lang': 'ru',
 'label': ['NEUTRAL'],
 'logits': [[0.02079816348850727, 0.5608097910881042, 0.41839200258255005]],
 'calculation_time': 0.40806150436401367}


красава братан 
=>RESPONSE:
{'text': ['красава братан'],
 'source_lang': 'ru',
 'label': ['POSITIVE'],
 'logits': [[0.007080805022269487, 0.006249494384974241, 0.9866697788238525]],
 'calculation_time': 0.39797306060791016}


Ты не бабник, нет - не льсти себе. ты - курицалюб 
=>RESPONSE:
{'text': ['Ты не бабник, нет - не льсти себе. ты - курицалюб'],
 'source_lang': 'ru',
 'label': ['NEUTRAL'],
 'logits': [[0.05387836694717407, 0.77876216173172, 0.1673593968153]],
 'calculation_time': 0.5120372772216797}


пьяная рожа 
=>RESPONSE:
{'text': ['пьяная рожа'],
 'source_lang': 'ru',
 'label': ['NEGATIVE'],
 'logits': [[0.9927225708961487, 0.005313348490744829, 0.0019640736281871796]],
 'calculation_time': 0.3383290767669678}
```

To post request with an array of messages:

```
Post request that sends all sentences at once
{'text': ['Я люблю дарить улыбку, ',
          'на Чаки очень похож ))))',
          'красава братан',
          'Ты не бабник, нет - не льсти себе. ты - курицалюб',
          'пьяная рожа'],
 'source_lang': 'ru',
 'label': ['POSITIVE', 'NEUTRAL', 'POSITIVE', 'NEUTRAL', 'NEGATIVE'],
 'logits': [[0.005161001347005367, 0.015147430822253227, 0.9796915650367737],
            [0.020798159763216972, 0.5608097910881042, 0.4183920919895172],
            [0.007080798037350178, 0.006249497644603252, 0.9866697788238525],
            [0.05387839674949646, 0.7787622809410095, 0.16735929250717163],
            [0.9927225708961487, 0.005313343834131956, 0.0019640708342194557]],
 'calculation_time': 1.644493818283081}
```


All models are mounted in doc dynamically to prevent the size of the container. Also, all cached files are stored in the `/cache/` folder, so they can be easily copied from the docker if necessary in the event of performance and other tasks.
