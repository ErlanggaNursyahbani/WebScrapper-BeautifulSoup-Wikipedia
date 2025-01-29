import re
import requests

def fetch_html(url):
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {url}")
        raise e

def clean_text(text):
    """Remove extra spaces and unnecessary characters, including \xa0."""
    return re.sub(r'\s+', ' ', text.replace('\xa0', '')).strip()

def convert_date(date_str):
    """Convert date to YYYY-MM-DD format."""
    months = {
        "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
        "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
        "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
    }
    try:
        day, month, year = date_str.split()
        return f"{year}-{months[month]}-{day.zfill(2)}"
    except:
        return "-"

def parse_date_range(date_text):
    """Parse date range and return start and end dates in YYYY-MM-DD format."""
    date_text = clean_text(date_text)
    if '–' in date_text:
        start, end = date_text.split('–')
    elif '-' in date_text:
        start, end = date_text.split('-')
    else:
        return "-", "-"
    
    start_date = convert_date(start.strip())
    end_date = convert_date(end.strip())
    return start_date, end_date

def is_valid_name(name):
    """Check if the name is valid based on the given conditions."""
    if not name:
        return False
    if name.isdigit():  # If the name is just numbers (e.g., '7')
        return False
    if len(name) <= 3:  # If the name length is 3 or fewer characters
        return False
    return True