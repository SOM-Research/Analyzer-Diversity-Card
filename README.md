# Diversity Card Analyzer

## 📋 **Overview**
This project provides a complete solution for analyzing and classifying root-level files (e.g., `README`, `CONTRIBUTING`, `CODE_OF_CONDUCT`) from a list of GitHub repositories. The tool is designed to automate the process of:
1. Extracting and organizing relevant files from repositories.
2. Performing detailed analysis of the extracted content using predefined prompts and advanced language models.

The tool is particularly useful for understanding various aspects of open-source projects, such as their governance, non-coding contributions, and adaptations for specific user groups.

---

## ✨ **Key Features**
1. **Repository Extraction**:
   - Automatically fetches specified root-level files from GitHub repositories.
   - Organizes the data by programming language for easier processing.
   - Allows filtering based on predefined patterns (e.g., `README`, `CODE_OF_CONDUCT`).

2. **Text Classification**:
   - Performs in-depth analysis of text files using a classification pipeline.
   - Utilizes prompts for specific dimensions, such as governance, user testing, and non-coding contributors.
   - Outputs structured JSON results for easy interpretation.

3. **Modular Design**:
   - **Extractor**: Responsible for fetching and organizing repository data.
   - **Classifier**: Processes extracted files and applies structured prompts to analyze content.

5. **Logging and Validation**:
   - Comprehensive logging ensures that all processes are tracked for debugging and validation.
   - Includes functionality for random file sampling during validation phases.

---

## 🔍 **Extractor**

### 📖 **Overview**
The **Extractor** module is responsible for retrieving specific root-level files from GitHub repositories. These files, such as `README`, `CONTRIBUTING`, or `CODE_OF_CONDUCT`, provide valuable insights into the structure, guidelines, and governance of open-source projects. The extracted files are organized by programming language and stored locally for further analysis.



### ⚙️ **How It Works**
1. **Configuration**:
   - The `repositories.json` file contains a list of repositories to process, specifying the repository owner, name, and primary programming language.
   - The `config.py` file defines global settings, including the output directory, target file patterns, and GitHub API token.

2. **Target File Matching**:
   - The extractor identifies files in the root directory of a repository that match a predefined list of patterns (e.g., `readme`, `code_of_conduct`).
   - Files are downloaded only if they meet these criteria.

3. **Data Organization**:
   - Extracted files are stored in a directory structure organized by programming language (`data/root_files/<language>`).
   - Each repository's files are combined into a single text file for easy processing (`<owner>_<repo>.txt`).

4. **Logging**:
   - Logs are maintained in `data/root_files/process_log.txt` to track the extraction process, including any errors or skipped files.



### 📂 **Key Files**
- **`extractor_repos.py`**: The main script for extracting repository files.
- **`config.py`**: Contains the configuration for the extractor, including API headers and file patterns.
- **`repositories.json`**: Defines the list of repositories to process.



### 🛠️ **Usage Instructions**
1. **Prepare Configuration**:
   - Ensure your GitHub API token is set in the `.env` file as `DIVERSITY_CARD`.
   - Define the list of repositories in `repositories.json` with the following structure:
     ```json
     {
       "repos": [
         { "owner": "OWNER_NAME", "name": "REPO_NAME", "language": "LANGUAGE" },
         { "owner": "OWNER_NAME", "name": "REPO_NAME", "language": "LANGUAGE" }
       ]
     }
     ```

2. **Run the Extractor**:
   Execute the extractor script to fetch and organize the repository files:
   ```bash
   python src/extractor/extractor_repos.py
   ```

3. **Output**:
   - Extracted files are stored in the `data/root_files/<language>` directory.
   - Check `data/root_files/process_log.txt` for logs of the extraction process.


### 📊 **Example Log Output**
```
2025-01-14 12:00:00 - Processing repository: microsoft/PowerToys (Language: C#)
2025-01-14 12:00:01 - Added README.md to data/root_files/c#/microsoft_PowerToys.txt
2025-01-14 12:00:02 - Skipping contributing.md in microsoft/PowerToys. Not a target file.
2025-01-14 12:00:03 - Processing repository: facebook/react (Language: JavaScript)
2025-01-14 12:00:04 - Added CODE_OF_CONDUCT.md to data/root_files/javascript/facebook_react.txt
```
The extractor ensures robustness by handling individual file errors without interrupting the overall process.

### 🌟 **Key Benefits**
- Automates the retrieval of essential files across multiple repositories.
- Organizes data efficiently for downstream classification.
- Provides detailed logs for traceability and debugging.

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
