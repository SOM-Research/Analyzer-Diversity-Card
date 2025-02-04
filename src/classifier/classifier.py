"""
GitHub Root Files Classifier
============================

Description:
------------
This script processes root-level files extracted from GitHub repositories using OpenAI's GPT model. 
It analyzes specific files (e.g., README, CONTRIBUTING, CODE_OF_CONDUCT) and classifies their content 
based on predefined prompts.

Features:
---------
- **Automatic Language Detection**: Dynamically scans folders in `ROOT_FOLDER` to detect available programming languages.
- **AI-Powered File Analysis**: Uses OpenAI's API to process and classify root-level documentation files.
- **Structured JSON Output**: Stores classification results in organized directories based on programming language.
- **Configurable Settings**: 
  - `config/classifier.yaml`: Defines paths, API credentials, and logging settings.
  - `prompts.py`: Stores prompt templates for analysis.
- **Error Handling and Logging**: Logs process details and errors in a dedicated log file.
"""
import os
import json
import re
import yaml
import logging
from openai import OpenAI
from pathlib import Path
from datetime import datetime
from prompts import (
    SYSTEM_PROMPT,
    DEVELOPMENT_TEAM_PROMPT,
    NON_CODING_PROMPT,
    USER_TESTING_PROMPT,
    DEPLOYMENT_CONTEXT_PROMPT,
    GOVERNANCE_PARTICIPANTS_PROMPT
)

# ==========================
# CONFIGURATION & LOGGING
# ==========================

def load_config():
    """
    Loads configuration from the YAML file.

    Returns:
        dict: Parsed configuration dictionary.
    """
    config_path = Path("config/classifier.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


# Load configuration from YAML
config = load_config()

# Global variables from YAML
ROOT_FOLDER = config["ROOT_FOLDER"]
CLASSIFICATION_FOLDER = config["CLASSIFICATION_FOLDER"]
LOG_FILE = config["LOG_FILE"]

# Ensure necessary directories exist
os.makedirs(CLASSIFICATION_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# OpenAI API Key from environment
API_KEY = os.getenv(config["OPENAI"]["api_key_env"])
if not API_KEY:
    raise EnvironmentError(f"Environment variable '{config['github']['token_env']}' is not set.")

# OpenAI Client
client = OpenAI(api_key=API_KEY)


# ==========================
# CORE FUNCTIONS
# ==========================

def select_all_files(root_folder):
    """
    Automatically detects programming language folders and retrieves all text files.

    Args:
        root_folder (str): The base directory containing subdirectories for each language.

    Returns:
        dict: A dictionary where keys are detected language names and values are lists of file paths.
    """
    selected_files = {}
    if not os.path.exists(root_folder):
        logging.warning(f"Root folder not found: {root_folder}")
        return selected_files

    # Get all subdirectories in root_folder
    languages = [d for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]

    for language in languages:
        language_path = os.path.join(root_folder, language)
        all_files = [
            os.path.join(language_path, f)
            for f in os.listdir(language_path)
            if os.path.isfile(os.path.join(language_path, f)) and f.endswith(".txt")
        ]
        selected_files[language] = all_files if all_files else []
    
    return selected_files


def read_input_file(file_path):
    """
    Reads and returns the content of a text file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string. Returns an empty string if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading the file {file_path}: {e}")
        return ""


def save_output_to_json(output_data, input_file_path, language):
    """
    Saves the processed output data into a JSON file.

    Args:
        output_data (dict): The data to be saved, typically containing analysis results.
        input_file_path (str): The path to the original input file (used for naming the output file).
        language (str): The language associated with the input file (used for folder organization).

    Returns:
        None
    """
    try:
        output_folder = os.path.join(CLASSIFICATION_FOLDER, language)
        os.makedirs(output_folder, exist_ok=True)

        base_name = os.path.basename(input_file_path)
        output_file_name = os.path.splitext(base_name)[0] + ".json"
        output_file_path = os.path.join(output_folder, output_file_name)

        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)

        logging.info(f"Output saved to {output_file_path}")
    except Exception as e:
        logging.error(f"Error saving the output to JSON: {e}")


def process_file(file_path):
    """
    Analyzes the content of a text file using predefined prompts and returns the results.

    Args:
        file_path (str): The path to the text file to be processed.

    Returns:
        dict: A dictionary containing the results for various analysis categories.
    """
    input_text = read_input_file(file_path)
    if not input_text.strip():
        logging.warning(f"Skipping empty file: {file_path}")
        return {}

    # Create dynamic prompts for analysis
    development_team_prompt = f"{DEVELOPMENT_TEAM_PROMPT}\n\nText to analyze:\n{input_text}"
    non_coding_prompt = f"{NON_CODING_PROMPT}\n\nText to analyze:\n{input_text}"
    user_testing_prompt = f"{USER_TESTING_PROMPT}\n\nText to analyze:\n{input_text}"
    deployment_context_prompt = f"{DEPLOYMENT_CONTEXT_PROMPT}\n\nText to analyze:\n{input_text}"
    governance_participants_prompt = f"{GOVERNANCE_PARTICIPANTS_PROMPT}\n\nText to analyze:\n{input_text}"

    def analyze(prompt, label):
        """
        Sends a prompt to the OpenAI API and parses the response.

        Args:
            prompt (str): The dynamic prompt for analysis.
            label (str): A label identifying the type of analysis (for error reporting).

        Returns:
            dict: Parsed JSON results from the model's response. Returns an empty dictionary if an error occurs.
        """
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(re.search(r"\{.*\}", completion.choices[0].message.content, re.DOTALL).group(0))
        except Exception as e:
            logging.error(f"Error processing {label} for file {file_path}: {e}")
            return {}

    return {
        "development_team": analyze(development_team_prompt, "development_team"),
        "non_coding_contributors": analyze(non_coding_prompt, "non_coding_contributors"),
        "tests_with_potential_users": analyze(user_testing_prompt, "tests_with_potential_users"),
        "deployment_context": analyze(deployment_context_prompt, "deployment_context"),
        "governance_participants": analyze(governance_participants_prompt, "governance_participants")
    }


# ==========================
# EXECUTION
# ==========================

if __name__ == "__main__":
    start_time = datetime.now()
    logging.info(f"Process started at: {start_time}")

    selected_files = select_all_files(ROOT_FOLDER)

    for language, files in selected_files.items():
        for file_path in files:
            logging.info(f"Processing file: {file_path}")
            output_data = process_file(file_path)
            save_output_to_json(output_data, file_path, language)

    end_time = datetime.now()
    logging.info(f"Process finished at: {end_time}")
    logging.info(f"Total duration: {end_time - start_time}")
