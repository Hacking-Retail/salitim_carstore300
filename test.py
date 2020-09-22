# from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS, cross_origin
from app.app import create_app
import unittest
import base64
import json
import os


class TestGlobal(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_home(self):
        res = self.client().get('/')
        self.assertEqual(res.data, b'Welcome buddy')

    # Basic authentication is needed for test with 64bit encode of (user and password):
    def test_response_cars(self):
        res = self.client().get('/cars', headers={
                "Authorization": "Basic dXNlcmJldGExOnRlc3Q="})
        print(json.loads(res.data)['success'])
        self.assertEqual(json.loads(res.data)['success'], True)

        # For Test Basic authentication is needed with 64bit encode of (user and password):

    def test_response_one_car(self):
        res = self.client().get('/cars/2', headers={
            "Authorization": "Basic dXNlcmJldGExOnRlc3Q="})
        print(json.loads(res.data)['success'])
        self.assertEqual(json.loads(res.data)['success'], True)

if __name__ == '__main__':
    unittest.main()
