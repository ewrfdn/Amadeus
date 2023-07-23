#!/bin/bash
$tag = $args[0]
if ([string]::IsNullOrEmpty($tag)) {
  Write-Host "please input the tag"
  exit 1
}


Write-Output "build docker image with tag: amadeus/vits_server:$tag"

if (!(Test-Path -path .\build -PathType Container)) {
  New-Item -ItemType Directory -Path .\build
}

docker build --no-cache -t amadeus/vits_server:$tag .
docker tag amadeus/vits_server:$tag
docker save -o ./build/vits_server-$tag.tgz amadeus/vits_server:$tag
 