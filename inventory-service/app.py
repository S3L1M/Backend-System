from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import lorem
import random 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db2:5432/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Redis caching
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://caching-db:6379/0'
cache = Cache(app)
cache.init_app(app)

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(500))

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description


@cache.cached()
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    result = []
    for product in products:
        result.append({
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify(result)


@cache.cached(timeout=50)
@app.route('/products/<name>', methods=['GET'])
def get_product_by_name(name):
    product = Product.query.filter_by(name=name).first()
    if product:
        return jsonify({
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/products/search', methods=['GET'])
def search_product():
    keyword = request.args.get('keyword')
    products = Product.query.filter(Product.name.ilike(f'%{keyword}%')).all()
    result = []
    for product in products:
        result.append({
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify(result)


@app.route('/products/price-range', methods=['GET'])
def get_products_by_price_range():
    min_price = float(request.args.get('min_price'))
    max_price = float(request.args.get('max_price'))
    products = Product.query.filter(Product.price.between(min_price, max_price)).all()
    result = []
    for product in products:
        result.append({
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify(result)


if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()

        # Add dummy product data
        for i in range(1, 101):
            name = f'Product {i}'
            price = round(random.uniform(1.99, 999.99), 2)
            description = lorem.get_sentence(count=2)
            product = Product(name, price, description)
            db.session.add(product)
            db.session.commit()

    app.run(host='0.0.0.0', port=7000)
