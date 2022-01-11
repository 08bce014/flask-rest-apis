import json

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import NoResultFound

from repository import ProductRepository
from model import Product, ProductDetails
from schema import ProductSchema
from exception import ServiceException

products_api = Blueprint('products_api', __name__)


@products_api.route('/', methods=['GET'])
def get_all():
    products = Product.query.all()
    product_schema = ProductSchema()
    results = product_schema.dump(products, many=True)
    return jsonify({"products": results})


@products_api.route('/<int:product_id>', methods=['GET'])
def get(product_id):
    product = Product.query.filter_by(id=product_id).one()
    product_schema = ProductSchema()
    result = product_schema.dump(product)
    return jsonify({"product": result})


@products_api.route('/', methods=['PUT'])
def create_product():
    product_json = json.loads(request.data)
    print(f"request data: {product_json.get('product_name')} and {product_json.get('product_color')}")
    product = Product(product_name=product_json.get('product_name'), product_color=product_json.get('product_color'))

    if product_json.get('product_details_list'):
        for product_details_json in product_json.get('product_details_list'):
            product_details = ProductDetails(product_details_json.get("description"), product_details_json.get("size"))
            product.product_details_list.append(product_details)

    product_created = ProductRepository.create(product)
    return jsonify({"product": product_created.to_dict()})


@products_api.route('/', methods=['POST'])
def update_product():
    product_json = json.loads(request.data)
    product = Product.query.filter_by(id=product_json.get('id')).one()
    product.product_color = product_json.get('product_color')
    product_saved = product.save()
    return jsonify({"product": product_saved.json})


@products_api.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id).one()
        if product is None:
            raise ServiceException("Product not available with given id", 500)
    except NoResultFound:
        raise ServiceException("Product not available with given id", 500)
    product.delete()
    return jsonify({"status": "Deleted"})


@products_api.errorhandler(ServiceException)
def handle_service_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
