from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.schemas import UserBlogsSchema, AddBlogSchema, FetchBlogSchema, FetchAllBlogListSchema
from src.models import UsersModel, BlogsModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request

blogs_blp = Blueprint('Blogs', __name__)

@blogs_blp.route('/blogs/all')
class BlogQueryAll(MethodView):
  @jwt_required()
  @blogs_blp.response(200, FetchAllBlogListSchema)
  def get(self):
    try:
      page = request.args.get('page', default=1, type=int)
      page_size = request.args.get('page_size', default=10, type=int)
      
      blogs = BlogsModel.query.paginate(page=page, per_page=page_size, error_out=False)
      
      allBlogs = {
        'count': blogs.total,
        'pages': blogs.pages,
        'blogs': blogs.items,
        'next_page': page + 1 if blogs.has_next else None,
        'prev_page': page - 1 if blogs.has_prev else None,
        'page_size': blogs.per_page
      }
        
      return allBlogs
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while fetching blogs', errors=repr(e))

@blogs_blp.route('/blogs')
class BlogQuery(MethodView):
  @jwt_required()
  @blogs_blp.response(200, UserBlogsSchema)
  def get(self):
    try:
      userId = get_jwt_identity()
      blogs = UsersModel.get_user_by_id(userId)
      
      if not blogs:
        abort(404, message='User not found')
        
      return blogs
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while fetching blogs', errors=repr(e))
      
  @jwt_required()
  @blogs_blp.arguments(AddBlogSchema)
  @blogs_blp.response(201, FetchBlogSchema)
  def post(self, blogData):
    try:
      userId = get_jwt_identity()
      
      newBlog = BlogsModel(**blogData, userId=userId)
      
      newBlog.create_blog()
      
      return newBlog
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while adding blog', errors=repr(e))
    except Exception as e:
      abort(500, message='Server error - An error occured while adding blog', errors=repr(e))

@blogs_blp.route('/blogs/<int:blogId>')
class BlogMutation(MethodView):
  @jwt_required()
  @blogs_blp.arguments(AddBlogSchema)
  @blogs_blp.response(200, FetchBlogSchema)
  def put(self, updatedBlogData, blogId):
    try:
      userId = get_jwt_identity()
      updatedBlog = BlogsModel(**updatedBlogData, userId=userId).update_blog(blogId)
      
      return updatedBlog
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while updating blog', errors=repr(e))
    except Exception as e:
      abort(500, message='Server error - An error occured while updating blog', errors=repr(e))
      
  @jwt_required()
  def delete(self, blogId):
    try:
      if not BlogsModel.delete_blog(blogId):
        return jsonify({'message': 'No blog deleted. Blog not found'}), 204
      
      return jsonify({'message': 'Blog deleted'}), 200
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while deleting blog', errors=repr(e))
    except Exception as e:
      abort(500, message='Server error - An error occured while deleting blog', errors=repr(e))