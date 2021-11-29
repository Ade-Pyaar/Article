import requests, json
from bs4 import BeautifulSoup




def scrape_articles():
    total = {}
    for num in range(15):

        url = f"https://pureportal.coventry.ac.uk/en/organisations/school-of-life-sciences/publications/?page={str(num)}"
        print(f"Scraping {url}")

        data = requests.get(url)

        html = BeautifulSoup(data.text, 'html.parser')

        articles = html.select('div.result-container')


        for i in range(len(articles)):

            title = articles[i].select('.link')[0].get_text()

            article_link = articles[i].select('a.link')[0].get('href')

            pub_date = articles[i].select('.date')[0].get_text()

            single_article = requests.get(article_link)

            single_html = BeautifulSoup(single_article.text, 'html.parser')

            total[i] = {
                'title': title,
                'article_link': article_link,
                'pub_link': pub_date,
                'persons': {person.get_text(): person.get('href') for person in articles[i].find_all(attrs={"class": "link person"})},            
                'keywords': [word.get_text() for word in single_html.find_all(attrs={'class': 'userdefined-keyword'})]
            }


    with open('total.json', 'w') as file:
        json.dump(total, file)