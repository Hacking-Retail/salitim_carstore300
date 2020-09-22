# from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS, cross_origin
from app.app import create_app
import unittest


class TestGlobal(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_response_home(self):
        res = self.client().get('/')
        self.assertEqual(res.statut_code, 200)

if __name__ == '__main__':
    unittest.main()
