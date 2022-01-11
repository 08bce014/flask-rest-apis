from . import db
from .base_classes import BaseModel, MetaBaseModel
import json
from json import JSONEncoder


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

    # def to_str(self, v):
    #     if isinstance(v, list):
    #         lists = list(map(lambda l: l.json, v))
    #         return lists
    #     else:
    #         return str(v)

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    def reprJSON(self):
        return dict(id=self.id, product_name=self.product_name, product_color=self.product_color,
                    product_details_list=self.product_details_list)


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

    def __str__(self):
        return "{"+f"'id': {self.id},'description':{self.description},'size':{self.size}"+"}"

    def json(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    def reprJSON(self):
        return dict(id=self.id, description=self.description, size=self.size)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

# class ProductEncoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__
