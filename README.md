# SSE Project 2

## Installing Pynguin with Docker

1. Build the docker container: `docker build -t pynguin-cli .`
2. Run with `./pynguin.sh`

## Development setup w/uv

1. Generate a venv: `uv venv --seed`
2. Sync dependencies: `uv sync`
3. Freeze dependencies when done: `uv pip freeze > requirements.txt`
