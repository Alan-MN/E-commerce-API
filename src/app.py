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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    loggedIn = db.Column(db.Boolean, nullable =False)

@app.route('/')
def hello_world():
    return "HELLO WORLD"


@app.route('/createUser', methods=["POST"])
def createUser():
    data = request.json
    if 'name' in data and 'password' in data and 'email' in data:
        newUser = User(name=data['name'], password=data['password'], email=data['email'],loggedIn=False)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "User successfully created"}), 200
    return jsonify({"message": "invalid user data"}), 400

@app.route('/seeUsers',methods=['GET'])
def seeUsers():
    products = User.query.all()
    product = list()
    for item in products:
        product.append([{'id': item.id, 'name': item.name,'logged_In': item.loggedIn}])
    return jsonify(product)


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

@app.route('/api/products/search/<string:productName>', methods=["GET"])
def search_product(productName):
    products = Product.query.all()
    for produto in products:
        if produto.name == productName:
            return jsonify({'name': produto.name, 'price':produto.price,'dicription':produto.description})

    return jsonify({"message": "product not found"}), 404
@app.route('/api/products/update/<int:productID>', methods=["PUT"])
def update_product(productID):
    data = request.json
    if 'name' in data and 'price' in data:
        Product.query.filter(Product.id == productID).update({
            'id': data['id'],
            'name': data['name'],
            'price': data['price'],
            'description': data['description']})
        db.session.commit()
        return jsonify({'message': ' item updated successfully'}),200

    return jsonify({'message': 'item not found'}),404



if __name__ == "__main__":
    app.run(debug=True)
