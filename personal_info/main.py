import pandas as pd
from bs4 import BeautifulSoup
from utils import fetch_html
from relatives import extract_relatives
from roles import get_roles
from personal import extract_birth_info
from concurrent.futures import ThreadPoolExecutor
import os

URLS = [
    "https://id.wikipedia.org/wiki/Muhammad_Salim_Fakhry",
    "https://id.wikipedia.org/wiki/Fadhlullah",
    "https://id.wikipedia.org/wiki/Rafli",
    "https://id.wikipedia.org/wiki/Irmawan",
    "https://id.wikipedia.org/wiki/Nazaruddin_Dek_Gam",
    "https://id.wikipedia.org/wiki/Teuku_Riefky_Harsya",
    "https://id.wikipedia.org/wiki/Ruslan_M._Daud"
]

OUTPUT_DIR = "./output"

def process_data(url):
    """Process data from Wikipedia page."""
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find("h1", class_="firstHeading").get_text(strip=True)
    roles = get_roles(soup)
    birth_date, birth_place = extract_birth_info(soup)
    relatives = extract_relatives(soup)

    return {
        "Nama": name,
        "Roles": str(roles),
        "Birth Date": birth_date,
        "Birth Place": birth_place,
        "Relatives": str(relatives),
        "Link Profile": url,
        "Link Source": url
    }

def save_to_csv(data, url):
    """Save data to a CSV file named after the last part of the URL."""
    # Extract the last part of the URL after '/wiki/' and replace '_' with space
    file_name = url.split("/")[-1].replace("_", " ") + ".csv"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    
    df = pd.DataFrame([data])
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"Data berhasil disimpan ke {file_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Make sure output directory exists
    with ThreadPoolExecutor() as executor:
        all_data = list(executor.map(process_data, URLS))  # Run in parallel

    # Save each URL's data to a separate CSV file
    for data, url in zip(all_data, URLS):
        save_to_csv(data, url)

if __name__ == "__main__":
    main()
