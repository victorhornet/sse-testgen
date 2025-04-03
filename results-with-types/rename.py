import os

if __name__ == "__main__":
    for path in os.listdir("."):
        if os.path.isdir(path):
            for subpath in os.listdir(path):
                if os.path.isdir(os.path.join(path, subpath)):
                    if subpath.startswith("iteration_"):
                        iteration_number = int(subpath.split("_")[1])
                        full_path = os.path.join(path, subpath)
                        if iteration_number < 7:
                            new_iteration_number = iteration_number + 7
                            new_path = os.path.join(
                                path, f"iteration_{new_iteration_number}"
                            )
                            if full_path != new_path:
                                print(f"Renaming {full_path} to {new_path}")
                                # input("Press Enter to continue")
                                os.rename(full_path, new_path)
