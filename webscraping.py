import requests
from bs4 import BeautifulSoup
import string
import json
import markdownify

class WebScraper:
    def __init__(self, url):
        self.url = url
        
    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Focus on robust scraping
        # Remove unwanted elements (e.g., sidebars, ads, social media links)
        for unwanted in soup(['script', 'style', 'header', 'footer','sidebar', 'ad', 'social']):
            unwanted.extract()
        
        # Convert tables to markdown
        for table in soup.find_all('table'):
            markdown_table = markdownify.markdownify(str(table), heading_style="ATX")
            table.replace_with(BeautifulSoup(markdown_table, 'html.parser'))
        
        title = soup.find('h1').text.strip()  # Extract title
        content = soup.get_text()
        return title, content
        
class DataCleaner:
    def __init__(self, content):
        self.content = content
    
    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_stopwords(self, text):
        stopwords = ["a", "an", "the", "and", "or", "but", "if", "then", "else", "while", "for", "in", "of", "at", "on", "by", "to", "from", "with"]
        text = ' '.join([word for word in text.split() if word.upper() not in stopwords])
        return text
    
    def clean_data(self):
        # Remove punctuation
        self.content = self.remove_punctuation(self.content)
        # Convert to lower case
        self.content = self.content.lower()
        # Remove stop words
        self.content = self.remove_stopwords(self.content)
        return self.content

if __name__ == '__main__':
    with open("D:\\url.txt", 'r') as f:
        urls = f.read().splitlines()

    output = []  # Create an empty list to store output

    for i, url in enumerate(urls):
        scraper = WebScraper(url)
        title, content = scraper.scrape()  # Extract title and content
        cleaner = DataCleaner(content)
        cleaned_content = cleaner.clean_data()

        output.append({
            'URL': url,
            'Title': title, 
            'Content': content,
            'Cleaned Content': cleaned_content
        })

    # Print output
    for i, entry in enumerate(output):
        print(f"Content of page {i+1}: {entry['URL']}")
        print(f"Title: {entry['Title']}")  # Print title
        print(f"Content: {entry['Content']}")
        print(f"Cleaned Content: {entry['Cleaned Content']}")
        print("="*50)

    # Save output to a JSON file
    with open('outp.json', 'w', encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4)
