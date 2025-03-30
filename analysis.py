import os
import json
import csv


def collect_energy_data(results_dir="results", output_dir="jasp"):
    """
    Collects energy data from JSON files in each iteration subfolder and writes:
      - A CSV for each algorithm in the 'jasp' folder.
      - An aggregated CSV file with all iterations from all algorithm folders.
    """
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List to collect all data across algorithms for the aggregated CSV
    aggregated_all_data = []

    # Loop over each algorithm directory in 'results'
    for algorithm in os.listdir(results_dir):
        algorithm_path = os.path.join(results_dir, algorithm)

        # Skip if it's not a directory
        if not os.path.isdir(algorithm_path):
            continue

        # Prepare a list to hold data for the current algorithm (without the "algorithm" key)
        aggregated_data = []

        # Look through each iteration folder within the algorithm directory
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
                iteration_index = iteration_folder.split("_")[-1]

                # Create row data for the per-algorithm CSV (excluding "algorithm")
                row_algo = {
                    "iteration": iteration_index,
                    "energy_consumption_joules": data.get("energy_consumption_joules", ""),
                    "execution_time_seconds": data.get("execution_time_seconds", ""),
                    "watts": data.get("watts", "")
                }
                aggregated_data.append(row_algo)

                # Create row data for the aggregated CSV (including "algorithm")
                row_agg = {
                    "algorithm": algorithm,
                    "iteration": iteration_index,
                    "energy_consumption_joules": data.get("energy_consumption_joules", ""),
                    "execution_time_seconds": data.get("execution_time_seconds", ""),
                    "watts": data.get("watts", "")
                }
                aggregated_all_data.append(row_agg)

        # If we found any data for this algorithm, write it out to a CSV file
        if aggregated_data:
            # Sort by iteration index numerically
            aggregated_data.sort(key=lambda x: int(x["iteration"]))
            csv_filename = os.path.join(output_dir, f"{algorithm}.csv")
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["iteration", "energy_consumption_joules", "execution_time_seconds", "watts"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(aggregated_data)
            print(f"Created: {csv_filename}")
        else:
            print(f"No JSON data found for {algorithm}, skipping CSV creation.")

    # Write the aggregated CSV with data from all algorithms if any data exists
    if aggregated_all_data:
        # Sort first by algorithm name, then by iteration number
        aggregated_all_data.sort(key=lambda x: (x["algorithm"], int(x["iteration"])))
        csv_all_filename = os.path.join(output_dir, "all_algorithms.csv")
        with open(csv_all_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["algorithm", "iteration", "energy_consumption_joules", "execution_time_seconds", "watts"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(aggregated_all_data)
        print(f"Created aggregated file: {csv_all_filename}")
    else:
        print("No JSON data found across any algorithm.")


if __name__ == "__main__":
    collect_energy_data()
