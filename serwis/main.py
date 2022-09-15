from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Cars(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    brand = db.Column(db.String(20))
    model = db.Column(db.String(20))
    adddate = db.Column(db.Date)
    moddate = db.Column(db.Date)

    def __init__(self, brand, model, adddate, moddate):
        self.brand = brand
        self.model = model
        self.adddate = adddate
        self.moddate = moddate


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars", methods=["POST", "GET"])
def cars():
    if request.method == "POST":
        id = request.form["id"]
        if id:
            return redirect(url_for("editcar", id=id))
        else:
            return render_template("car.html", cars=Cars.query.all())
    else:
        return render_template("car.html", cars=Cars.query.all())


@app.route("/addcar", methods=["POST", "GET"])
def addcar():
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        addcar = date.today()
        modcar = addcar
        car = Cars(brand, model, addcar, modcar)
        db.session.add(car)
        db.session.commit()
        return render_template("car.html", cars=Cars.query.all())
    else:
        return render_template("addcar.html")


@app.route("/editcar/<id>", methods=["POST", "GET"])
def editcar(id):
    car = Cars.query.filter_by(_id=id).first()
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        addcar = car.adddate
        modcar = date.today()
        Cars.querry.filter_by(_id=id).delete()
        car = Cars(brand, model, addcar, modcar)
        db.session.add(car)
        db.session.commit()
        return render_template("car.html", cars=Cars.query.all())
    else:
        return render_template("editcar.html", car=car)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
