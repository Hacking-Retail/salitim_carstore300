import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from .models.models import setup_db, Car, Store, Customer, Bill
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import json
import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    auth = HTTPBasicAuth()
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

    @app.route('/cars/', methods=['GET'])
    def get_cars():
        try:
            cars = Car.query.all()
            formated_cars = [
                car.format() for car in cars]
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

    @app.route('/users/', methods=['POST'])
    def new_user():
        try:
            body = request.get_json()
            name = body.get('user_name')
            password = body.get('password')
            new_user = Customer(name= name, password=generate_password_hash(password))
            new_user.insert()
            return jsonify({"success": True})
        except BaseException:
            print(sys.exc_info())
            abort(422)

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

    '''
        error handling for unprocessable entity
        '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app


if __name__ == '__main__':
    create_app()
