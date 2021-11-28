from flask import render_template, request, flash, url_for
from article_query import app, db
from .models import Articles
import os
from .utils import store_articles, scrape_articles






if not os.path.exists("article_query/article.db"):
    db.create_all()
    store_articles(db)




@app.route('/', methods=['POST', 'GET'])
def home():
    page_content = 'form'
    result = []
    if request.method == 'POST':
        page_content = 'result'
        keyword = request.form.get('keyword').strip().lower()

        all_articles = Articles.query.order_by(Articles.title)
        for item in all_articles:
            if keyword in item.title.lower():
                result.append(item)

        if len(result) < 1:
            page_content = 'form'
            flash("No result found for you keyword, try another keyword", 'danger')
    
    return render_template('home.html', title='Article Query', page_content=page_content, result=result)




@app.route('/scrape')
def scrape():
    scrape_articles()
    store_articles(db)

    return url_for('home')