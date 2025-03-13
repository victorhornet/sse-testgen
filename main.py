import json
import os
import subprocess
import time
from typing import Optional
from pyEnergiBridge.api import EnergiBridgeRunner

if os.name == "java":
    raise RuntimeError("This script is only supported on POSIX and Windows systems.")

CWD = os.getcwd()
WINDOWS_PYNGUIN_EXECUTABLE = os.path.join(CWD, "pynguin.bat")
POSIX_PYNGUIN_EXECUTABLE = os.path.join(CWD, "pynguin.sh")

PYNGUIN_EXECUTABLE = os.getenv(
    "PYNGUIN_EXECUTABLE",
    POSIX_PYNGUIN_EXECUTABLE if os.name == "posix" else WINDOWS_PYNGUIN_EXECUTABLE,
)


def main():
    energy_bridge_runner = EnergiBridgeRunner()
    os.makedirs("logs", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    with open("pynguin_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:
        results_dir = os.path.join(os.getcwd(), "results", config["name"])
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        energy_bridge_runner.start(
            results_file=os.path.join(results_dir, "results.csv")
        )

        for example in os.listdir("examples"):
            if not example.endswith(".py"):
                continue
            module_name = os.path.splitext(example)[0]
            run_pynguin(module_name, config["params"])

        energy, duration = energy_bridge_runner.stop()
        print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")
        with open(os.path.join(results_dir, "energy.json"), "w") as f:
            json.dump(
                {
                    "energy_consumption_joules": energy,
                    "execution_time_seconds": duration,
                },
                f,
                indent=4,
            )

        # TODO: idk if this is a good way to prevent the bias
        time.sleep(5)


def run_pynguin(
    module_name: str, params: dict[str, str] = {}, log_file_name: Optional[str] = None
):
    """Runs Pynguin test generation for the given module name.

    Args:
        module_name: The name of the module to run Pynguin on.
        params: The CLI parameters to pass to Pynguin. Example: {"seed": 42}.
        log_file_name: The name of the log file to pipe the output to. Example: "triangle-mio-42". Default: <module_name>
    """
    if log_file_name:
        log_file_name = log_file_name.replace(".log", "")
    log_file_name = f"{log_file_name or module_name}.log"
    log_file_path = os.path.join(os.getcwd(), "logs", log_file_name)
    with open(log_file_path, "w") as log_file:
        subprocess.run(
            [
                PYNGUIN_EXECUTABLE,
                "--module-name",
                module_name,
                *[f"--{k}={v}" for k, v in params.items()],
            ],
            check=True,
            stdout=log_file,
            stderr=log_file,
        )


if __name__ == "__main__":
    main()
