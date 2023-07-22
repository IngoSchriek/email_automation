import requests
import re
import csv
import time

search_queries = ['bar', 'pub', 'igreja']

locations = ['Porto Alegre', 'Rio de Janeiro', 'São Paulo', 'Florianópolis']

email_providers = ['gmail', 'hotmail']


def search_google(query, proxy):
    base_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(base_url, params=params,
                            headers=headers, proxies={'http': proxy,
                                                      'https': proxy}, timeout=30)
    response.raise_for_status()
    print(f"Status: {response.status_code}")
    print(f'Proxy: {proxy}')
    return response.text


def extract_emails(html_content):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, html_content)
    return emails


with open("valid_proxies.txt", "r") as f:
    proxies = f.read().split('\n')

proxy_counter = 0
with open("emails_found.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)

    for search_query in search_queries:
        for location in locations:
            for email_provider in email_providers:

                query = f"{search_query} em {location} \"{email_provider}\""
                google_html = ""
                try:
                    print(f'Searching for "{query}"')
                    google_html = search_google(query, proxies[proxy_counter])
                except:
                    print('Failed')
                finally:
                    proxy_counter += 1

                    if proxy_counter == (len(proxies) - 1):
                        proxy_counter = 0

                if google_html:
                    emails_found = extract_emails(google_html)

                    for email in emails_found:
                        print(f'Extracted email: {email}')
                        csv_writer.writerow([email])
