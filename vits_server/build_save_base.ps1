#!/bin/bash
docker build  -t amadeus/vits_server:$tag .
docker tag amadeus/vits_server:$tag
docker save -o ./build/vits_server-$tag.tgz amadeus/vits_server:$tag
 