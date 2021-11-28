from .models import Articles
import requests, json
from bs4 import BeautifulSoup


def store_articles(db):
    with open('total.json', 'r') as file:
        total_data = json.load(file)
    
    
    for key in total_data.keys():
        title = total_data[key]['title']
        article_link = total_data[key]['article_link']
        pub_date = total_data[key]['pub_link']
        persons = ','.join(total_data[key]['persons'])
        keywords = ','.join(total_data[key]['keywords'])

        new_article = Articles(
            title = title,
            link = article_link,
            date = pub_date,
            persons = persons,
            keywords = keywords,
        )

        db.session.add(new_article)

    db.session.commit()



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
                'persons': [person.get_text() for person in articles[i].find_all(attrs={"class": "link person"})],
                'keywords': [word.get_text() for word in single_html.find_all(attrs={'class': 'userdefined-keyword'})]
            }

    with open('total.json', 'w') as file:
        json.dump(total, file)

