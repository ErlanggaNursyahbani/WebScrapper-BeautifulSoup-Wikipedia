import requests
from bs4 import BeautifulSoup
import pandas as pd
from personal import get_roles, get_birth_date, get_birth_place
from relatives import get_relative
import utils

# Constants
URL = "https://id.wikipedia.org/wiki/Daftar_Bupati_Bekasi"
OUTPUT_FILE = "./output/bupati_bekasi.csv"

def process_table(url):
    """
    Memproses tabel dari URL dan mengembalikan DataFrame.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    if not table:
        print("Tabel tidak ditemukan di halaman.")
        return pd.DataFrame()
    
    rows = table.find_all("tr")
    data = []

    for row in rows[1:]:  # Skip header row
        processed_row = process_table_row(row)
        if processed_row:
            data.append(processed_row)

    # Buat DataFrame dari hasil data
    df = pd.DataFrame(data)

    # Simpan ke file CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"Data berhasil disimpan ke {OUTPUT_FILE}")
    return df


def process_table_row(row):
    """
    Memproses baris tabel individual untuk mendapatkan data yang relevan.
    """
    columns = row.find_all("td")

    if len(columns) < 3:
        return None

    # Ambil nama dan link profil
    name_column = columns[2]
    name = name_column.get_text(strip=True) if name_column else "Tidak Diketahui"
    name_links = name_column.find_all("a")
    
    name = utils.clean_name(name)

    # Inisialisasi data
    profile_url = roles = birth_date = birth_place = relatives_info = None

    if name_links:
        profile_url = f"https://id.wikipedia.org{name_links[0]['href']}"
        roles = get_roles(profile_url)
        birth_date = get_birth_date(profile_url)
        birth_place = get_birth_place(profile_url)
        relatives_info = get_relative(profile_url)
    else:
        # Jika tidak ada tautan profil, gunakan informasi dari kolom lain
        role_start = columns[3].get_text(strip=True) if len(columns) > 3 else "-"
        role_end = columns[4].get_text(strip=True) if len(columns) > 4 else "-"
        role_start, role_end = utils.parse_date_range(f"{role_start} - {role_end}")
        roles = [{"role_name": "Bupati Bekasi", "role_start": role_start, "role_end": role_end}]

    return {
        "Nama": name,
        "Roles": roles,
        "Birth Date": birth_date,
        "Birth Place": birth_place,
        "Relatives": relatives_info,
        "Link Profile": profile_url or "-",
        "Link Source": URL,
    }


if __name__ == "__main__":
    process_table(URL)
