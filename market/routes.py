from flask import render_template

from market import app
from market.models import Item


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/achievement')
def achievement_page():
    items = Item.query.all()
    mail = "biuro.szachy.online@gmail.com"
    return render_template('achievement.html', items=items, mail=mail)
