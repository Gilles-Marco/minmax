import re

# REGEX pattern to extract letter of the 
couleur_graine_pattern = re.compile(r"[R|B]", re.M)
numero_case_pattern = re.compile(r"[1][0-6]|[1-9]", re.M)

def extract_case_number(action):
    does_match = re.search(numero_case_pattern, action)
    if does_match:
        return does_match[0]
    else:
        return None

def extract_couleur(action):
    does_match = re.search(couleur_graine_pattern, action)
    if does_match:
        return does_match[0]
    else:
        return None