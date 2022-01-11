from marshmallow import Schema, fields


class ProductDetailsSchema(Schema):
    id = fields.Integer(required=True)
    description = fields.Str(dump_only=True)
    size = fields.Str(dump_only=True)


class ProductSchema(Schema):
    id = fields.Integer(required=True)
    product_name = fields.Str(required=True)
    product_color = fields.Str(dump_only=True)
    product_details_list = fields.Nested(ProductDetailsSchema, many=True, required=False)

