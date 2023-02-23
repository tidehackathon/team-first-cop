wget -nc -O $(pwd)/models_bucket/xlm_roberta_large-ru-sentiment-rusentiment/pytorch_model.bin https://huggingface.co/sismetanin/xlm_roberta_large-ru-sentiment-rusentiment/resolve/main/pytorch_model.bin

docker network create ml-bridge

docker build -t cyberp/master:cpu-stable -f app .
docker build -t cyberp/workers:cpu-v1 -f subworker .

docker run --detach --net ml-bridge -m 7gb --name DET_EMOTION_MODEL -p 8010:8010 -v $(pwd)/models_bucket:/models_bucket/ -e MODELNAME=DET_EMOTION_MODEL cyberp/workers:cpu-v1
docker run --detach --net ml-bridge --name master -m 500mb -p 8228:80 cyberp/master:cpu-stable


echo "All done!"