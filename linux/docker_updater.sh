#!/bin/bash

function getDockerID {
    tmp_file=/tmp/container.tmp
    sudo docker container ls > $tmp_file
    tail -qn +2 $tmp_file
    container_id=$(egrep -oe '^\S{12}' $tmp_file)
    rm $tmp_file
    return $container_id
}

function getLatestImage {
    echo -e '[INFO] Pulling latest image...'
    sudo docker pull zadam/trilium:latest
}

echo "Searching for docker container"

echo $(getDockerID())

var=$(curl --location --request GET 'https://jsonplaceholder.typicode.com/users' --header 'Content-Type: application/json' --data-raw '{"id": "2"}')
echo $var