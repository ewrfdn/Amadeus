#!/bin/bash

tag=$1
if [ -z $tag ]; then
  echo "please input the tag"
  exit 1
fi

echo "build docker image with tag: amadeus/vits_server:$tag"

mkdir build

docker build -t amadeus/vits_server:$tag .
docker tag amadeus/vits_server:$tag
docker save -o ./build/sd_control_center-$tag.tgz amadeus/vits_server:$tag
