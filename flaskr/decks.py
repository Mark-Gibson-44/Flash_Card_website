from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('decks', __name__)

@bp.route('/')
def index():
    #db = get_db()

    return render_template('index.html')

def get_all_decks():
    deck = get_db().execute(
        'SELECT set_name FROM deck'
    )

    if deck is None:
        abort(404, 'No Decks Created')
    
    return deck