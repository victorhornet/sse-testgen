# SSE Project 1

## Building docker container

1. Export dependencies `uv pip freeze > requirements.txt`
2. TODO build script

## Installation

1. Clone the repo
2. Build the docker container: `docker build -t pynguin-cli .`
3. Run with `./pynguin.sh`

## Development setup w/uv

1. Clone the repo
2. Generate a venv: `uv venv --seed`
3. Sync dependencies: `uv sync`
4. Freeze dependencies when done: `uv pip freeze > requirements.txt`
