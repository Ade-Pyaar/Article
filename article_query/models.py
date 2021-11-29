from article_query import db


class Articles(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    persons = db.Column(db.String(5000), nullable=True)
    keywords = db.Column(db.String(500), nullable=True)