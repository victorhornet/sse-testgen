#! /bin/bash

docker run \
    -it \
    --rm \
    -v $(pwd)/examples:/input:ro \
    -v $(pwd)/tests:/output \
    -v $(pwd)/pynguin-report:/app/pynguin-report \
    pynguin-cli \
    --project-path "/input" \
    --output-path "/output" \
    --verbose \
    "$@"
