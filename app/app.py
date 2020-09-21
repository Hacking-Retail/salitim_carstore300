import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_cors import CORS, cross_origin
from .models.models import setup_db, Car, Store, Customer, Bill
import json
import sys
from .models import models


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  CORS. Allow '*' for origins. Delete the sample route after
  completing the TODOs
  '''
    CORS(app, resources={r"*": {"origins": "*"}},
         supports_credentials=True)

    '''
  after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def get_home():
        try:
            return "Welcome buddy"
        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/cars', methods=['GET'])
    def get_cars():
        try:
            cars = Car.query.all()
            formated_cars = [
                cars.format() for car in cars]
            if not cars:
                abort(404)
            return jsonify({
                'success': True,
                'cars': formated_cars
            })
        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/cars/<int:car_id>', methods=['GET'])
    def get_car(car_id):
        try:
            car = Car.query.filter(
                Car.id == car_id).one_or_none()
            if car is None:
                abort(404)
            return jsonify({
                'success': True,
                'model': car.model,
                'mileage': car.mileage
            })
        except BaseException:
            abort(404)

    '''
            implement error handler for 404
            error handler should conform to general task above
        '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    return app


if __name__ == '__main__':
    create_app()
