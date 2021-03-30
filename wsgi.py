# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import escape
import jsonpickle

from game import Game

app = Flask(__name__)
app.secret_key = b"J|\xb1\x8b\xea';^V\x1c\xcc\xb1P\xd3\xa0\xd5"

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', grid=session['grid'], user=escape(session['username']), score=escape(session["score"]))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        game = Game()
        session['username'] = request.form['username']
        session['score'] = 0
        session['used_word'] = jsonpickle.encode(set())
        session['grid'] = game.grid
    return redirect(url_for('home'))

@app.route('/logout', methods=["GET","POST"])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/check', methods=["POST"])
def check():
    used_word_set = jsonpickle.decode(session['used_word'])

    game = Game()
    game.grid = list(request.form['grid'])
    word = request.form['word']
    is_valid = game.is_valid(word)
    is_used = word in used_word_set
    if is_valid and not is_used:
        session['score'] += len(word)
        used_word_set.add(word)
        session['used_word'] = jsonpickle.encode(used_word_set)
    return render_template(
        'home.html',
        is_valid=is_valid,
        grid=game.grid,
        word=word,
        user=escape(session['username']),
        score=escape(session["score"]),
        is_used=is_used
    )
