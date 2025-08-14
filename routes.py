from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Product
from extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    products = Product.query.all()
    in_stock_products = Product.query.filter_by(in_stock=True).all()
    return render_template("products.html", products=products, in_stock=in_stock_products)

@main.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        in_stock = request.form.get("in_stock") == "on"
        description = request.form["description"]

        new_product = Product(name=name, price=price, in_stock=in_stock, description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add_product.html")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.in_stock = request.form.get("in_stock") == "on"
        product.description = request.form["description"]
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("edit_product.html", product=product)

@main.route("/delete/<int:id>")
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/api/products", methods=["GET"])
def api_get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "in_stock": p.in_stock,
        "description": p.description
    } for p in products])

@main.route("/api/products", methods=["POST"])
def api_add_product():
    data = request.get_json()
    new_product = Product(
        name=data.get("name"),
        price=float(data.get("price", 0)),
        in_stock=bool(data.get("in_stock", True)),
        description=data.get("description", "")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price,
        "in_stock": new_product.in_stock,
        "description": new_product.description
    }), 201

@main.route("/api/products/<int:id>", methods=["PUT"])
def api_edit_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = float(data.get("price", product.price))
    product.in_stock = bool(data.get("in_stock", product.in_stock))
    product.description = data.get("description", product.description)
    db.session.commit()
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "in_stock": product.in_stock,
        "description": product.description
    })

@main.route("/api/products/<int:id>", methods=["DELETE"])
def api_delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product {id} deleted successfully."})
