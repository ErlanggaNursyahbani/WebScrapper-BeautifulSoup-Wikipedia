from bs4 import BeautifulSoup
from utils import parse_date_range

# mencari dari infobox personal info (metode pertama)
def get_roles_from_first_method(soup):
    """Extract roles and date ranges from the infobox table."""
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
                start_date, end_date = parse_date_range(date_text)
                
                roles.append((current_role, start_date, end_date))
        else:
            # If there is a <th> element, consider it as the current role
            if row.find("th"):
                current_role = text  # Set text as the current role

    return roles

# mencari dari tabel pemilu (metode kedua, tanpa asumsi dan menggunakan format yang benar)
def get_roles_from_second_method(soup):
    roles = []
    
    table = soup.find("table", class_="wikitable")
    if table:
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            columns = row.find_all("td")
            if columns:
                pemilu_year = row.find("th").get_text().strip()
                roles_start = int(pemilu_year)
                roles_end = roles_start + 5
                roles_name = columns[0].get_text().strip()

                # Jika ada informasi yang sesuai pada tabel, kita hanya ambil year
                roles.append(('Anggota Dewan Perwakilan Rakyat Republik Indonesia', f'{roles_start}-10-01', f'{roles_end}-10-01'))

    return roles

def get_roles(soup):
    """Main function to get roles from either of the methods based on availability."""
    # cara pertama
    roles = get_roles_from_first_method(soup)
    
    # cara kedua
    if not roles:
        roles = get_roles_from_second_method(soup)
    
    return roles
