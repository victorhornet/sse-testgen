import os
import json
import csv


def collect_energy_data(results_dir="results", output_dir="jasp"):
    """
    Collects energy data from JSON files in each iteration subfolder and writes
    a CSV for each algorithm in a 'jasp' folder.
    """

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop over each algorithm directory in 'results'
    for algorithm in os.listdir(results_dir):
        algorithm_path = os.path.join(results_dir, algorithm)

        # Skip if it's not actually a directory
        if not os.path.isdir(algorithm_path):
            continue

        # Prepare a list to hold data from all iterations of this algorithm
        aggregated_data = []

        # Look through each iteration folder
        for iteration_folder in sorted(os.listdir(algorithm_path)):
            iteration_path = os.path.join(algorithm_path, iteration_folder)

            # We only care about folders that look like "Iteration_x"
            if not os.path.isdir(iteration_path) or not iteration_folder.lower().startswith("iteration_"):
                continue

            # Construct the path to the JSON file
            json_file = os.path.join(iteration_path, "energy.json")

            if os.path.isfile(json_file):
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Extract the iteration index (e.g., "Iteration_0" -> "0")
                # or just store the entire folder name
                iteration_index = iteration_folder.split("_")[-1]

                # Append a row of data.
                aggregated_data.append({
                    "iteration": iteration_index,
                    "energy_consumption_joules": data.get("energy_consumption_joules", ""),
                    "execution_time_seconds": data.get("execution_time_seconds", ""),
                    "watts": data.get("watts", "")
                })

        # If we found any data for this algorithm, write it out to CSV
        if aggregated_data:
            # Sort by iteration index numerically (optional)
            aggregated_data.sort(key=lambda x: int(x["iteration"]))

            # Create a filename for the CSV (e.g. "dynamosa-42.csv")
            csv_filename = os.path.join(output_dir, f"{algorithm}.csv")

            # Write the CSV
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["iteration", "energy_consumption_joules", "execution_time_seconds", "watts"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(aggregated_data)

            print(f"Created: {csv_filename}")
        else:
            print(f"No JSON data found for {algorithm}, skipping CSV creation.")


if __name__ == "__main__":
    collect_energy_data()
