import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

KEYWORDS = ['дизайн','холла', 'преимущество', 'фото', 'web', 'python'] ## Определяем список ключевых слов

main_response = requests.get("https://habr.com/ru/articles")
main_html = main_response.text
main_soup = BeautifulSoup(main_html, features="lxml")
articles_tag = main_soup.find("div", class_="tm-articles-list")
article_tags = articles_tag.find_all("article")

parsed_data = []

for article in article_tags:
    divs = article.find_all('div', 'article-formatted-body article-formatted-body article-formatted-body_version-2')
    for div in divs:
        if div.parent.name == 'div':
            text = div.get_text().lower()
            for keyword in KEYWORDS:
                if re.search(keyword, text):

                    time_tag = article.find("time")
                    pub_time = time_tag["datetime"]

                    h2_tag = article.find("h2", class_="tm-title")
                    title = h2_tag.text.strip()

                    a_tag = h2_tag.find("a")
                    relative_link = a_tag["href"]
                    link = urljoin("https://habr.com", relative_link)
                    print(f'{pub_time} - {title} - {link}')
