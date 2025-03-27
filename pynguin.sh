#!/bin/bash

docker run \
    -it \
    --rm \
    -v $(pwd)/examples:/input:ro \
    -v $(pwd)/tests:/output \
    -v $(pwd)/pynguin-report:/app/pynguin-report \
    pynguin-cli \
    --maximum-search-time 1 \
    --maximum-iterations 1 \
    --maximum-statement-executions 1 \
    --maximum-test-executions 1 \
    --project-path "/input" \
    --output-path "/output" \
    --verbose \
    "$@"
