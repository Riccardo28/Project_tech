# This file is a placeholder for database models
# When you integrate a database (e.g., SQLAlchemy), define your User model here

# Example with SQLAlchemy (uncomment when ready to use):
# from sqlalchemy import Column, Integer, String, Boolean
# from app.core.database import Base
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True, nullable=False)
#     full_name = Column(String(100), nullable=False)
#     hashed_password = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
