import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

BASE_URL = "https://balena.io"

def get_links_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_links = [a['href'] for a in soup.find_all('a', href=True)]
        # Convert relative links to absolute
        absolute_links = [urljoin(url, link) for link in raw_links]
        # Filter out external links
        return [link for link in absolute_links if urlparse(link).netloc == urlparse(BASE_URL).netloc]
    except:
        return []

def find_emails_in_url(url):
    print("looking into ", url, ":")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_regex, soup.get_text())
        print(emails)
        return emails

    except:
        return []

def crawl_website_for_emails(base_url, depth=2):
    visited_urls = set()
    urls_to_visit = [(base_url, 0)]
    all_emails = set()
    
    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0)
        if current_url not in visited_urls and current_depth <= depth:
            visited_urls.add(current_url)
            emails_in_current_page = find_emails_in_url(current_url)
            all_emails.update(emails_in_current_page)
            if current_depth < depth:
                for link in get_links_from_url(current_url):
                    urls_to_visit.append((link, current_depth + 1))

    return all_emails

if __name__ == "__main__":
    emails = crawl_website_for_emails(BASE_URL)
    for email in emails:
        print(email)
