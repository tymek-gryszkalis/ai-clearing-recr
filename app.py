from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests, json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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
            output.append({"id" : car.id, "make" : car.make, "model" : car.model})
        return {"cars" : output}
    
@app.route("/rate", methods = ["POST"])
def rate():
    try:
        value = request.json["value"]
        carId = request.json["id"]
    except:
        abort(400)
    if not (value <= 5 and value >= 1):
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
    except:
        abort(400)
    sql = text(f"SELECT carId, COUNT(*) FROM rate GROUP BY carId LIMIT {amount}")
    r = db.session.execute(sql).fetchall()
    output = []
    for i in r:
        car = Car.query.filter_by(id = int(i[0])).first()
        output.append({"id" : car.id, "make" : car.make, "model" : car.model, "numberOfRates" : i[1]})
    return {"cars" : output}