"""
Text File Processor with OpenAI Integration
===========================================

Description:
------------
This script processes text files for multiple programming languages, analyzing 
their content using predefined prompts with OpenAI's GPT model. It organizes 
the results and saves them in structured JSON files for each language.

Key Features:
-------------
1. **File Selection**: Randomly selects a specified number of text files for each language.
2. **Dynamic Prompt Generation**: Creates tailored prompts for different analytical contexts.
3. **OpenAI API Integration**: Leverages GPT-4o-mini for analyzing file content.
4. **Result Storage**: Saves analysis results in JSON files, organized by language.
5. **Robust Error Handling**: Handles missing API keys, empty files, and processing errors gracefully.
6. **Environment Configuration**:
   - `.env`: Stores the OpenAI API key.
   - `config.py`: Contains global settings such as root directories, file counts, and language definitions.
"""
import os
import random
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from config import ROOT_FOLDER, LANGUAGES, FILES_PER_LANGUAGE, CLASSIFICATION_FOLDER
from prompt import SYSTEM_PROMPT, DEVELOPMENT_TEAM_PROMPT, NON_CODING_PROMPT, USER_TESTING_PROMPT, DEPLOYMENT_CONTEXT_PROMPT, GOVERNANCE_PARTICIPANTS_PROMPT


def select_random_files(root_folder, languages, files_per_language):
    """
    Selects random text files from subdirectories of a root folder for specified programming languages.

    Args:
        root_folder (str): The base directory containing subdirectories for each language.
        languages (list): A list of language names corresponding to subdirectory names.
        files_per_language (int): The number of files to randomly select per language.

    Returns:
        dict: A dictionary where keys are language names and values are lists of randomly selected file paths.
    """
    selected_files = {}
    for language in languages:
        language_path = os.path.join(root_folder, language)
        # Check if the language folder exists and is a directory
        if os.path.exists(language_path) and os.path.isdir(language_path):
            # Get all text files in the folder
            all_files = [
                os.path.join(language_path, f)
                for f in os.listdir(language_path)
                if os.path.isfile(os.path.join(language_path, f)) and f.endswith(".txt")
            ]
            # Randomly select files, up to the specified limit
            selected_files[language] = random.sample(all_files, min(len(all_files), files_per_language))
        else:
            print(f"Language folder not found or is empty: {language_path}")
            selected_files[language] = []  # If folder doesn't exist, set an empty list
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
        print(f"Error reading the file: {e}")
        return ""  # Return an empty string if there's an error


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
        # Create the classification folder by language if it doesn't exist
        output_folder = os.path.join(CLASSIFICATION_FOLDER, language)
        os.makedirs(output_folder, exist_ok=True)

        # Generate the output file name
        base_name = os.path.basename(input_file_path)
        output_file_name = os.path.splitext(base_name)[0] + ".json"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Save the output data in JSON format
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)

        print(f"Output saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving the output to JSON: {e}")

# Load variables from the .env file
load_dotenv(override=True)

# Get the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Raise an error if the API key is missing
if not api_key:
    raise ValueError("No API key found. Please set it in the '.env' file or as an environment variable.")

# Create an OpenAI client using the API key
client = OpenAI(api_key=api_key)

# Function to process a text file
def process_file(file_path):
    """
    Analyzes the content of a text file using predefined prompts and returns the results.

    Args:
        file_path (str): The path to the text file to be processed.

    Returns:
        dict: A dictionary containing the results for various analysis categories.
    """
    # Read the content of the file
    input_text = read_input_file(file_path)
    if not input_text.strip():
        print(f"Skipping empty file: {file_path}")
        return {}  # Skip processing if the file is empty

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
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract JSON content from the model's response
            return json.loads(re.search(r"\{.*\}", completion.choices[0].message.content, re.DOTALL).group(0))
        except Exception as e:
            print(f"Error processing {label} for file {file_path}: {e}")
            return {}

    # Return results for different analysis categories
    return {
        "development_team": analyze(development_team_prompt, "development_team"),
        "non_coding_contributors": analyze(non_coding_prompt, "non_coding_contributors"),
        "tests_with_potential_users": analyze(user_testing_prompt, "tests_with_potential_users"),
        "deployment_context": analyze(deployment_context_prompt, "deployment_context"),
        "governance_participants": analyze(governance_participants_prompt, "governance_participants")
    }

# Select random files for processing
selected_files = select_random_files(ROOT_FOLDER, LANGUAGES, FILES_PER_LANGUAGE)

# Process each selected file
for language, files in selected_files.items():
    for file_path in files:
        print(f"Processing file: {file_path}")
        output_data = process_file(file_path)
        save_output_to_json(output_data, file_path, language)
