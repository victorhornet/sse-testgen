#! /bin/bash

docker run \
    -v $(pwd)/examples:/input:ro \
    -v $(pwd)/results:/output \
    -v $(pwd)/pynguin-report:/app/pynguin-report \
    pynguin-cli \
    --seed 42 \
    --project-path "/input" \
    --output-path "/output" \
    "$@"
