"""
Configuration File
==================

Description:
------------
This configuration file defines the essential settings for processing files 
from multiple programming languages. It includes directory paths, target 
languages, and parameters for file selection and classification storage.

Configuration Variables:
------------------------
1. **ROOT_FOLDER**: The base directory containing the root files grouped by programming language.
2. **LANGUAGES**: A list of programming languages to process.
3. **FILES_PER_LANGUAGE**: The number of files to randomly select for each language.
4. **CLASSIFICATION_FOLDER**: The directory where the processed classification results will be stored.
"""

# Base directory containing root files grouped by language
ROOT_FOLDER = "data/root_files"

# List of programming languages to process
LANGUAGES = ["c#", "python", "java", "typescript", "javascript"]

# Number of files to randomly select per language
FILES_PER_LANGUAGE = 5

# Directory to save classification results
CLASSIFICATION_FOLDER = "data/classification2"
