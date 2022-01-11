from model import Product


class ProductRepository:
    """Repository for the product model"""

    @staticmethod
    def get(product_id):
        return Product.query.filter_by(id=product_id).one()

    @staticmethod
    def get_by_name(product_name):
        return Product.query.filter_by(product_name=product_name).one()

    @staticmethod
    def update(product_name, product_color):
        product = ProductRepository.get_by_name(product_name)
        product.product_color = product_color

        return product.save()

    @staticmethod
    def create(product_name, product_color):
        """Create a new product"""
        product = Product(product_name, product_color)

        return product.save()

    @staticmethod
    def create(product):
        """Create a new product"""

        return product.save()
