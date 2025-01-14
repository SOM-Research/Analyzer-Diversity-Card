import os
import random
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT, DEVELOPMENT_TEAM_PROMPT, NON_CODING_PROMPT, USER_TESTING_PROMPT, DEPLOYMENT_CONTEXT_PROMPT, GOVERNANCE_PARTICIPANTS_PROMPT

# Configuración inicial
ROOT_FOLDER = "data/root_files"
LANGUAGES = ["c#", "python", "java", "typescript", "javascript"]
FILES_PER_LANGUAGE = 5  # Número de archivos a elegir al azar por lenguaje
CLASSIFICATION_FOLDER = "data/classification2"  # Carpeta base para guardar resultados

# Función para seleccionar archivos al azar
def select_random_files(root_folder, languages, files_per_language):
    selected_files = {}
    for language in languages:
        language_path = os.path.join(root_folder, language)
        if os.path.exists(language_path) and os.path.isdir(language_path):
            all_files = [
                os.path.join(language_path, f)
                for f in os.listdir(language_path)
                if os.path.isfile(os.path.join(language_path, f)) and f.endswith(".txt")
            ]
            selected_files[language] = random.sample(all_files, min(len(all_files), files_per_language))
        else:
            print(f"Language folder not found or is empty: {language_path}")
            selected_files[language] = []
    return selected_files

# Función para leer el contenido de un archivo de texto
def read_input_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return ""

# Función para guardar el resultado en un archivo JSON
def save_output_to_json(output_data, input_file_path, language):
    try:
        # Crear la carpeta de clasificación por lenguaje si no existe
        output_folder = os.path.join(CLASSIFICATION_FOLDER, language)
        os.makedirs(output_folder, exist_ok=True)

        # Generar el nombre del archivo de salida
        base_name = os.path.basename(input_file_path)
        output_file_name = os.path.splitext(base_name)[0] + ".json"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Guardar el resultado en formato JSON
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(output_data, json_file, ensure_ascii=False, indent=4)

        print(f"Output saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving the output to JSON: {e}")

# Cargar variables desde el archivo .env
load_dotenv(override=True)

# Obtener la clave de API desde el entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No API key found. Please set it in the '.env' file or as an environment variable.")

# Crear el cliente con la clave de API
client = OpenAI(api_key=api_key)

# Función para procesar un archivo de texto
def process_file(file_path):
    input_text = read_input_file(file_path)
    if not input_text.strip():
        print(f"Skipping empty file: {file_path}")
        return {}

    # Crear los prompts dinámicos para cada análisis
    development_team_prompt = f"{DEVELOPMENT_TEAM_PROMPT}\n\nText to analyze:\n{input_text}"
    non_coding_prompt = f"{NON_CODING_PROMPT}\n\nText to analyze:\n{input_text}"
    user_testing_prompt = f"{USER_TESTING_PROMPT}\n\nText to analyze:\n{input_text}"
    deployment_context_prompt = f"{DEPLOYMENT_CONTEXT_PROMPT}\n\nText to analyze:\n{input_text}"
    governance_participants_prompt = f"{GOVERNANCE_PARTICIPANTS_PROMPT}\n\nText to analyze:\n{input_text}"

    # Realizar las llamadas al modelo para los análisis
    def analyze(prompt, label):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(re.search(r"\{.*\}", completion.choices[0].message.content, re.DOTALL).group(0))
        except Exception as e:
            print(f"Error processing {label} for file {file_path}: {e}")
            return {}

    return {
        "development_team": analyze(development_team_prompt, "development_team"),
        "non_coding_contributors": analyze(non_coding_prompt, "non_coding_contributors"),
        "tests_with_potential_users": analyze(user_testing_prompt, "tests_with_potential_users"),
        "deployment_context": analyze(deployment_context_prompt, "deployment_context"),
        "governance_participants": analyze(governance_participants_prompt, "governance_participants")
    }

# Seleccionar archivos al azar
selected_files = select_random_files(ROOT_FOLDER, LANGUAGES, FILES_PER_LANGUAGE)

# Procesar cada archivo seleccionado
for language, files in selected_files.items():
    for file_path in files:
        print(f"Processing file: {file_path}")
        output_data = process_file(file_path)
        save_output_to_json(output_data, file_path, language)
