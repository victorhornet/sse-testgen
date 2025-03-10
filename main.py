import json
import os
import subprocess
import time
from pyEnergiBridge.api import EnergiBridgeRunner


PYNGUIN_EXECUTABLE = os.getenv(
    "PYNGUIN_EXECUTABLE", os.path.join(os.getcwd(), "pynguin.sh")
)


def main():
    energy_bridge_runner = EnergiBridgeRunner()

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


def run_pynguin(module_name: str, params: dict):
    subprocess.run(
        [
            PYNGUIN_EXECUTABLE,
            "--module-name",
            module_name,
            *[f"--{k}={v}" for k, v in params.items()],
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
