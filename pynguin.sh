#!/bin/bash

docker run \
    -it \
    --rm \
    -v $(pwd)/examples:/input:ro \
    -v $(pwd)/tests:/output \
    -v $(pwd)/pynguin-report:/app/pynguin-report \
    pynguin-cli \
    --maximum-search-time 10 \
    --project-path "/input" \
    --output-path "/output" \
    --verbose \
    "$@"
