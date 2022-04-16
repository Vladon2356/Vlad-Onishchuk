from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..database.database import base, session


class CarModel(base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(30), nullable=False, server_default='')
    price = Column(Integer, nullable=False)
    owner = relationship("OwnerModel", back_populates='cars')
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=True)

    @classmethod
    def find_by_id(cls, id, to_dict=True):
        car = session.query(cls).filter_by(id=id).first()
        if not car:
            return {"messege":f"Car with id {id} not found"}
        if to_dict:
            return cls.to_dict(car)
        else:
            return car

    @classmethod
    def find_by_brand(cls, brand: str,offset,limit, to_dict=True):
        cars = session.query(cls).filter_by(brand=brand).offset(offset).limit(limit).all()
        if not cars:
            return {"messege":f"Car with brand {brand} not found"}
        if to_dict:
            return [cls.to_dict(car) for car in cars]
        else:
            return cars

    @classmethod
    def find_by_model(cls, model: str,offset,limit, to_dict=True):
        cars = session.query(cls).filter_by(model=model).offset(offset).limit(limit).all()
        if not cars:
            return {"messege":f"Owner with model {model} not found"}
        if to_dict:
            return [cls.to_dict(car) for car in cars]
        else:
            return cars

    @classmethod
    def find_by_price(cls, price: int,offset,limit, to_dict=True):
        cars = session.query(cls).filter_by(price=price).offset(offset).limit(limit).all()
        if not cars:
            return {"messege":f"Car with price {price} not found"}
        if to_dict:
            return [cls.to_dict(car) for car in cars]
        else:
            return cars

    @classmethod
    def find_by_owner_id(cls, owner_id,offset,limit):
        cars = session.query(cls).filter_by(owner_id=owner_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(a) for a in cars]

    @classmethod
    def return_all(cls,offset, limit):
        cars = session.query(cls).order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(a) for a in cars]

    @classmethod
    def delete_by_id(cls, id):
        car = session.query(cls).filter_by(id=id).first()
        if car:
            session.delete(car)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(car):
        return {
            "id": car.id,
            "model": car.model,
            "price": car.price,
            "brand": car.brand,
            "owner_id": car.owner_id
        }
