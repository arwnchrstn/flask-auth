from marshmallow import fields, Schema

class PlainUserSchema(Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String(required=True)
  password = fields.String(load_only=True)

class RefreshTokenSchema(Schema):
  access_token = fields.String(dump_only=True)

class AddBlogSchema(Schema):
  id = fields.Integer(dump_only=True)
  title = fields.String(required=True)
  content = fields.String(required=True)
  
class FetchBlogListSchema(Schema):
  id = fields.Integer(dump_only=True)
  title = fields.String(dump_only=True)

class FetchBlogSchema(FetchBlogListSchema):
  content = fields.String(dump_only=True)
  created_at = fields.DateTime(dump_only=True)

class UserBlogsSchema(PlainUserSchema):
  blogs = fields.List(fields.Nested(FetchBlogListSchema()), dump_only=True)