"""
GitHub Root Files Downloader
=============================

Description:
------------
This script automates the extraction of specific root-level files (e.g., README, 
CONTRIBUTING, CODE_OF_CONDUCT) from GitHub repositories. It retrieves these 
files based on predefined patterns, organizes them by programming language, 
and stores the results locally.

Features:
---------
- **Configurable Target Files**: Downloads files that match specified patterns (e.g., "readme", "code_of_conduct").
- **Organized Storage**: Groups files into directories based on the repository's primary programming language.
- **Robust Error Handling**: Logs process details and errors to a dedicated log file.
- **External Configuration**:
  - `config/extractor.yaml`: Defines API credentials, file patterns, output directories, and logging settings.
  - `config/repositories.json`: Specifies repositories to process, including owner, name, and language.
"""
import os
import json
import requests
import yaml
import logging
from datetime import datetime
from pathlib import Path
from requests.exceptions import RequestException

# ==========================
# CONFIGURATION & LOGGING
# ==========================

def load_config():
    """
    Loads configuration from the YAML file.

    Returns:
        dict: Parsed configuration dictionary.
    """
    config_path = Path("config/extractor.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


# Load configuration from YAML
config = load_config()

# Global variables from YAML
BASE_OUTPUT_DIR = Path(config["BASE_OUTPUT_DIR"])
TARGET_FILES = config["TARGET_FILES"]
LOG_FILE = Path(config["LOG_FILE"])
REPO_CONFIG_FILE = Path(config["REPOSITORIES_FILE"])

# Ensure necessary directories exist
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# GitHub Token from environment variable
GITHUB_TOKEN = os.getenv(config["github"]["token_env"])
if not GITHUB_TOKEN:
    raise EnvironmentError(f"Environment variable '{config['github']['token_env']}' is not set.")

# HTTP Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}


# ==========================
# CORE FUNCTIONS
# ==========================

def is_target_file(file_name):
    """
    Checks if a file matches the target patterns.

    Args:
        file_name (str): The name of the file.

    Returns:
        bool: True if the file matches any target pattern, False otherwise.
    """
    return any(file_name.lower().startswith(pattern) for pattern in TARGET_FILES)


def fetch_repo_files(owner, repo):
    """
    Fetches the root-level files from a GitHub repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.

    Returns:
        list | None: List of files if successful, None otherwise.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f"Error fetching repository contents: {owner}/{repo}. Details: {e}")
        return None


def download_root_files(owner, repo, language):
    """
    Downloads and saves specific root-level files from a GitHub repository.

    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        language (str): Primary programming language.

    Returns:
        None
    """
    files = fetch_repo_files(owner, repo)
    if not files or not isinstance(files, list):
        logging.warning(f"No files found in repository: {owner}/{repo}.")
        return

    language_dir = BASE_OUTPUT_DIR / language.lower()
    language_dir.mkdir(parents=True, exist_ok=True)

    repo_file_path = language_dir / f"{owner}_{repo}.txt"

    with open(repo_file_path, "w", encoding="utf-8") as repo_file:
        for file in files:
            file_name = file["name"]
            if file["type"] == "file" and is_target_file(file_name):
                file_content_url = file.get("download_url")
                if file_content_url:
                    try:
                        file_response = requests.get(file_content_url, headers=HEADERS, timeout=10)
                        file_response.raise_for_status()
                        repo_file.write(f"\n--- Start file: {file_name} ---\n")
                        repo_file.write(file_response.text)
                        repo_file.write(f"\n--- End file: {file_name} ---\n")
                        logging.info(f"Downloaded {file_name} from {owner}/{repo}.")
                    except RequestException as e:
                        logging.error(f"Failed to download {file_name} from {owner}/{repo}. Details: {e}")
                else:
                    logging.warning(f"File {file_name} in {owner}/{repo} has no download URL.")
            else:
                logging.info(f"Skipping non-matching file: {file_name} in {owner}/{repo}.")


def process_repositories():
    """
    Reads repository list from config and processes them.

    Returns:
        None
    """
    if not REPO_CONFIG_FILE.exists():
        logging.error(f"Repositories configuration file not found: {REPO_CONFIG_FILE}")
        return

    try:
        with open(REPO_CONFIG_FILE, "r", encoding="utf-8") as file:
            repo_data = json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON in '{REPO_CONFIG_FILE}': {e}")
        return

    for repo in repo_data.get("repos", []):
        owner = repo.get("owner")
        repo_name = repo.get("name")
        language = repo.get("language", "unknown")

        if not owner or not repo_name:
            logging.warning(f"Skipping malformed repository entry: {repo}")
            continue

        logging.info(f"Processing repository: {owner}/{repo_name} (Language: {language})")
        try:
            download_root_files(owner, repo_name, language)
        except Exception as e:
            logging.error(f"Unexpected error processing {owner}/{repo_name}: {e}")


if __name__ == "__main__":
    start_time = datetime.now()
    logging.info(f"Process started at: {start_time}")

    process_repositories()

    end_time = datetime.now()
    logging.info(f"Process finished at: {end_time}")
    logging.info(f"Total duration: {end_time - start_time}")
