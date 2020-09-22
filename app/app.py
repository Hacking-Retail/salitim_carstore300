from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from .models.models import setup_db, Car, Customer, Bill
from flask_httpauth import HTTPBasicAuth
import sys
from flask import g


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

    @auth.verify_password
    def verify_password(username, password):
        user = Customer.query.filter_by(name=username).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True

    @app.route('/', methods=['GET'])
    def get_home():
        try:
            return "Welcome buddy"
        except BaseException:
            print(sys.exc_info())
            abort(404)

    @app.route('/cars', methods=['GET'])
    @auth.login_required
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
    @auth.login_required
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

    @app.route('/users', methods=['POST'])
    def new_user():
        try:
            body = request.get_json()
            name = body.get('user_name')
            password = body.get('password')
            if name is None or password is None:
                abort(400)  # missing arguments
            if Customer.query.filter_by(name=name).first() is not None:
                abort(400)  # existing user
            new_user = Customer(name=name)
            new_user.hash_password(password)
            new_user.insert()
            return jsonify({"success": True})
        except BaseException:
            print(sys.exc_info())
            abort(422)

    @app.route('/test', methods=['GET'])
    @auth.login_required
    def test():
        print('test')

    @app.route('/cars/<int:car_id>/bills/', methods=['POST'])
    @auth.login_required
    def buy_car(car_id):
        try:
            active_car = Car.query.filter(
                Car.id == car_id).one_or_none()
            print(active_car.format()['price_eur'])
            new_bill = Bill(price=active_car.price_eur)
            new_bill.car_id = car_id
            new_bill.cars = active_car
            new_bill.insert()
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
