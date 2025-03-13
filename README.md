# SSE Project 2

## Linux

### Installing Pynguin with Docker

1. Build the docker container: `docker build -t pynguin-cli .`
2. Run with `./pynguin.sh`

## Development setup w/uv

1. Generate a venv: `uv venv --seed`
2. Sync dependencies: `uv sync`
3. Freeze dependencies when done: `uv pip freeze > requirements.txt`

## Running the experiment

1. Install [EnergiBridge](https://github.com/tdurieux/EnergiBridge)
2. Rename `pyenergibridge_config.json.example` to `pyenergibridge_config.json`: `mv pyenergibridge_config.json{.example,}`
3. Update the binary path in `pyenergibridge_config.json`
4. Create experiment configs in `pynguing_configs.jsonc`. For example:

```jsonc
 {
        // Name of the experiment config
        "name": "dynamosa-42",
        // Parameters to be passed to the pynguin cli
        "params": {
            // e.g. --seed 42
            "seed": 42,
            // e.g. --algorithm DYNAMOSA
            "algorithm": "DYNAMOSA"
        }
    },
```

5. Run the `main.py` script:
    - with `uv`: `uv run python main.py`
    - from `.venv`: `.venv/bin/activate/python main.py`

## Windows

1. Build the docker container: `docker build -t pynguin-cli .`
2. Run the docker container and the script by running `python main_no_energy.py`.
