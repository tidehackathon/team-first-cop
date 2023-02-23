@echo off
set emo=DET_EMOTION_MODEL
set top=DET_TOPICS_MODEL
set apr=DET_APPROP_MODEL
set PWD=%~dp0
set ntw=ml-bridge


docker run --net ml-bridge -m 6gb --name %emo% -p 8010:8010 -v %PWD%models_bucket:/models_bucket/ -e MODELNAME=%emo% cyberp/workers:cpu-v1
@REM docker run --net %ntw% --name %top% -m 4gb -p 8011:8011 -v %PWD%models_bucket:/models_bucket/ -e MODELNAME=%top% cyberp/workers:cpu-v1
@REM docker run --net %ntw% --name %apr% -m 4gb -p 8012:8011 -v %PWD%models_bucket:/models_bucket/ -e MODELNAME=%apr% cyberp/workers:cpu-v1