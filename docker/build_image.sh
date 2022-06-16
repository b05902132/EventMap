#!/usr/bin/env sh

PROJECT_ROOT="$(dirname "$0")"/../

cd "${PROJECT_ROOT}"

# This project use poetry to manage dependency.
# Ask poetry to export the dependency into requirements.txt format,
# and since pip does not support mixing pypi dependency and git dependency in a single requirements.txt,
# we seperate them into two files.
poetry export -f requirements.txt | awk -e '{if ($0 ~ /git\+https:/)  {print > "req_git.txt"} else {print > "req.txt"}}'
docker build -f docker/Dockerfile . --target dependencies -t event_map:deps
docker build -f docker/Dockerfile . -t event_map "$@"
