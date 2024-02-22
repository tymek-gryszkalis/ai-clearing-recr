from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import requests, json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String(30), nullable = False)
    model = db.Column(db.String(30), nullable = False)
    rate = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.make} {self.model}"

@app.route("/cars", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        make = request.json["make"]
        model = request.json["model"]
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json';
        r = requests.get(url)
        modelExists = False
        for i in r.json()["Results"]:
            if i["Model_Name"] == model:
                modelExists = True
                break
        if not modelExists:
            abort(404)
        newCar = Car(make = make, model = model)
        db.session.add(newCar)
        db.session.commit()
        return {id : newCar.id}
    elif request.method == "GET":
        cars = Car.query.all()
        output = []
        for car in cars:
            output.append({"make" : car.make, "model" : car.model})
        return {"cars" : output}
