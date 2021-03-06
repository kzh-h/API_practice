#!/bin/bash

sudo docker login --username $HEROKU_USERNAME --password $HEROKU_API_KEY registry.heroku.com
sudo docker tag $HEROKU_APP_NAME:latest registry.heroku.com/$HEROKU_APP_NAME/web
if [ $TRAVIS_BRANCH == "main" ] && [ $TRAVIS_PULL_REQUEST == "false" ]; then sudo docker push registry.heroku.com/$HEROKU_APP_NAME/web; fi

chmod +x heroku-container-release.sh
sudo chown $USER:docker ~/.docker
sudo chown $USER:docker ~/.docker/config.json
sudo chmod g+rw ~/.docker/config.json

./heroku-container-release.sh