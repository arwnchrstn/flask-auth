from src.extensions import db
from datetime import datetime

class RevokedTokensModel(db.Model):
  __tablename__ = 'revoked_tokens'
  
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(80), nullable=False, unique=True)
  created_at = db.Column(db.DateTime, default=datetime.now())
  
  def __repr__(self) -> str:
    return f'<Token {self.jti}>'
  
  @classmethod
  def add_to_blocklist(cls, jti: str) -> None:
    revokedToken = cls(jti=jti)
    
    db.session.add(revokedToken)
    db.session.commit()
    
  @classmethod
  def token_in_blocklist(cls, jti: str) -> bool:
    if cls.query.filter(cls.jti == jti).first() == None:
      return False
    return True