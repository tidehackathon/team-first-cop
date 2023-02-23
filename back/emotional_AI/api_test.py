from numpy.lib.utils import source
import requests
import pprint
from requests.utils import quote

url = 'http://localhost:8228'
#####################################
# Повідомлення
messages = [
    'Я люблю дарить улыбку, ', 
    "на Чаки очень похож ))))",
    "красава братан",
    "Ты не бабник, нет - не льсти себе. ты - курицалюб",
    "пьяная рожа"
]
# Мова повідомлень, не обов'язковий параметр
source_lang='ru'
# Вибір моделі, що повинна використовуватись для задачі, 
# за замовчуванням 'DET_EMOTION_MODEL'
env_names = ['DET_EMOTION_MODEL', 'DET_TOPICS_MODEL', 'DET_APPROP_MODEL']
env = env_names[0]
#####################################
r = requests.post(url+"/set_ip", json={'env': env, "ip":'http://192.168.101.29:8010'})
# Варіант 1: GET запити для кожного окремого повідомлення
for text in messages:
    r = requests.get(f'{url}/label?message={quote(text)}&source_lang={source_lang}&env={env}')
    translated_text = r.json()
    print(text,"\n=>RESPONSE:")
    pprint.pprint(translated_text, sort_dicts=False)
    print("\n")


# Варіант 2: POST запит який відсилає масив повідомлень
print("\nPost request that sends all sentences at once")
r = requests.post(url+"/label", json={'message': messages, "source_lang":source_lang, 'env': env})
response_data = r.json()
pprint.pprint(response_data, sort_dicts=False)

# r = requests.post(f'{url}/set_model_env', json={'new_env':'DET_TOPICS_MODEL'})
# response_data = r.json()
# pprint.pprint(response_data, sort_dicts=False)