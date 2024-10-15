import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import urlparse

def ensure_https(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return 'https://' + url
    return url

def check_urls(urls):
    results = []
    for url in tqdm(urls, desc="Checking URLs", unit="url"):
        url = ensure_https(url)
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
        except requests.RequestException as e:
            status_code = str(e)
        results.append((url, status_code))
    return results

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

url_file_path = 'urls.txt'
urls_to_check = read_urls_from_file(url_file_path)

url_statuses = check_urls(urls_to_check)

df = pd.DataFrame(url_statuses, columns=["URL", "Status Code"])
output_file = "url_accessibility_report.xlsx"
df.to_excel(output_file, index=False)

print(f"URL accessibility report saved to {output_file}")
