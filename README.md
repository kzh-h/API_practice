# API_practice

## Reference
[機械学習モデルを動かすWeb APIを作ってみる(1)：APIの作成](https://nigimitama.hatenablog.jp/entry/2020/02/10/050000)  
[機械学習モデルを動かすWeb APIを作ってみる(2)：uWSGIの設定](https://nigimitama.hatenablog.jp/entry/2020/02/12/214018)  
[機械学習モデルを動かすWeb APIを作ってみる(3)：Herokuにデプロイ](https://nigimitama.hatenablog.jp/entry/2020/02/17/000000)  
[機械学習モデルを動かすWeb APIを作ってみる(4)：chaliceでLambdaにデプロイ](https://nigimitama.hatenablog.jp/entry/2020/02/25/000000)  
[機械学習モデルを動かすWeb APIを作ってみる(5)：Lambdaにデプロイ](https://nigimitama.hatenablog.jp/entry/2020/03/09/000000)  

## Work on container
```
cd ./
docker-compose up -d
```
```
docker exec -it <container> bash
```
or
```
docker-compose exec mlap bash
```

## Train model
- ```cd ./src/models/```
- Set hyperparameters with params.json  
- Train model.  
```python train.py --input-file params.json --version v<0000>```  

## Control server
- Run server with flask.   
```
cd ./app
python api.py &
```
- Stop server (flask).
```
ps ax 
kill <PID> (or kill -9 <PID>)
``` 
- If stop server (uwsgi), container is down. If develop interface with flask, commentout command in docker-compose.yml and build container.

## post on CLI
- on CLI  
  - success  
  ```curl -X POST -H "Content-Type: application/json" -d '{"address": "東京都千代田区", "area": 30, "building_year": 2013}' localhost/api/predict```
  - faile
  ```curl -X POST -H "Content-Type: application/json" -d '{"address": None, "area": 30, "building_year": 2013}' localhost/api/predict```
- from .json
```curl -X POST -H "Content-Type: application/json" -d @file.josn' localhost/api/predict```

## MEMO
### 2021-01-14
- In .travis.yml, since login-user do not have root-authorization when deploy, docker build command is executed with sudo.
- Deploy with docker container, Procfile is not required. Instead, in Dockerfile.prod CMD <startup server> is written.
### 2021-01-12
- ```pip install uwsgi``` does not work on Ubuntu 20.xx.  
  Downgrade to Ubuntu 18.xx, ```apt install gcc-4.8``` and set symboliclink.  
  Rerference: [Condaの仮想環境でuWSGIのインストールに失敗する](https://katsuwosashimi.com/archives/300/python-conda-install-uwsgi-failed/)
- If required, update GCC from 4.x to 7.x.