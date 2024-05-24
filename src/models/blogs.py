from src.extensions import db
from datetime import datetime

class BlogsModel(db.Model):
  __tablename__ = 'blogs'
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  content = db.Column(db.String(1000), nullable=False)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now())
  
  users = db.relationship('UsersModel', back_populates='blogs')
  
  def __repr__(self) -> str:
    return f'<Blog {self.title}>'
  
  def __init__(self, title: str, content: str, userId: int):
    self.title = title
    self.content = content
    self.userId = userId

  def create_blog(self):
    db.session.add(self)
    db.session.commit()
  
  def update_blog(self, blogId):
    blog = self.query.get(blogId)
    
    if blog:
      blog.title = self.title
      blog.content = self.content
      
      db.session.add(blog)
      db.session.commit()
      return blog
    
    self.id = blogId
    db.session.add(self)
    db.session.commit()
    
    return self
    
  @classmethod
  def delete_blog(cls, blogId) -> bool:
    blog = cls.query.get(blogId)
    
    if not blog:
      return False
    
    db.session.delete(blog)
    db.session.commit()
    return True