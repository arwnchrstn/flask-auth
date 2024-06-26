from marshmallow import fields, Schema

class PlainUserSchema(Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String(required=True)
  password = fields.String(load_only=True)

class RefreshTokenSchema(Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String(required=True)
  accessToken = fields.String(dump_only=True)

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

class FetchAllBlogListSchema(Schema):
  count = fields.Integer(dump_only=True)
  blogs = fields.List(fields.Nested(FetchBlogListSchema()), dump_only=True)
  next_page = fields.Integer(dump_only=True, allow_none=True)
  prev_page = fields.Integer(dump_only=True, allow_none=True)
  pages = fields.Integer(dump_only=True, allow_none=True)
  page_size = fields.Integer(dump_only=True)

class UserBlogsSchema(PlainUserSchema):
  blogs = fields.List(fields.Nested(FetchBlogListSchema()), dump_only=True)