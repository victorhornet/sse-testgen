import json
import os
import argparse
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
    parser = argparse.ArgumentParser(
        description="Run Pynguin test generation with various configurations"
    )
    parser.add_argument(
        "--allowed-projects",
        type=str,
        help="Comma-separated list of allowed projects",
    )

    args = parser.parse_args()

    allowed_projects: set[str] = (
        set(args.allowed_projects.split(",")) if args.allowed_projects else set()
    )
    excluded_projects = {
        "tests",
    }

    # energy_bridge_runner = EnergiBridgeRunner()

    with open("pynguin_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:
        results_dir = Path.cwd() / "results" / config["name"]
        if not results_dir.exists():
            results_dir.mkdir(parents=True)

        # energy_bridge_runner.start(results_file=results_dir / "results.csv")

        # Recursively traverse "examples" for all .py files
        for project_name in os.listdir("examples"):
            if project_name in excluded_projects:
                continue
            if len(allowed_projects) > 0 and project_name not in allowed_projects:
                continue
            project_path = Path("examples") / project_name
            for root, _, files in os.walk(project_path):
                if "tests" in Path(root).parts:
                    continue
                for file_name in files:
                    excluded_files = {
                        "__init__.py",
                        "setup.py",
                        "__main__.py",
                        "launcher.py",
                        "conf.py",
                    }
                    if file_name.endswith(".py") and file_name not in excluded_files:
                        full_path = Path(root) / file_name

                        # Convert the path under "examples" into a Python module name
                        # e.g., "examples/dataclasses_json/sty/renderfunc.py" -> "dataclasses_json.sty.renderfunc"
                        relative_path = full_path.relative_to(project_path)
                        module_name = str(relative_path.with_suffix("")).replace(
                            os.path.sep, "."
                        )
                        run_pynguin(
                            project_name=project_name,
                            module_name=module_name,
                            params=config["params"],
                            log_file_path=project_name
                            / Path(module_name.replace(".", "/"))
                            / f"{config['name']}.txt",
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
    project_name: str,
    module_name: str,
    params: dict[str, str] = {},
    log_file_path: Optional[Path] = None,
):
    """Runs Pynguin test generation for the given module name.

    Args:
        project_name: The name of the project to run Pynguin on, relative to the `/examples` directory. Example: `codetiming_local`
        module_name: The name of the module to run Pynguin on.
        params: The CLI parameters to pass to Pynguin. Example: {"seed": 42}.
        log_file_path: The path to the log file to pipe the output to. Example: "codetiming_local/codetiming/_timers/mio-42.txt". Default: <project_path>/<module_name>.txt
    """
    log_file_path = (
        Path.cwd() / "logs" / (log_file_path or f"{project_name}/{module_name}.txt")
    )
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Running Pynguin on {module_name} with params {params}")
    try:
        with open(log_file_path, "w") as log_file:
            subprocess.run(
                [
                    PYNGUIN_EXECUTABLE,
                    "--no-rich",
                    "--project-path",
                    Path("/input") / project_name,
                    "--module-name",
                    module_name,
                    *[f"--{k}={v}" for k, v in params.items()],
                ],
                check=True,
                text=True,
                stdout=log_file,
            )
    except subprocess.CalledProcessError as e:
        print(f"Skipping module {module_name} due to error: {e}")

    # print a newline for better readability
    print()


if __name__ == "__main__":
    main()
