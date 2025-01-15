import subprocess
import os
import sys

def run_script(script_path):
    """
    Executes a Python script using subprocess.

    Args:
        script_path (str): The path to the Python script to execute.

    Returns:
        None
    """
    try:
        print(f"Executing script: {script_path}")
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Script {script_path} executed successfully.\nOutput:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}.\nExit code: {e.returncode}\nOutput: {e.stdout}\nError: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error executing {script_path}: {e}")
        sys.exit(1)

def main():
    """
    Main function to sequentially execute the scripts.
    """
    # Define paths to the scripts
    base_dir = os.path.abspath(os.path.dirname(__file__))
    scripts = [
        os.path.join(base_dir, "src/extractor/extractor_repos.py"),
        os.path.join(base_dir, "src/classifier/classifier.py")
    ]

    print("Starting the main script execution...\n")
    
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"Script not found: {script}")
            sys.exit(1)

    print("\nAll scripts executed successfully!")

if __name__ == "__main__":
    main()
