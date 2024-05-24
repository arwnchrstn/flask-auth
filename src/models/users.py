from src.extensions import db
import bcrypt

class UsersModel(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(155), nullable=False, unique=True)
  password = db.Column(db.String(155), nullable=False)
  
  blogs = db.relationship('BlogsModel', back_populates='users', lazy='dynamic', cascade='all, delete')
  
  def __init__(self, username: str, password: str) -> None:
    self.username = username
    self.password = password
  
  def __repr__(self):
    return f'User <{self.username}>'
  
  def check_username_if_exists(self):
    return UsersModel.query.filter(UsersModel.username == self.username).first()
  
  def get_user_data(self):
    return self.check_username_if_exists()
  
  @classmethod
  def get_user_by_id(cls, userId):
    return cls.query.get(userId)
  
  def save_user(self):
    self.hash_password()
    
    db.session.add(self)
    db.session.commit()
    
  def hash_password(self):
    passwordBytes = self.password.encode('utf-8')
    salt = bcrypt.gensalt()
    self.password = bcrypt.hashpw(passwordBytes, salt)
    
  def delete_user(self):
    db.session.delete(self)
    db.session.commit()
    
  def verify_password(self):
    user = self.get_user_data()
    
    passwordBytes = self.password.encode('utf-8')
    hashedPwBytes = user.password.encode('utf-8')
    
    return bcrypt.checkpw(passwordBytes, hashedPwBytes)