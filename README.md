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
## 🔍 **Classifier**

### 📖 **Overview**
The **Classifier** module is responsible for analyzing the content of extracted root files from GitHub repositories. Using advanced language models and predefined prompts, it performs a structured analysis of various dimensions such as governance, user testing, and non-coding contributors. The outputs are stored in JSON format, providing a clear and organized representation of the insights gained from the analysis.


### ⚙️ **How It Works**
1. **File Selection**:
   - Files to be analyzed are selected either randomly (during validation) or by processing all files extracted in the `root_files` directory.
   - The classifier supports multiple programming languages and handles files organized by language folders.

2. **Prompts**:
   - The analysis is guided by predefined prompts stored in the `prompt` folder.
   - Each prompt is designed to extract specific information from the text, such as mentions of governance participants or non-coding contributors.

3. **Analysis**:
   - The classifier processes the text of each file and applies the corresponding prompts.
   - Outputs are generated in JSON format, with details for each analyzed dimension.

4. **Output Organization**:
   - Results are stored in the `classification` directory, organized by language.
   - Each file's output is saved as a `.json` file named after the input file.



### 📂 **Key Files**
- **`classifier.py`**: The main script for analyzing extracted files.
- **`prompt.py`**: Contains predefined prompts for different analysis dimensions.
- **`config.py`**: Configuration for the classifier, including output paths and language settings.



### 🛠️ **Usage Instructions**
1. **Prepare the Environment**:
   - Ensure your OpenAI API key is set in the `.env` file as `OPENAI_API_KEY`.
   - Verify that the `root_files` directory contains extracted files organized by language.

2. **Run the Classifier**:
   Execute the classifier script to analyze the extracted files:
   ```bash
   python src/classifier/classifier.py
   ```

3. **Output**:
   - Results are saved in the `data/classification` directory, organized by language.
   - Each result is stored as a JSON file corresponding to the input file name.



### 📊 **Example Output**

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
### 🌟 **Key Benefits**
- Provides a structured analysis of open-source project files.
- Uses advanced language models for nuanced insights.
- Outputs JSON files, making it easy to integrate with other systems or dashboards.

---
