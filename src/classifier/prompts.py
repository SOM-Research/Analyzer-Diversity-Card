"""
Prompts for Text Analysis with OpenAI
=====================================

Description:
------------
This file contains a collection of system and contextual prompts designed for 
analyzing textual data using OpenAI's language models. The prompts are tailored 
to extract specific information from input text and return structured JSON 
outputs for various analytical purposes.

Prompts Included:
-----------------
1. **System Prompt**: Defines the model's role as an efficient text analysis assistant.
2. **Development Team Prompt**: Extracts details about mentions of development teams and their profiles.
3. **Non-Coding Prompt**: Identifies and analyzes mentions of non-coding contributors.
4. **User Testing Prompt**: Extracts information about testing practices with users, labor force, and reporting platforms.
5. **Deployment Context Prompt**: Identifies use cases, target populations, and adaptations for specific users.
6. **Governance Participants Prompt**: Analyzes mentions of governance participants and project funders.

Usage:
------
These prompts are dynamically incorporated into API calls to OpenAI's models, 
enabling consistent and precise text analysis tailored to each context.
"""

SYSTEM_PROMPT = """
You are the most capable and efficient assistant, excelling in analyzing text accurately and providing structured outputs in JSON format.
"""

DEVELOPMENT_TEAM_PROMPT = """
Analyze the following text and respond in JSON format:

1. Does the text mention **explicit** the development team?
2. Are any specific aspects of the development team mentioned (e.g., team size, geographic diversity, gender diversity, roles, expertise, etc.)? If yes, list the aspects mentioned.

Output format:
{
  "mention_to_dev_team": "yes/no",
  "profile_aspects": {
    "mentioned": "yes/no",
    "aspects": ["list of aspects if mentioned, otherwise empty"]
  }
}

Examples:

1. Input text: "The development team is composed of 5 engineers and 2 designers."
   Output:
   {
     "mention_to_dev_team": "yes",
     "profile_aspects": {
       "mentioned": "yes",
       "aspects": ["team size", "roles"]
     }
   }

2. Input text: "The development team includes engineers from the USA and Europe."
   Output:
   {
     "mention_to_dev_team": "yes",
     "profile_aspects": {
       "mentioned": "yes",
       "aspects": ["geographic diversity"]
     }
   }

3. Input text: "The team has a balanced composition of 40 % female and 60% male members."
   Output:
   {
     "mention_to_dev_team": "yes",
     "profile_aspects": {
       "mentioned": "yes",
       "aspects": ["gender diversity"]
     }
   }

4. Input text: "The development team worked tirelessly to complete the project on time."
   Output:
   {
     "mention_to_dev_team": "yes",
     "profile_aspects": {
       "mentioned": "no",
       "aspects": []
     }
   }

5. Input text: "There is no direct mention of the development team in this report."
   Output:
   {
     "mention_to_dev_team": "no",
     "profile_aspects": {
       "mentioned": "no",
       "aspects": []
     }
   }

6. Input text:
"""


