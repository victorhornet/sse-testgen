# Evaluating Power Consumption of Python Test Generation using Pynguin

## Prerequisites

-   Docker
-   Python 3.10.12

## Setup Instructions

1. Install [EnergiBridge](https://github.com/tdurieux/EnergiBridge)
2. Build the pynguin docker container: `docker build -t pynguin-cli .`
3. Use `./pynguin.sh` or everywhere instead of the normal `pynguin` command
4. In case of write permission errors, you may need to give permissions to the Docker `appuser`: `sudo chown -R 10001:10001 ./tests/`
5. Set up the Python environment using [venv](#python-environment-setup-wvenv) or [uv](#python-environment-setup-wuv)

### Python Environment Setup w/venv

note: make sure to use **Python 3.10.12**

6. Create a python virtual environment:

```bash
python -m venv .venv
```

7. Activate the virtual environment:

```bash
source .venv/bin/activate
```

8. Install requirements:

```bash
pip install -r requirements.txt
```

9. Done, [run the experiment](#running-the-experiment)

### Python Environment Setup w/uv

6. Generate a venv:

```bash
uv venv --seed
```

7. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## Running the experiment

1. Rename `pyenergibridge_config.json.example` to `pyenergibridge_config.json`:

```bash
mv pyenergibridge_config.json{.example,}
```

2. Update the binary path in `pyenergibridge_config.json` to the installation path of the EnergiBridge binary
3. Create experiment configs in `pynguing_configs.json`, passing a config name and the pynguin CLI parameters. For example:

```jsonc
[
    //...
    {
        "name": "dynamosa-42",
        "params": {
            "seed": 42,
            "algorithm": "DYNAMOSA"
        }
    }
    //...
]
```

5. Run the `main.py` script:

    - with `uv`:

    ```bash
    uv run python main.py --allowed-projects codetiming_local,docstring_parser_local --iterations 10
    ```

    - with `uv` from the zen script on macos:

    ```bash
    ./run_zen.sh
    ```

    - from `.venv`:

    ```bash
    .venv/bin/python main.py --allowed-projects codetiming_local,docstring_parser_local --iterations 10
    ```

For more information on available command-line options:

```bash
python main.py --help
```

## Analysis

To collect the results from the json files and run the analysis, use:

```bash
python analysis.py
```
