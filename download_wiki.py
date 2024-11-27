import requests
import sys
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import json

class WikiDownloader:
    def __init__(self, base_url, output_dir, user_agent='Wiki Offline Downloader/1.0 (Educational Purpose)'):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent
        })

    def download_page(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None

    def save_page(self, url, content):
        parsed_url = urlparse(url)
        path = parsed_url.path.strip('/')
        if not path:
            path = 'index'
            
        filepath = os.path.join(self.output_dir, f"{path}.html")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return filepath

    def get_links(self, content, current_url):
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/'):
                full_url = urljoin(self.base_url, href)
                if self.base_url in full_url and full_url not in self.visited_urls:
                    links.add(full_url)
                    
        return links

    def crawl(self, start_url, delay=1):
        queue = [start_url]
        self.visited_urls = set()
        
        while queue:
            url = queue.pop(0)
            if url in self.visited_urls:
                continue
                
            print(f"Downloading: {url}")
            content = self.download_page(url)
            if content:
                self.save_page(url, content)
                self.visited_urls.add(url)
                queue.extend(self.get_links(content, url))
                
            time.sleep(delay)  # Respect the wiki's servers
            
            # Save progress
            self.save_progress()

    def save_progress(self):
        with open(os.path.join(self.output_dir, 'progress.json'), 'w') as f:
            json.dump({
                'visited_urls': list(self.visited_urls)
            }, f)

    def load_progress(self):
        progress_file = os.path.join(self.output_dir, 'progress.json')
        if os.path.exists(progress_file):
            with open(progress_file) as f:
                data = json.load(f)
                self.visited_urls = set(data['visited_urls'])


if __name__ == '__main__':
    # Get arguments for base URL, output directory, and user agent from params

    if len(sys.argv) < 3:
        print("Usage: python download_wiki.py <base_url> <output_dir> [<user_agent>]")
        sys.exit(1)
        
    base_url = sys.argv[1]
    output_dir = sys.argv[2]
    user_agent = sys.argv[3] if len(sys.argv) > 3 else 'Wiki Offline Downloader/1.0 (Educational Purpose)'

    downloader = WikiDownloader(base_url, output_dir, user_agent)
    downloader.load_progress()
    downloader.crawl(base_url)
    
