"""
Configuration File for GitHub Root Files Script
==============================================

Description:
------------
This configuration file provides the necessary settings for the script to 
download and organize root-level files from GitHub repositories. It includes 
API credentials, output directory paths, target file patterns, and HTTP headers.

Key Configuration Variables:
----------------------------
1. **GITHUB_TOKEN**: GitHub API token loaded from an environment variable.
2. **BASE_OUTPUT_DIR**: Directory where the downloaded root files will be stored.
3. **TARGET_FILES**: List of file name patterns to identify and download specific files.
4. **HEADERS**: HTTP headers for authenticating and formatting GitHub API requests.
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# GitHub API token loaded from environment variables
GITHUB_TOKEN = os.getenv("DIVERSITY_CARD")
if not GITHUB_TOKEN:
    raise EnvironmentError(
        "The environment variable 'DIVERSITY_CARD' is not set or is empty. "
        "Please configure it in the .env file before running the script."
    )

# Base directory for storing output files
BASE_OUTPUT_DIR = 'data/root_files'

# List of file patterns to match for downloading specific root files
TARGET_FILES = [
    "readme", "contributing", "code_of_conduct", "governance",
    "codeowners", "community", "support", "security", "release",
    "code-of-conduct"
]

# HTTP headers for GitHub API requests, including the authorization token
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}
