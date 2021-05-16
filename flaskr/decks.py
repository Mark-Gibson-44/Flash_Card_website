from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('decks', __name__)

@bp.route('/')
def index():
    db = get_db()
    
    return render_template('index.html')

@bp.route('/browse')
def browse():
    db = get_db()
    decks = db.execute(
        'SELECT * from deck'
    ).fetchall()
    
    return render_template('decks/browse.html', decks=decks)

@bp.route('/<int:deck_id>/decks/deck_browse')
def deck_browse(deck_id):
    cards = get_cards(deck_id)
  
    return render_template('decks/deck_browse.html', card=cards)




def get_cards(deck_id):
    db = get_db()
    card = db.execute(
        """SELECT deck_id, front_card, back_card
        FROM flash_card  JOIN deck d ON deck_id = d.id
        WHERE d.id = ?""",
        (deck_id,)
    ).fetchall()

    return card


def get_all_decks():
    deck = get_db().execute(
        'SELECT id, set_name FROM deck'
    )
    
    if deck is None:
        abort(404, 'No Decks Created')
    
    return deck

@bp.route('/create',  methods=('GET', 'POST'))
@login_required
def create_deck():
    
    if request.method == 'POST':
        
        deck_title = request.form['title']
        error = None
        if not deck_title:
            error = 'Deck needs a title'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            db.execute(
                'INSERT INTO deck (set_name) VALUES (?)',
                (deck_title,)
            )
            db.commit()
            
    return render_template('decks/add.html')