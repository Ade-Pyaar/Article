from flask import render_template, request, flash
from article_query import app, db
import json, os

from .utils import store_articles
from .models import Articles


if not os.path.exists('article_query\\article.db'):
    try:
        db.create_all()
        store_articles(db)
    except:
        print("database existing already")




@app.route('/', methods=['POST', 'GET'])
def home():
    page_content = 'form'
    result = []
    total_persons = {}
    keyword = ''
    if request.method == 'POST':
        page_content = 'result'
        keyword = request.form.get('keyword').strip().lower()

        if keyword == '' or keyword == ' ':
            page_content = 'form'
            flash("Empty keyword is not allowed", 'danger')
            return render_template('home.html', title='Article Query', page_content=page_content, result=result)

        else:

            all_articles = Articles.query.order_by(Articles.title)

            for item in all_articles:
                if keyword in item.title.lower():
                    result.append(item)


            for item in all_articles:
                if keyword in item.keywords.lower():
                    result.append(item)

            total_persons = {}
            for item in result:
                total_persons[item.id] = json.loads(item.persons)


        if len(result) < 1:
            page_content = 'form'
            flash("No result found for you keyword, try another keyword", 'danger')

    
    return render_template('home.html', title='Article Query', page_content=page_content, result=result, total_persons=total_persons, keyword=keyword)