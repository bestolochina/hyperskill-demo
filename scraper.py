import os
import requests
from string import punctuation
from bs4 import BeautifulSoup

pages_number = int(input())
article_type = input()
for page in range(1, pages_number + 1):
    url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page={page}'
    directory = f'Page_{page}'
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    os.chdir(directory)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        if article.find("span",  attrs={'data-test': 'article.type'}).text == article_type:

            link = ('https://www.nature.com' +
                    article.find('a', attrs={'data-track-action': "view article"}, href=True)['href'])

            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                article_body = soup.find('p', attrs={"class": "article__teaser"})

                if article_body:
                    article_title = article.find('a', attrs={'data-track-action': "view article"}).text.strip()
                    for char in punctuation:
                        article_title = article_title.replace(char, '')
                    article_title = article_title.replace(' ', '_') + '.txt'  # name
                    article_text = article_body.text.strip().encode('UTF-8')  # body

                    with open(article_title, 'wb') as file:
                        file.write(article_text)
    os.chdir('..')
