import json

def get_tags():
    tags = []
    with open('hw10\seeds\json_data/quotes.json') as file:
        quotes = json.load(file)
        for quote in quotes:
            for tag in quote['tags'].split(','):
                if tag not in tags:
                    tags.append(tag)
    return tags

def get_authors():
    with open('hw10\seeds\json_data/authors.json') as file:
        authors = json.load(file)

    return authors

def get_quotes():
    with open('hw10\seeds\json_data/quotes.json') as file:
        quotes = json.load(file)
        for quote in quotes:
            print(quote)
    return quotes
