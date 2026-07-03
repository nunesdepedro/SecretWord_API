from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.core.database import Base


class Passwords(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    website = Column(String(255))
    username = Column(String(255))

    password_encrypted = Column(String, nullable=False)

    notes = Column(Text, nullable=True)
