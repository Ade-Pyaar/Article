from flask import render_template, request, flash
from article_query import app, db
from .models import Articles
import os, json


def store_articles():
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



if not os.path.exists("article_query/article.db"):
    db.create_all()
    store_articles()



@app.route('/', methods=['POST', 'GET'])
def home():
    page_content = 'form'
    result = []
    if request.method == 'POST':
        page_content = 'result'
        keyword = request.form.get('keyword').strip()

        all_articles = Articles.query.order_by(Articles.title)
        for item in all_articles:
            if keyword in item.keywords:
                result.append(item)

        if len(result) < 1:
            page_content = 'form'
            flash("No result found for you keyword, try another keyword", 'danger')
    
    return render_template('home.html', title='Article Query', page_content=page_content, result=result)
