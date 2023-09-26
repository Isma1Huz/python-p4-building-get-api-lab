#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()

    datas = []
    for item in all_bakeries:
        data = {
            'id': item.id,
            'name': item.name,
            'created_at': item.created_at,
            'updated_at': item.updated_at
        }
        datas.append(data)
    
    return jsonify(datas)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    byprice = Bakery.query.filter_by(id=id).first()
    

    data = {
        'id': byprice.id,
        'name': byprice.name,
        'created_at': byprice.created_at,
        'updated_at': byprice.updated_at
    }
    all = make_response(jsonify(data))
    return all


@app.route('/baked_goods/by_price/<int:price>')
def baked_goods_by_price(price):
    byprice = BakedGood.query.filter(BakedGood.price == price).all()

    data = []
    for item in byprice:
        data.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'created_at': item.created_at,
            'updated_at': item.updated_at
        })

    response = make_response(
        jsonify(data),
        200
    )
    return response

    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    byprice = BakedGood.query.order_by(BakedGood.price.desc()).first()

    data = {
        'id': byprice.id,
        'name': byprice.name,
        'price': byprice.price,
        'created_at': byprice.created_at,
        'updated_at': byprice.updated_at
    }
    all = make_response(jsonify(data))
    return all
if __name__ == '__main__':
    app.run(port=5555, debug=True)
