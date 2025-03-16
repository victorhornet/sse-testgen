import json
import os
from pathlib import Path
import subprocess
import time
from typing import Optional
from pyEnergiBridge.api import EnergiBridgeRunner

if os.name == "java":
    raise RuntimeError("This script is only supported on POSIX and Windows systems.")

CWD = Path.cwd()
WINDOWS_PYNGUIN_EXECUTABLE = CWD / "pynguin.bat"
POSIX_PYNGUIN_EXECUTABLE = CWD / "pynguin.sh"

PYNGUIN_EXECUTABLE = os.getenv(
    "PYNGUIN_EXECUTABLE",
    POSIX_PYNGUIN_EXECUTABLE if os.name == "posix" else WINDOWS_PYNGUIN_EXECUTABLE,
)


def main():
    # energy_bridge_runner = EnergiBridgeRunner()

    with open("pynguin_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:
        results_dir = Path.cwd() / "results" / config["name"]
        if not results_dir.exists():
            results_dir.mkdir(parents=True)

        # energy_bridge_runner.start(results_file=results_dir / "results.csv")

        # Recursively traverse "examples" for all .py files
        for root, _, files in os.walk("examples"):
            if "tests" in Path(root).parts:
                continue  # works
            if "apimd" in Path(root).parts:
                continue
            if "basic" in Path(root).parts:
                continue
            if "codetiming_local" in Path(root).parts:
                continue
            for file_name in files:
                if file_name.endswith(".py") and file_name != "__init__.py" and file_name != "setup.py" and file_name != "__main__.py" and file_name != "launcher.py":
                    # Build the full path to the file
                    full_path = Path(root) / file_name

                    # Convert the path under "examples" into a Python module name
                    # e.g., "examples/dataclasses_json/sty/renderfunc.py" -> "dataclasses_json.sty.renderfunc"
                    relative_path = full_path.relative_to("examples")
                    # Strip off the ".py" suffix and replace path separators with dots
                    module_name = str(relative_path.with_suffix("")).replace(os.path.sep, ".")

                    run_pynguin(
                        module_name,
                        config["params"],
                        # For the log file, we create a path under logs/<module_name>/configName.txt
                        log_file_path=Path(module_name.replace(".", "/")) / f"{config['name']}.txt",
                    )

        # # For checking individual packages without running the whole project
        # sty_dir = os.path.join("examples", "isort")
        # for file_name in os.listdir(sty_dir):
        #     if file_name.endswith(".py") and file_name != "__init__.py":
        #         # Remove the .py extension
        #         base_name = os.path.splitext(file_name)[0]
        #         # Use a dotted module name: sty.<filename>
        #         module_name = f"isort.{base_name}"
        #         run_pynguin(
        #             module_name,
        #             config["params"],
        #             log_file_path=Path(module_name) / Path(f"{config['name']}.txt"),
        #         )

        # energy, duration = energy_bridge_runner.stop()
        # print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")
        # with open(results_dir / "energy.json", "w") as f:
        #     json.dump(
        #         {
        #             "energy_consumption_joules": energy,
        #             "execution_time_seconds": duration,
        #         },
        #         f,
        #         indent=4,
        #     )

        # TODO: idk if this is a good way to prevent the bias
        time.sleep(5)


def run_pynguin(
    module_name: str, params: dict[str, str] = {}, log_file_path: Optional[Path] = None
):
    """Runs Pynguin test generation for the given module name.

    Args:
        module_name: The name of the module to run Pynguin on.
        params: The CLI parameters to pass to Pynguin. Example: {"seed": 42}.
        log_file_path: The path to the log file to pipe the output to. Example: "triangle/mio-42.txt". Default: <module_name>.txt
    """
    log_file_path = Path.cwd() / "logs" / (log_file_path or f"{module_name}.txt")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Running Pynguin on {module_name} with params {params}")
    with open(log_file_path, "w") as log_file:
        subprocess.run(
            [
                PYNGUIN_EXECUTABLE,
                "--no-rich",
                "--module-name",
                module_name,
                *[f"--{k}={v}" for k, v in params.items()],
            ],
            check=True,
            text=True,
            stdout=log_file,
        )


if __name__ == "__main__":
    main()
