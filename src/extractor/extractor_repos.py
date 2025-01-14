import os
import json
import requests
from datetime import datetime
from config import BASE_OUTPUT_DIR, TARGET_FILES, HEADERS  # Import configurations

# Logging
def log_message(message):
    """Write process messages to a log file."""
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    log_file_path = os.path.join(BASE_OUTPUT_DIR, 'process_log.txt')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

# Match target files
def is_target_file(file_name):
    """Check if a file matches the target patterns."""
    lower_name = file_name.lower()
    return any(lower_name.startswith(pattern) for pattern in TARGET_FILES)

# Download Root Files
def download_root_files(owner, repo, language):
    """Download specific root files from a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        log_message(f"Failed to fetch root files for {owner}/{repo}. Status: {response.status_code}, Response: {response.text}")
        return

    files = response.json()
    if not isinstance(files, list):
        log_message(f"No files found in {owner}/{repo}.")
        return

    # Prepare language-specific directory
    language_dir = os.path.join(BASE_OUTPUT_DIR, language)
    os.makedirs(language_dir, exist_ok=True)

    # Create a single file per repository
    repo_file_path = os.path.join(language_dir, f"{owner}_{repo}.txt")
    with open(repo_file_path, "w", encoding="utf-8") as repo_file:
        for file in files:
            file_name = file["name"]
            if file["type"] == "file" and is_target_file(file_name):
                file_content_url = file["download_url"]
                if not file_content_url:
                    log_message(f"No download URL for file {file_name} in {owner}/{repo}.")
                    continue

                try:
                    # Download the file content
                    file_response = requests.get(file_content_url, headers=HEADERS)
                    if file_response.status_code == 200:
                        repo_file.write(f"\n--- Start file: {file_name} ---\n")
                        repo_file.write(file_response.text)
                        repo_file.write(f"\n--- End file: {file_name} ---\n")
                        log_message(f"Added {file_name} to {repo_file_path}.")
                    else:
                        log_message(f"Failed to download {file_name} from {owner}/{repo}. Status: {file_response.status_code}")
                except Exception as e:
                    log_message(f"Error downloading {file_name} from {owner}/{repo}: {e}")
            else:
                log_message(f"Skipping {file_name} in {owner}/{repo}. Not a target file.")

# Process Repositories
def process_repositories(config):
    """Process each repository in the provided configuration."""
    for repo in config["repos"]:
        owner = repo["owner"]
        repo_name = repo["name"]
        language = repo.get("language", "unknown").lower()
        log_message(f"Processing repository: {owner}/{repo_name} (Language: {language})")
        try:
            download_root_files(owner, repo_name, language)
        except Exception as e:
            log_message(f"Error processing {owner}/{repo_name}: {e}")

# Main Script
if __name__ == "__main__":
    # Load configuration from file
    config_file = "config.json"
    with open(config_file, "r") as file:
        config = json.load(file)

    # Log start time
    start_time = datetime.now()
    log_message(f"Process started at: {start_time}")

    # Process repositories
    process_repositories(config)

    # Log end time and duration
    end_time = datetime.now()
    log_message(f"Process finished at: {end_time}")
    log_message(f"Total duration: {end_time - start_time}")
