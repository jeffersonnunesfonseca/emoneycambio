#!/bin/bash

if [ -z ${DOCKER_USERNAME} ]; then
    echo "Missing DOCKER_USERNAME variable!"
    exit 1
fi

error() {
    if [ $? != 0 ]; then
        echo "Error!"
        exit 122
    fi
}

build() {
    echo "=> Building ${1}"
    docker build -t ${1} .
    echo "=> Built ${1}"
}

tag() {
    echo "=> Tagging ${1}"
    docker tag ${1} $(echo $DOCKER_USERNAME):${1}
    echo "=> Tagged ${1}"
}

push() {
    echo "=> Pushing ${1}"
    docker push $(echo $DOCKER_USERNAME):${1}
    echo "=> Pushed ${1}"
}


build ${1}
error
tag ${1}
error
push ${1}
error
ssh -i ~/.ssh/Jeff.pem ubuntu@$IP_SERVER "sudo service nginx restart && sudo docker pull jefonseca/emoneycambio && sudo docker rm -f emoneycambio && sudo docker run -d -p 5656:5656 --network host --env-file /home/ubuntu/.secrets/.env --name emoneycambio jefonseca/emoneycambio:latest"

exit 0