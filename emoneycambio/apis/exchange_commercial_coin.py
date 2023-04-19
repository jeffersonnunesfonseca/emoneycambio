from flask import render_template, redirect, url_for, request, Blueprint, jsonify
from marshmallow import Schema, fields
api = Blueprint('exchange_commercial_coin', __name__, url_prefix='/v1')

@api.route('/exchange_commercial_coins', methods = ['GET'])
def exchange_commercial_coins():
    from emoneycambio.services.exchange_commercial_coin import ExchangeCommercialCoin
    action = ExchangeCommercialCoin()        
    coins = action.get_updated_coins()

    return jsonify(coins)
