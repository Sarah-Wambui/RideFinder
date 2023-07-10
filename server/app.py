#!usr/bin/env python3
from flask import  make_response, jsonify, request
from flask_restful import Resource
from config import app, db, api
from models import  Customer, Car, Review

class Index(Resource):
    def get(self):
        return make_response(jsonify({"message": "Welcome to Car/Customer/Review API"}))
api.add_resource(Index, '/')

class SignUp(Resource):
    def post(self):
        new_customer = Customer(
            username = request.form["username"]
        )
        new_customer.password_hash = request.form["_password_hash"]
        db.session.add(new_customer)
        db.session.commit()
        return make_response(jsonify(new_customer.to_dict()), 201)
api.add_resource(SignUp, "/signup")

class Login(Resource):
    def post(self):
        return f"<h1>This is the login page</h1>"
api.add_resource(Login, "/login")

class Cars(Resource):
    def get(self):
        cars = [car.to_dict() for car in Car.query.all()]
        return make_response(jsonify({"cars":cars}), 200)
api.add_resource(Cars, "/cars")

if __name__ == "__main__":
    app.run(port=5001, debug=True)