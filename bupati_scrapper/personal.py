
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import utils
# personal berisi roles,birt_date,birth_place

# Extract roles information
def get_roles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find table with class 'infobox'
    table = soup.find("table", class_="infobox")
    if not table:
        return []  # Return empty list if table not found

    rows = table.find_all("tr")  # Get all rows in the table
    roles = []
    current_role = None

    for row in rows:
        text = row.get_text()  # Get the text in the row without spaces
        if not text:
            continue  # Skip empty rows
        
        # Masa jabatan
        if "Masa jabatan" in text:
            columns = row.find_all("td")
            if current_role and columns:
                # Extract date range from column
                date_text = text.replace("Masa jabatan", "").strip()
                start_date, end_date = utils.parse_date_range(date_text)
                
                roles.append((current_role, start_date, end_date))
        else:
            # If there is a <th> element, consider it as the current role
            if row.find("th"):
                current_role = text  # Set text as the current role

    return roles

# Extract birth date
def get_birth_date(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    birth_date = "-"  # Default value if birth date not found

    # Find element <th> with text "Lahir"
    birth_info_row = soup.find("th", text="Lahir")
    if birth_info_row:
        # Get the corresponding <td> element
        td = birth_info_row.find_next_sibling("td")
        if td:
            full_text = td.get_text(strip=True)
            # Look for date in the text
            match = re.search(r"\d{1,2}\s\w+\s\d{4}", full_text)
            if match:
                extracted_date = match.group(0)  # Extract the date
                # Convert the extracted date to "YYYY-MM-DD" format
                birth_date = utils.convert_date(extracted_date)

            # Validate if the text contains age or other information
            if re.search(r"\d+\s+(tahun|hari)", full_text):
                birth_date = "-"  # Return default if not valid

    return birth_date
    
# Extract birth place
def get_birth_place(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    birth_place = "-"  # Default value if birth place not found
    # Find <th> element with text "Lahir"
    th = soup.find("th", text="Lahir")
    if th:
        # Get the corresponding <td> element
        td = th.find_next_sibling("td")
        if td:
            full_text = td.get_text(strip=True)
            # Remove any text in parentheses (e.g., (umur 62))
            full_text = re.sub(r"\(.*?\)", "", full_text)
            # Use regex to extract the place of birth
            match = re.search(r"\d{1,2} \w+ \d{4}(.*)", full_text)
            if match:
                # The part after the date is considered as the birth place
                birth_place = match.group(1).strip()
    return birth_place


# contoh penggunaan
# url = 'https://id.wikipedia.org/wiki/Suhardi_Duka'
# print("== Page isi berisi tentang roles, birth date, dan birth place ==")
# roles = get_roles(url)
# birth_date = get_birth_date(url)
# birth_place = get_birth_place(url)
# print(roles)
# print(birth_date)
# print(birth_place)