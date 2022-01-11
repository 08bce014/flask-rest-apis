import json

from flask import Blueprint, request, jsonify
from repository import ProductRepository
from model import Product, ProductDetails

products_api = Blueprint('products_api', __name__)


@products_api.route('/', methods=['GET'])
def get_all():
    products = Product.query.all()
    lists = list(map(lambda l: l.to_dict(), products))
    return jsonify({"products": lists})


@products_api.route('/<int:product_id>', methods=['GET'])
def get(product_id):
    product = Product.query.filter_by(id=product_id).one()
    return jsonify({"product": product.to_dict()})


@products_api.route('/', methods=['PUT'])
def create_product():
    product_json = json.loads(request.data)
    print(f"request data: {product_json.get('product_name')} and {product_json.get('product_color')}")
    product = Product(product_name=product_json.get('product_name'), product_color=product_json.get('product_color'))

    if product_json.get('product_details_list'):
        for product_details_json in product_json.get('product_details_list'):
            product_details = ProductDetails(product_details_json.get("description"), product_details_json.get("size"))
            product.product_details_list.append(product_details)
            # db.session.add(product_details)

    product_created = ProductRepository.create(product)
    product_details_list = product_created.product_details_list
    return jsonify({"product": product_created.to_dict()})


@products_api.route('/', methods=['POST'])
def update_product():
    product_json = json.loads(request.data)
    product = Product.query.filter_by(id=product_json.get('id')).one()
    product.product_color = product_json.get('product_color')
    product_saved = product.save()
    return jsonify({"product": product_saved.json})
