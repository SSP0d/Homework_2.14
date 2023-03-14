import json
import os
from typing import List, Set
from datetime import datetime

import requests
from bs4 import BeautifulSoup

base_url = "http://quotes.toscrape.com"


def get_quotes() -> List[dict]:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_info = soup.select('div[class=quote]')

    quotes = []

    for quote_descr in quotes_info:
        quote_author = quote_descr.find('small', attrs={'class': 'author'}).text.strip()
        quote_text = quote_descr.find('span', attrs={'class': 'text'}).text.split(',')
        quote_tags = quote_descr.find('div', attrs={'class': 'tags'}).find('meta')['content']

        quote = {}

        quote['tags'] = quote_tags
        quote['author'] = quote_author
        quote['quote'] = quote_text

        quotes.append(quote)

    return quotes


def get_url_authors() -> Set[str]:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    author_links = soup.select('div[class=quote] span a')
    urls = []

    for link in author_links:
        urls.append(base_url + link['href'])

    return set(urls)


def get_authors(urls: Set[str]):
    authors = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        author_detail = soup.select('div[class=author-details]')[0]

        fullname = author_detail.find('h3', attrs={'class': 'author-title'}).text.strip().split('\n')[0]
        born_date = author_detail.find('span', attrs={'class': 'author-born-date'}).text.strip()
        born_location = author_detail.find('span', attrs={'class': 'author-born-location'}).text.strip()
        description = author_detail.find('div', attrs={'class': 'author-description'}).text.strip()

        author = {}
        author['fullname'] = fullname
        author['born_date'] = datetime.strptime(born_date, "%B %d, %Y").isoformat()
        author['born_location'] = born_location
        author['description'] = description

        authors.append(author)

    return authors


def store_in_json(filename: str, data: List[dict]):
    with open(f'json_data/{filename}', 'w', encoding='utf-8') as fd:
        json.dump(data, fd, ensure_ascii=False)


def parse_and_store_data():
    urls = get_url_authors()
    authors = get_authors(urls)
    quotes = get_quotes()
    store_in_json('authors.json', authors)
    store_in_json('quotes.json', quotes)


if __name__ == '__main__':
    parse_and_store_data()
