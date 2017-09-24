from flask import Blueprint

bets = Blueprint('bets', __name__)

from . import endpoints