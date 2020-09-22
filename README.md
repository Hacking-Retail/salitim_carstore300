
# CARSTORE3000 

Buy a car and get it easily!

Getting Started
Pre-Requisites
Python 3.7

Follow instructions to install the latest version of python for your platform in the python docs

You need pip to for next stage

PIP Dependencies
Install dependencies by naviging to the /backend directory and running:

pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

Running the server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

export FLASK_APP=app.py
flask run


Models
Customer and Car with them attributes, Bill and Store for the place to get the gar.

Roles
Customer authentication.



## ENDPOINTS

```
GET '/cars'

return list cars

{
    "cars": [
        {
            {
            'id': 1,
            'maker': "Volvo",
            'model': "C30",
            'mileage': 100000,
            'manufacture_year': "2006",
            'engine_displacement': """,
            'engine_power': "3",
            'color_slug ': "green",
            'transmission': "manual",
            'door_count': "3",
            'seat_count': "4",
            'fuel_type': "gazoil",
            'price_eur': "5000"
        },
        ...
        
    ],

}

GET '/cars/<int:car_id>/'

return a car

{
    "car": [
        {
            "mileage": 100000,
            "model": "c30",
            "success": true
        }
    ]
}

POST '/users'

return success for new user

{
    "success": true
}

POST '/cars/<int:car_id>/bills/'

return success for new bill

{
    "success": true
}
```

##ERRORS
The application return this errors:

404: Resource not found
422: unprocessable

# Testing
To run the tests go into root folder application and run in your terminal

python test_app.py
and launch Carstore3000.postman_collection.json on postman and see result tests
