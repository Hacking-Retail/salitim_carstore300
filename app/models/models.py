import os
from sqlalchemy import Column, String, Integer, create_engine, Float, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

database_name = "carstore"
database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', 'password', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Car(db.Model):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    maker = Column(String)
    model = Column(String)
    mileage = Column(Integer)
    manufacture_year = Column(String)
    engine_displacement = Column(String)
    engine_power = Column(String)
    color_slug = Column(String)
    transmission = Column(String)
    door_count = Column(Integer)
    seat_count = Column(Integer)
    fuel_type = Column(String)
    price_eur = Column(Float)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)
    bills = relationship("Bill", uselist=False, back_populates="cars")

    def __init__(self, maker, model, mileage, manufacture_year, engine_displacement, engine_power, color_slug,
                 transmission, door_count, seat_count, fuel_type, price_eur):
        self.maker = maker
        self.model = model
        self.mileage = mileage
        self.manufacture_year = manufacture_year
        self.engine_displacement = engine_displacement
        self.engine_power = engine_power
        self.color_slug = color_slug
        self.transmission = transmission
        self.door_count = door_count
        self.seat_count = seat_count
        self.fuel_type = fuel_type
        self.price_eur = price_eur

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'maker': self.maker,
            'model': self.model,
            'mileage': self.mileage,
            'manufacture_year': self.manufacture_year,
            'engine_displacement': self.engine_displacement,
            'engine_power': self.engine_power,
            'color_slug ': self.color_slug,
            'transmission': self.transmission,
            'door_count': self.door_count,
            'seat_count': self.seat_count,
            'fuel_type': self.fuel_type,
            'price_eur': self.price_eur,

        }


class Store(db.Model):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    adress = Column(String)
    cars = db.relationship("Car", backref='store', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, adress):
        self.name = name,
        self.adress = adress

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'adress': self.adress,
            }


class Customer(db.Model):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bills = db.relationship("Bill", backref='customer', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
            }


class Bill(db.Model):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    cars = relationship("Car", back_populates="bills")

    def __init__(self, price):
        self.price = price

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.price,
            }