NON_CODING_PROMPT = """
Analyze the following text and respond in JSON format:

  1. Does it **explicitly** mention non-coding contributors (such as Issue reporters, Advocates, Community managers, Documentors, or Translators)? (yes/no)
    - **Note**: Generic terms like "contributors" do not qualify. The mention must clearly identify specific roles such as those listed above.

  2. Are any roles of non-coding contributors explained? (yes/no)
    If yes, list the roles (e.g., Issue reporters, Advocates, Community managers, Documentors, or Translators).
    
Output format:
{
  "mention_non_coding_contributors": "yes/no",
  "non_coding_roles": {
    "explained": "yes/no",
    "roles": ["list of roles if mentioned, otherwise empty"]
  }
}

Examples:

1. Input text: "Community managers play a vital role in ensuring smooth collaboration in the project."
   Output:
   {
     "mention_non_coding_contributors": "yes",
     "non_coding_roles": {
       "explained": "yes",
       "roles": ["Community managers"]
     }
   }

2. Input text: "The project relied heavily on translators to make the documentation accessible to a global audience."
   Output:
   {
     "mention_non_coding_contributors": "yes",
     "non_coding_roles": {
       "explained": "yes",
       "roles": ["Translators"]
     }
   }

3. Input text: "Although the report focuses on developers, it does not elaborate on other contributors."
   Output:
   {
     "mention_non_coding_contributors": "yes",
     "non_coding_roles": {
       "explained": "no",
       "roles": []
     }
   }

4. Input text: "The document does not mention non-coding contributors or their roles in the project."
   Output:
   {
     "mention_non_coding_contributors": "no",
     "non_coding_roles": {
       "explained": "no",
       "roles": []
     }
   }

5. Input text: "Issue reporters and advocates collaborated to highlight the project's most critical needs."
   Output:
   {
     "mention_non_coding_contributors": "yes",
     "non_coding_roles": {
       "explained": "yes",
       "roles": ["Issue reporters", "Advocates"]
     }
   }

6. Input text: 
"""


USER_TESTING_PROMPT = """
Analyze the following text and respond in JSON format:

1. Does it mention tests with potential users (e.g., crowd-testing, beta testers)? (yes/no)
2. If yes, does it mention the use of the labor force? (yes/no)
3. Is there any mention of beta reporters or reporting platforms (e.g., app reviews in app platforms)? (yes/no)

Output format:
{
  "mention_tests_with_users": "yes/no",
  "mention_labor_force": "yes/no",
  "mention_reporting_platforms": "yes/no"
}

Examples:

1. Input text: "The app underwent rigorous testing by beta testers, who provided feedback on its performance."
   Output:
   {
     "mention_tests_with_users": "yes",
     "mention_labor_force": "no",
     "mention_reporting_platforms": "no"
   }

2. Input text: "Crowd-testing was performed, utilizing a large pool of testers to identify usability issues."
   Output:
   {
     "mention_tests_with_users": "yes",
     "mention_labor_force": "yes",
     "mention_reporting_platforms": "no"
   }

3. Input text: "User feedback was collected through app reviews on major platforms like Google Play and the App Store."
   Output:
   {
     "mention_tests_with_users": "no",
     "mention_labor_force": "no",
     "mention_reporting_platforms": "yes"
   }

4. Input text: "The project does not rely on crowd-testing or beta testers for user feedback."
   Output:
   {
     "mention_tests_with_users": "no",
     "mention_labor_force": "no",
     "mention_reporting_platforms": "no"
   }

5. Input text: "Beta testers and crowd-testing were both utilized to gather insights, and app reviews on platforms helped refine the final version."
   Output:
   {
     "mention_tests_with_users": "yes",
     "mention_labor_force": "yes",
     "mention_reporting_platforms": "yes"
   }
}

6. Input text:
"""

