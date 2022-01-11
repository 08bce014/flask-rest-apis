from . import db
from .base_classes import BaseModel, MetaBaseModel
import json


class Product(db.Model,  BaseModel, metaclass=MetaBaseModel):

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_color = db.Column(db.String(50), nullable=False)
    product_details_list = db.relationship("ProductDetails", backref="product", lazy="dynamic")

    def __init__(self, product_name, product_color):
        self.product_name = product_name
        self.product_color = product_color

    def json(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})


class ProductDetails(db.Model, BaseModel, metaclass=MetaBaseModel):
    __tablename__ = "productdetails"

    id = db.Column('id', db.Integer, primary_key=True)
    description = db.Column('description', db.String(100))
    size = db.Column('size', db.String(100))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # product = db.relationship('Product')

    def __init__(self, description, size):
        self.description = description
        self.size = size

    def __repr__(self):
        return '<Product Details %r' % self.id

    def json(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})
