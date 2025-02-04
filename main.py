import subprocess
import os
import sys
import logging
import time
from pathlib import Path

# ==========================
# CONFIGURATION & LOGGING
# ==========================

# Define the base directory dynamically
BASE_DIR = Path(__file__).resolve().parent

# Define paths to the scripts
SCRIPTS = [
    BASE_DIR / "src/extractor/repositories_extractor.py",
    BASE_DIR / "src/classifier/classifier.py"
]

# Configure logging
LOG_FILE = BASE_DIR / "logs/main.log"
os.makedirs(LOG_FILE.parent, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ==========================
# CORE FUNCTIONS
# ==========================

def run_script(script_path):
    """
    Executes a Python script using subprocess and logs execution time.

    Args:
        script_path (Path): The path to the Python script to execute.

    Returns:
        float: Execution time in seconds.
    """
    start_time = time.time()
    try:
        logging.info(f"Starting execution: {script_path}")
        print(f"\n▶ Running: {script_path.name}...")

        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )

        execution_time = time.time() - start_time
        logging.info(f"Completed: {script_path} in {execution_time:.2f} seconds.\nOutput:\n{result.stdout}")
        print(f"✅ {script_path.name} completed successfully in {execution_time:.2f} seconds.")

        return execution_time

    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing {script_path}.\nExit code: {e.returncode}\nOutput: {e.stdout}\nError: {e.stderr}")
        print(f"❌ Error executing {script_path}. Check logs for details.")
        sys.exit(1)

    except Exception as e:
        logging.error(f"Unexpected error executing {script_path}: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def main():
    """
    Main function to sequentially execute the scripts and measure execution times.
    """
    print("\n🚀 Starting execution pipeline...\n")
    logging.info("Main execution started.")

    total_start_time = time.time()
    execution_times = {}

    for script in SCRIPTS:
        if script.exists():
            execution_times[script.name] = run_script(script)
        else:
            logging.error(f"Script not found: {script}")
            print(f"❌ Script not found: {script}")
            sys.exit(1)

    total_duration = time.time() - total_start_time

    print("\n📊 Execution Summary:")
    logging.info("Execution Summary:")
    for script, duration in execution_times.items():
        print(f"   - {script}: {duration:.2f} seconds")
        logging.info(f"   - {script}: {duration:.2f} seconds")

    print(f"\n✅ All scripts executed successfully in {total_duration:.2f} seconds!")
    logging.info(f"All scripts executed successfully in {total_duration:.2f} seconds.")

# ==========================
# EXECUTION
# ==========================

if __name__ == "__main__":
    main()
