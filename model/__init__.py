from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .product import Product
from .product import ProductDetails