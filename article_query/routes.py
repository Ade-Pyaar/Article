from flask import render_template, request, flash, url_for
from article_query import app
import json

from .utils import scrape_articles



with open('total.json', 'r') as file:
    total = json.load(file)




@app.route('/', methods=['POST', 'GET'])
def home():
    page_content = 'form'
    result = []
    people_links = {}
    if request.method == 'POST':
        page_content = 'result'
        keyword = request.form.get('keyword').strip().lower()

        if keyword == '' or keyword == ' ':
            page_content = 'form'
            flash("Empty keyword is not allowed", 'danger')
            return render_template('home.html', title='Article Query', page_content=page_content, result=result)

        else:

            # search the titles for the user keyword
            for key in total.keys():
                if keyword in total[key]['title'].lower():
                    result.append(total[key])

            # search the keywords for the user keyword
            for key in total.keys():
                if keyword in ','.join(total[key]['keywords']).lower():
                    result.append(total[key])


        if len(result) < 1:
            page_content = 'form'
            flash("No result found for you keyword, try another keyword", 'danger')

    
    return render_template('home.html', title='Article Query', page_content=page_content, result=result)







@app.route('/scrape')
def scrape():
    scrape_articles()

    return url_for('home')