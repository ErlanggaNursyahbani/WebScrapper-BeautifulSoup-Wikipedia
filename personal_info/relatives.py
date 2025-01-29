from utils import clean_text, is_valid_name

def extract_relatives(soup):
    """Extract relatives (spouse, child, parent, sibling, relative) from the infobox."""
    relatives = []
    table = soup.find("table", class_="infobox")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            text = clean_text(row.get_text(strip=True))

            if 'Suami/istri' in text:
                spouse = row.find('td').get_text(strip=True)
                if is_valid_name(spouse):
                    relatives.append({"connection": "spouse", "description": "Suami/istri", "name": spouse})
            elif 'Anak' in text:
                children = row.find('td').get_text(strip=True).split(',')
                for child in children:
                    if is_valid_name(child.strip()):
                        relatives.append({"connection": "child", "description": "Anak", "name": child.strip()})
            elif 'Orang tua' in text:
                parents = row.find('td').get_text(strip=True).split(',')
                for parent in parents:
                    if is_valid_name(parent.strip()):
                        relatives.append({"connection": "parent", "description": "Orang tua", "name": parent.strip()})
            elif 'Saudara' in text:
                siblings = row.find('td').get_text(strip=True).split(',')
                for sibling in siblings:
                    if is_valid_name(sibling.strip()):
                        relatives.append({"connection": "sibling", "description": "Saudara", "name": sibling.strip()})
            elif 'Kerabat' in text:
                relatives_data = row.find('td').get_text(strip=True).split(',')
                for relative in relatives_data:
                    if is_valid_name(relative.strip()):
                        relatives.append({"connection": "relative", "description": "Kerabat", "name": relative.strip()})

    return relatives