DEPLOYMENT_CONTEXT_PROMPT = """
Analyze the following text and respond in JSON format:

1. Does the documentation **explicitly** mention any specific use case? (yes/no)  
   A specific use case refers to a clearly stated example of how the software is intended to be used (e.g., "Servers for school management systems", ...).  
   - If yes, list the specific use cases explicitly mentioned in the text.

2. Does the documentation **explicitly** mention any specific target population? (yes/no)  
   A target population refers to a clearly stated group of users for whom the software is designed (e.g., "healthcare workers,"  "students in schools", ...).  
   - **Do not infer or assume the target population** based on the software's features or technical focus. Only consider populations explicitly named in the text.
   - If yes, list the specific target populations explicitly mentioned in the text.

3. Does the documentation explicitly mention if the software is adapted to a specific population? (yes/no)
   Adaptation refers to clearly stated adjustments made to accommodate the needs of specific groups of people, such as linguistic groups (e.g., support for Catalan speakers), professional groups (e.g., tailored tools for teachers), or people with specific accessibility needs (e.g., blind or deaf users).
   - Do not include general technical features or inferred adaptations. Only consider explicit mentions of adjustments for particular populations.
   - If yes, list the specific adaptations made for the identified groups.

Output format:
{
  "mention_specific_use_case": "yes/no",
  "specific_use_cases": [list of specific use cases or empty array],
  "mention_target_population": "yes/no",
  "specific_target_populations": [list of specific target populations or empty array],
  "mention_specific_adaptation": "yes/no",
  "specific_adaptations": [list of specific adaptations or empty array]
}

Examples:

1. Input text: "This software does resumes and is designed to help teachers and students in schools complete their assignments efficiently."
   Output:
   {
     "mention_specific_use_case": "yes",
     "specific_use_cases": ["create resumes"],
     "mention_target_population": "yes",
     "specific_target_populations": ["teachers", "students in schools"],
     "mention_specific_adaptation": "no",
     "specific_adaptations": []
   }

2. Input text: "The website is adapted to ensure visually impaired users can navigate easily."
   Output:
   {
     "mention_specific_use_case": "no",
     "specific_use_cases": [],
     "mention_target_population": "no",
     "specific_target_populations": [],
     "mention_specific_adaptation": "yes",
     "specific_adaptations": ["adapted to ensure visually impaired users can navigate easily"]
   }

3. Input text: "This app is designed for children and has been adapted to include larger text for easier reading."
   Output:
   {
     "mention_specific_use_case": "no",
     "specific_use_cases": [],
     "mention_target_population": "yes",
     "specific_target_populations": ["children"],
     "mention_specific_adaptation": "yes",
     "specific_adaptations": ["adapted to include larger text for easier reading"]
   }

4. Input text: "The software is designed to report issues, help with coding, and is intended for new developers. The software supports Catalan speakers and is specifically adapted for users with visual impairments."
   Output:
   {
     "mention_specific_use_case": "yes",
     "specific_use_cases": ["report issues", "help with coding"],
     "mention_target_population": "yes",
     "specific_target_populations": ["new developers"],
     "mention_specific_adaptation": "yes",
     "specific_adaptations": ["adapted for Catalan speakers", "adapted for users with visual impairments"]
   }

5. Input text: "This software is specifically designed for healthcare professionals working in emergency settings."
   Output:
   {
     "mention_specific_use_case": "no",
     "specific_use_cases": [],
     "mention_target_population": "yes",
     "specific_target_populations": ["healthcare professionals"],
     "mention_specific_adaptation": "no",
     "specific_adaptations": []
   }

6. Input text:
"""

GOVERNANCE_PARTICIPANTS_PROMPT = """
Analyze the following text and respond in JSON format:

1. Does the documentation mention governance participants, either as individuals or as part of an organization? (yes/no)
   - Governance participants could include individuals (e.g., "Governance is handled by a board of community leaders") or organizations (e.g., "The project is overseen by Open Source Initiative").
2. Does the documentation mention the funders of the project? (yes/no)
   - Funders could be individuals or organizations (e.g., "The project is funded by the European Commission" or "John Doe provided financial support").

Output format:
{
  "mention_governance_participants": "yes/no",
  "mention_funders": "yes/no"
}

Examples:

1. Input text: "The governance committee includes representatives from NGOs and private companies."
   Output:
   {
     "mention_governance_participants": "yes",
     "mention_funders": "no"
   }

2. Input text: "Governance decisions are made by individuals with experience in community management."
   Output:
   {
     "mention_governance_participants": "yes",
     "mention_funders": "no"
   }

3. Input text: "The project is funded by the European Commission and several private donors."
   Output:
   {
     "mention_governance_participants": "no",
     "mention_funders": "yes"
   }


4. Input text: "No governance or funding-related information is provided in this documentation."
   Output:
   {
     "mention_governance_participants": "no",
     "mention_funders": "no"
   }

5. Input text: "The governance board is managed by the Open Source Initiative, and the project receives funding from the Mozilla Foundation."
   Output:
   {
     "mention_governance_participants": "yes",
     "mention_funders": "yes"
   }

6. Input text:
"""

