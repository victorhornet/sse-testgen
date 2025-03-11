import json
import os
import subprocess
import time

def main():
    # Load Pynguin configuration from JSON
    with open("pynguin_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:
        # Create a results directory per config
        results_dir = os.path.join(os.getcwd(), "results", config["name"])
        os.makedirs(results_dir, exist_ok=True)

        # Iterate over all Python examples
        for example in os.listdir("examples"):
            if not example.endswith(".py"):
                continue
            module_name = os.path.splitext(example)[0]
            run_pynguin(module_name, config["params"])

        # Pause briefly between runs to avoid bias
        time.sleep(5)

def run_pynguin(module_name: str, params: dict):
    # Get absolute paths for the volume mounts
    project_dir = os.getcwd()
    examples_path = os.path.join(project_dir, "examples")
    tests_path = os.path.join(project_dir, "tests")
    report_path = os.path.join(project_dir, "pynguin-report")

    # Construct the docker run command directly
    command = [
        "docker", "run",
        "-v", f"{examples_path}:/input:ro",
        "-v", f"{tests_path}:/output",
        "-v", f"{report_path}:/app/pynguin-report",
        "pynguin-cli",  # this is the name of the Docker image
        "--project-path", "/input",
        "--output-path", "/output",
        "--verbose",
        "--module-name", module_name,
    ]
    # Append any additional parameters from the configuration
    command += [f"--{key}={value}" for key, value in params.items()]

    print("Running command:", " ".join(command))
    subprocess.run(command, check=True)

if __name__ == "__main__":
    main()
