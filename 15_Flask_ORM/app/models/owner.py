from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from ..database.database import base, session
from .car import CarModel


class OwnerModel(base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    cars = relationship(CarModel, lazy='dynamic',
                        cascade="all, delete-orphan",
                        foreign_keys="CarModel.owner_id",
                        back_populates='owner')

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        owner = session.query(cls).filter_by(id=id).first()
        if not owner:
            return {}
        if to_dict:
            return cls.to_dict(owner)
        else:
            return owner

    @classmethod
    def find_by_name(cls, name, offset, limit, to_dict=True):
        owners = session.query(cls).filter_by(name=name).offset(offset).limit(limit).all()
        if not owners:
            return {"messege": f"Owner with name {name} not found"}
        if to_dict:
            return [cls.to_dict(owner) for owner in owners]
        else:
            return owners

    @classmethod
    def find_by_age(cls, age, offset, limit, to_dict=True):
        owners = session.query(cls).filter_by(age=age).offset(offset).limit(limit).all()
        if not owners:
            return {"messege": f"Owner with age {age} not found"}
        if to_dict:
            return [cls.to_dict(owner) for owner in owners]
        else:
            return owners

    @classmethod
    def return_all(cls, offset, limit):
        owners = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(owner) for owner in owners]

    @classmethod
    def delete_by_id(cls, id):
        owner = session.query(cls).filter_by(id=id).first()
        if owner:
            session.delete(owner)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(owner):
        return {
            "id": owner.id,
            "name": owner.name,
            "age": owner.age,
            "cars": [CarModel.to_dict(a) for a in owner.cars]
        }
