# Configuration file for the GitHub root files script
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GitHub API token
GITHUB_TOKEN = os.getenv("DIVERSITY_CARD")
if not GITHUB_TOKEN:
    raise EnvironmentError("The environment variable 'DIVERSITY_CARD' is not set or is empty. Please configure it before running the script.")

# Base directory for storing output files
BASE_OUTPUT_DIR = 'data/root_files'

# List of target file patterns to download
TARGET_FILES = [
    "readme", "contributing", "code_of_conduct", "governance",
    "codeowners", "community", "support", "security", "release",
    "code-of-conduct"
]

# HTTP headers for GitHub API requests
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}
