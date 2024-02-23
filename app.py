from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests, json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bghehbrewxjpkj:ce2faf8be88f571a3e977788f4f37ccca17fed2845012a83c8949d4426e40722@ec2-44-206-204-65.compute-1.amazonaws.com:5432/devevfvcit6mud"
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String(30), nullable = False)
    model = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f"{self.make} {self.model}"
    
class Rate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.Integer)
    carId = db.Column(db.Integer, db.ForeignKey("car.id"))

    def __repr__(self):
        return f"{self.carId}: {self.value}"

@app.route("/cars", methods = ["GET", "POST"])
def cars():
    if request.method == "POST":
        try:
            make = request.json["make"]
            model = request.json["model"]
        except:
            abort(400)
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json';
        r = requests.get(url)
        modelExists = False
        for i in r.json()["Results"]:
            if i["Model_Name"].lower() == model.lower():
                modelExists = True
                make = i["Make_Name"]
                model = i["Model_Name"]
                break
        if not modelExists:
            abort(404)
        newCar = Car(make = make, model = model)
        db.session.add(newCar)
        db.session.commit()
        return {"id" : newCar.id}
    elif request.method == "GET":
        cars = Car.query.all()
        output = []
        for car in cars:
            rates = Rate.query.filter_by(carId = car.id).all()
            if len(rates) > 0:
                avg = 0
                for rate in rates:
                    avg += rate.value
                avg /= len(rates)
                avg = round(avg, 2)
            else:
                avg = None
            output.append({"id" : car.id, "make" : car.make, "model" : car.model, "avg" : avg})
        return {"cars" : output}
    else:
        abort(500)
    
@app.route("/rate", methods = ["POST"])
def rate():
    try:
        value = request.json["value"]
        carId = request.json["id"]
        if not (value <= 5 and value >= 1):
            raise Exception
    except:
        abort(400)
    Car.query.get_or_404(carId)
    newRate = Rate(value = value, carId = carId)
    db.session.add(newRate)
    db.session.commit()
    return {"id" : newRate.id}

@app.route("/popular", methods = ["GET"])
def popular():
    try:
        amount = request.json["amount"]
        if amount < 0:
            raise Exception
    except:
        abort(400)
    sqlQuery = text(f"SELECT *, COUNT(*) FROM rate GROUP BY carId LIMIT {amount}")
    r = db.session.execute(sqlQuery).fetchall()
    output = []
    for i in r:
        car = Car.query.filter_by(id = int(i[0])).first()
        if car is None:
            break
        output.append({"id" : car.id, "make" : car.make, "model" : car.model, "numberOfRates" : i[1]})
    return {"cars" : output}