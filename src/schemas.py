from marshmallow import fields, Schema

class PlainUserSchema(Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String(required=True)
  password = fields.String(load_only=True)

class RefreshTokenSchema(Schema):
  access_token = fields.String(dump_only=True)