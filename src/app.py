from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)


# prudto : name, id, price, description


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route('/')
def hello_world():
    return "HELLO WORLD"


@app.route('/api/products')
def show_products():
    products = Product.query.all()
    product = list()
    for item in products:
        product.append([{'id':item.id,'name':item.name}])
    return jsonify(product)

@app.route('/api/products/add', methods=["POST"])
def add_products():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "product successfully added"}), 200
    return jsonify({"message": "invalid product data"}), 400


@app.route('/api/products/delete/<int:productID>', methods=["DELETE"])
def delete_products(productID):
    product = Product.query.get(productID)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "product successfully deleted"}), 200

    return jsonify({"message": "product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
