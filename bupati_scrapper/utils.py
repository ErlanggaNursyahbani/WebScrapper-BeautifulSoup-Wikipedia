from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def convert_date(date_str: str):
    """
    Convert date untuk format menjadi YYYY-MM-DD.
    """
    try:
        month = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
            "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
            "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }

        # Untuk cek tanggal yang memiliki rentang waktu cth. "1 Januari 2020 – 5 Februari 2021"
        if "-" in date_str or "–" in date_str:
            date_parts = re.split(r"[-–]", date_str)
            start_date = convert_date(date_parts[0].strip())
            end_date = (
                "Present" if "sekarang" in date_parts[1].lower()
                else convert_date(date_parts[1].strip())
            )
            return start_date, end_date

        # Untuk cek tanggal yang memiliki format "1 Januari 2020"
        day, month_str, year = date_str.split()
        month_num = month[month_str]
        return f"{year}-{month_num}-{day.zfill(2)}"

    except Exception:
        return "-" 


def parse_date_range(date_text: str):
    try:
        return convert_date(date_text)  # pakai convert_date untuk mengubah format tanggal
    except Exception:
        return "-", "-"  # Default value jika gagal mengubah format tanggal
    
    
def clean_name(name: str) -> str:
    """
    Membersihkan nama dari karakter yang tidak diinginkan.
    """
    name = re.sub(r'\u200b', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\d{1,2}–\d{1,2} tahun|\d+\s*tahun,\s*\d+\s*hari', '', name)
    name = re.sub(r'\d{1,2}\s\w+\s\d{4}', '', name)
    name = re.sub(r'["“”\'’]', '', name)
    
    return name.strip()


def is_valid_name(name):
    """Check if the name is valid based on the given conditions."""
    if not name:
        return False
    if name.isdigit():  
        return False
    if len(name) <= 3:  
        return False
    return True