import re
from utils import clean_text, convert_date

def process_birth_place(birth_place_raw):
    """Clean and format birth place."""
    birth_place_clean = re.sub(r'\[\[([^\]]+)\]\]', r'\1', birth_place_raw)
    birth_place_clean = re.sub(r'\{\{[^}]*\}\}', '', birth_place_clean)
    birth_place_clean = ' '.join(birth_place_clean.split())
    return birth_place_clean.replace("Aceh Selatan, Aceh", "Aceh Selatan Indonesia")

def extract_birth_info(soup):
    """Extract birth date and place from the infobox."""
    birth_date = "-"
    birth_place = "-"
    birth_row = soup.find("th", text="Lahir")
    if birth_row:
        td = birth_row.find_next_sibling("td")
        if td:
            full_text = clean_text(td.get_text())
            date_match = re.search(r"\d{1,2}\s\w+\s\d{4}", full_text)
            if date_match:
                birth_date = convert_date(date_match.group(0))
            birth_place = ','.join(full_text.split(',')[1:]).strip()
    return birth_date, birth_place
