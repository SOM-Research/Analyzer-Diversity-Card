# Diversity Card Analyzer

## 📋 **Overview**
This project provides a complete solution for extracting and analyzing root-level files (e.g., `README`, `CONTRIBUTING`, `CODE_OF_CONDUCT`) from GitHub repositories. The tool is designed to:
1. **Extract** relevant files from repositories and organize them by programming language.
2. **Analyze** the extracted content using predefined prompts and AI-powered classification.

This tool is particularly useful for understanding various aspects of open-source projects, such as governance, community engagement, and documentation quality.

---

## ✨ **Key Features**
1. **Repository Extraction**:
   - Automatically fetches specified root-level files from GitHub repositories.
   - Organizes extracted data by programming language.
   - Supports configurable file patterns (e.g., `README`, `CODE_OF_CONDUCT`).

2. **Text Classification**:
   - Uses AI-powered prompts to analyze extracted files.
   - Identifies governance structures, user testing mentions, and non-coding contributions.
   - Generates structured JSON results for further analysis.

3. **Modular Design**:
   - **Extractor**: Fetches and organizes repository data.
   - **Classifier**: Processes extracted files and applies structured prompts to analyze content.
   - **Main Runner**: Automates execution of both modules.

4. **Logging and Validation**:
   - Logs all operations in dedicated log files.
   - Includes validation features for sampling and debugging.

---

## 🔍 Extractor

### 📖 Overview
The **Extractor** module automates the retrieval of specific root-level files from GitHub repositories. These files, such as `README`, `CONTRIBUTING`, and `CODE_OF_CONDUCT`, provide essential insights into the structure, guidelines, and governance of open-source projects. Extracted files are categorized by programming language and stored locally for further analysis.

### ⚙️ How It Works
1. **Configuration**:
   - The extraction process is configured through `config/extractor.yaml`, which defines:
     - GitHub API authentication
     - Target file patterns (e.g., `README.md`, `CODE_OF_CONDUCT.md`)
     - Output directory structure
   - `repositories.json` contains the list of repositories to be processed, specifying repository owner, name, and programming language.

2. **Target File Matching**:
   - The extractor scans the root directory of each repository and identifies files that match predefined patterns.
   - Only relevant files are downloaded to avoid unnecessary processing.

3. **Data Organization**:
   - Extracted files are stored in `data/root_files/<language>/`.
   - Each repository’s files are combined into a single text file named `<owner>_<repo>.txt` to facilitate structured processing.

4. **Logging**:
   - Every extraction process is logged in `logs/extractor.log`.
   - The log file contains details of processed repositories, extracted files, skipped files, and any errors encountered.

### 📂 Key Files
- **`repositories_extractor.py`** → Main script for extracting files from repositories.
- **`config/extractor.yaml`** → Configures extraction settings (API authentication, file patterns, output paths).
- **`repositories.json`** → Defines the list of repositories to be processed.

### 🛠️ Usage Instructions
1. **Prepare Configuration**:
   - Ensure `config/extractor.yaml` is correctly set up with API credentials and extraction parameters.
   - Define repositories in `repositories.json` with the following structure:
     ```json
     {
       "repos": [
         { "owner": "OWNER_NAME", "name": "REPO_NAME", "language": "LANGUAGE" },
         { "owner": "OWNER_NAME", "name": "REPO_NAME", "language": "LANGUAGE" },
       ]
     }
     ```

2. **Run the Extractor**:
   Execute the extractor script to fetch and organize repository files:
   ```bash
   python src/extractor/repositories_extractor.py
   ```

3. **Output**:
   - Extracted files are stored in `data/root_files/<language>/`.
   - Log file is available in `logs/extractor.log` for debugging and tracking the extraction process.

### 🌟 Key Benefits
✅ Automates the retrieval of essential documentation across multiple repositories.

✅ Organizes extracted data efficiently for structured analysis.

✅ Provides detailed logs for traceability and debugging.

--- 
## 🔍 Classifier

### 📖 Overview
The **Classifier** module processes and analyzes extracted root files from GitHub repositories using AI-driven text classification. It applies structured prompts to assess various aspects of open-source project documentation, such as governance participation, non-coding contributions, and user testing. The classification results are stored in JSON format for easy interpretation and further analysis.

### ⚙️ How It Works
1. **File Selection**:
   - The classifier automatically detects and processes files stored in `data/root_files/`.
   - Files are organized by programming language, and all extracted files are processed systematically.

2. **Prompt-Based Analysis**:
   - The classification process is guided by predefined prompts stored in `config/prompts.yaml`.
   - Each prompt is designed to extract specific information, such as governance structures, diversity indicators, and user testing considerations.

3. **AI Processing**:
   - The classifier interacts with an AI language model to analyze the content of each file.
   - The model's responses are parsed into structured JSON format, containing categorized insights.

4. **Output Organization**:
   - Classification results are stored in `data/classification/<language>/`.
   - Each processed file generates a corresponding JSON output, named `<file_name>.json`.

5. **Logging**:
   - Execution details, including processed files and errors, are logged in `logs/classifier.log`.

### 📂 Key Files
- **`classifier.py`** → Main script for analyzing extracted files.
- **`config/classifier.yaml`** → Configures classification settings (API authentication, output paths, prompts).
- **`prompts.py`** → Contains predefined prompts for structured analysis.

### 🛠️ Usage Instructions
1. **Prepare Configuration**:
   - Ensure `config/classifier.yaml` is correctly set up with API credentials and classification parameters.
   - Verify that the `data/root_files/` directory contains extracted files organized by language.

2. **Run the Classifier**:
   Execute the classifier script to analyze extracted files:
   ```bash
   python src/classifier/classifier.py
   ```

3. **Output**:
   - Processed results are stored in `data/classification/<language>/`.
   - Log file is available in `logs/classifier.log` for debugging and tracking the classification process.

### 📊 Example Output
```json
{
  "development_team": {
    "mention_to_dev_team": "yes",
    "profile_aspects": {
      "mentioned": "yes",
      "aspects": ["geographic diversity"]
    }
  },
  "non_coding_contributors": {
    "mention_non_coding_contributors": "no",
    "non_coding_roles": {
      "explained": "no",
      "roles": []
    }
  },
  "tests_with_potential_users": {
    "mention_tests_with_users": "yes",
    "mention_labor_force": "no",
    "mention_reporting_platforms": "no"
  },
  "deployment_context": {
    "mention_specific_use_case": "no",
    "mention_target_population": "no",
    "mention_specific_adaptation": "no"
  },
  "governance_participants": {
    "mention_governance_participants": "no",
    "mention_funders": "no"
  }
}
```

### 🌟 Key Benefits
✅ Provides structured analysis of open-source project documentation.

✅ Uses AI-driven classification for deeper insights.

✅ Outputs JSON files for seamless integration with other tools or dashboards.

✅ Comprehensive logging ensures transparency and debugging support.

