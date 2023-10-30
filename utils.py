import os
import re
import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print(os.getenv('OPENAI_API'))
openai.api_key = os.getenv('OPENAI_API')  # Replace with your OpenAI API key


# def validate(text):
#     def search_vicinity(keywords, pattern, text, search_range=50):
#         for keyword in keywords:
#             for match in re.finditer(re.escape(keyword), text, re.IGNORECASE):
#                 start_pos = max(0, match.start() - search_range)
#                 end_pos = match.end() + search_range
#                 vicinity_text = text[start_pos:end_pos]
#
#                 # Search for the pattern in the vicinity of the keyword
#                 pattern_match = re.search(pattern, vicinity_text)
#                 if pattern_match:
#                     return pattern_match.group()
#         return None
#
#     # Define patterns and keywords for each field
#     data_patterns = {
#         "Surname": {
#             "keywords": ["SURNAME", "ПРОЗВИЩЕ", "ФАМИЛИЯ"],
#             "pattern": r"\b[A-ZА-ЯЁ]{2,}\b"
#         },
#         "Given Name": {
#             "keywords": ["GIVEN NAMES", "ИМЯ", "ІМЯ"],
#             "pattern": r"\b[A-ZА-ЯЁ]{2,}(?:\s[A-ZА-ЯЁ]{2,})?\b"
#         },
#         "Nationality": {
#             "keywords": ["NATIONALITY", "ГРАМАДЗЯНСТВА", "НАЦИОНАЛЬНОСТЬ"],
#             "pattern": r"\b[A-ZА-ЯЁ]{4,}\b"
#         },
#         "Date of Birth": {
#             "keywords": ["DATE OF BIRTH", "ДАТА НАРАДЖЭННЯ", "ДАТА РОЖДЕНИЯ"],
#             "pattern": r"\b(\d{2}[-/\s]\d{2}[-/\s]\d{4}|\d{4}[-/\s]\d{2}[-/\s]\d{2})\b"
#         },
#         "Place of Birth": {
#             "keywords": ["PLACE OF BIRTH", "МЕСТА НАРАДЖЭННЯ", "МЕСТО РОЖДЕНИЯ"],
#             "pattern": r"\b[A-ZА-ЯЁ]{3,}(?:\s[A-ZА-ЯЁ]{2,})?\b"
#         },
#         "Authority": {
#             "keywords": ["AUTHORITY", "ОРГАН", "УПРАВЛЕНИЕ"],
#             "pattern": r"([A-ZА-ЯЁ]{2,}\s?){2,}"
#         },
#         "Passport Number": {
#             "keywords": ["PASSPORT No", "НУМАР ПАШПАРТА", "НОМЕР ПАСПОРТА"],
#             "pattern": r"\b[A-ZА-ЯЁ]{2}\d{6,9}\b"
#         },
#         "Passport Identifier": {
#             "keywords": ["IDENTIFICATION No", "ІДЭНТЫФІКАЦЫЙНЫ НУМАР", "ИДЕНТИФИКАЦИОННЫЙ НОМЕР"],
#             "pattern": r"\b[A-ZА-ЯЁ0-9]{9,}\b"
#         }
#     }
#
#     # Extracting information
#     extracted_data = {}
#     for field, info in data_patterns.items():
#         result = search_vicinity(info["keywords"], info["pattern"], text)
#         extracted_data[field] = result or "Not found"
#
#     return extracted_data


def gpt_validate(text):
    response = openai.Completion.create(
      engine="text-davinci-003",  # or the latest available model
      prompt=f"Extract the following details from the passport information:"
             f"\n{text}\n\nDetails to extract:\n1. Name\n2. Surname\n3. Nationality\n4. Date of Birth\n"
             f"5. Place of Birth\n6. Authority\n7. Passport Number\n\nProvide me with only 2 jsons. "
             f"No other words at all. Do not mention English JSON or Russian JSON. Do not translate text. "
             f"If there is no suitable value in russian, do not translate anything. No words."
             f"The first one should have English text, the second one should have russian text. "
             f"If you are not sure that this is the right value or you can not find one, still include this "
             f"key in json with value 'None'. Name should be always included. "
             f"In Russian passports the name consists of 2 words. Include both of them in field Name",
      max_tokens=500
    )
    print(response.choices[0].text)

    return response.choices[0].text.strip()

# Example usage
# text = "... (your OCR text here) ..."
# passport_data = extract_passport_data(text)
# print(passport_data)
