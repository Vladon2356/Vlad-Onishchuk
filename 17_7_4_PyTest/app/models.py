import datetime

from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import base, session


class UserModel(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(80), nullable=False)
    username = Column(String(30), nullable=False)
    hashed_password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_writer = Column(Boolean,default=False)

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        user = session.query(cls).filter_by(id=id).first()
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user

    @classmethod
    def find_by_username(cls, username, to_dict=True):
        user = session.query(cls).filter_by(username=username).first()
        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user


    @classmethod
    def find_by_email(cls, email, to_dict=True):
        user = session.query(cls).filter_by(email=email).first()

        if not user:
            return {}
        if to_dict:
            return cls.to_dict(user)
        else:
            return user


    @classmethod
    def return_all(cls, to_dict=True):
        users = session.query(cls).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(user) for user in users]
        else:
            return list(users)

    @classmethod
    def delete_by_id(cls, id):
        user = session.query(cls).filter_by(id=id).first()
        if user:
            session.delete(user)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(user):
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "email": user.email,
            "username": user.username,
            "is_admin": user.is_admin,
            "is_writer": user.is_writer
        }

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class PostModel(base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    text = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship(UserModel)

    @classmethod
    def find_by_id(cls, id,to_dict=True):
        post = session.query(cls).filter_by(id=id).first()
        if not post:
            return {"message":f"Post with id {id} not found"}, 404
        else:
            if to_dict:
                return cls.to_dict(post)
            else:
                return post

    @classmethod
    def find_by_titile(cls, title,to_dict=True):
        post = session.query(cls).filter_by(title=title).first()
        if not post:
            return {"message":f"Post with title {title} not found"}
        else:
            if to_dict:
                return cls.to_dict(post)
            else:
                return post
    @classmethod
    def find_by_author_id(cls, author_id,to_dict=True):
        posts = session.query(cls).filter_by(author_id=author_id).all()
        if not posts:
            return {"message":f"Posts by author {author_id} not found"}
        else:
            if to_dict:
                return [cls.to_dict(post) for post in posts]
            else:
                return posts

    @classmethod
    def return_all(cls, to_dict = True):
        posts = session.query(cls).order_by(cls.id).all()
        if to_dict:
            return [cls.to_dict(post) for post in posts]
        else:
            return list(posts)

    @classmethod
    def delete_by_id(cls, id):
        post = session.query(cls).filter_by(id=id).first()
        if post:
            session.delete(post)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(post):
        return {
            "id": post.id,
            "title": post.title,
            "text": post.text[:50],
            "author_id": post.author_id,
        }
class RevokedTokenModel(base):
    __tablename__ = 'revoked_tokens'
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.datetime.utcnow)

    def add(self):
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
