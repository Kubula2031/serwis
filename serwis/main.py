from flask import Flask, render_template, request, redirect, url_for
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


class Orders(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    owner = db.Column(db.String(40))
    car_id = db.Column(db.Integer, db.ForeignKey(Cars._id))
    status = db.Column(db.String(20))
    adddate = db.Column(db.Date)
    moddate = db.Column(db.Date)

    def __init__(self, desc, owner, car_id, status, adddate, moddate):
        self.desc = desc
        self.owner = owner
        self.car_id = car_id
        self.status = status
        self.adddate = adddate
        self.moddate = moddate


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars", methods=["POST", "GET"])
def cars():
    if request.method == "POST":
        cid = request.form["id"]
        if cid and cid.isdecimal() and Cars.query.filter_by(_id=cid).first():
            return redirect(url_for("editcar", eid=cid))
        else:
            return redirect(url_for("cars"))
    else:
        return render_template("car.html", cars=Cars.query.all())


@app.route("/addcar", methods=["POST", "GET"])
def addcar():
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        car = Cars(brand, model, date.today(), date.today())
        db.session.add(car)
        db.session.commit()
        return redirect(url_for("cars"))
    else:
        return render_template("addcar.html")


@app.route("/editcar/<eid>", methods=["POST", "GET"])
def editcar(eid):
    car = Cars.query.filter_by(_id=eid).first()
    if request.method == "POST":
        if request.form["action"] == "submit":
            brand = request.form["brand"]
            model = request.form["model"]
            car.brand = brand
            car.model = model
            car.moddate = date.today()
            db.session.commit()
            return redirect(url_for("cars"))
        else:
            Cars.query.filter_by(_id=eid).delete()
            Orders.query.filter_by(car_id=eid).delete()
            db.session.commit()
            return redirect(url_for("cars"))
    else:
        return render_template("editcar.html", car=car)


@app.route("/orders", methods=["POST", "GET"])
def orders():
    if request.method == "POST":
        oid = request.form["id"]
        if oid and oid.isdecimal() and Orders.query.filter_by(_id=oid).first():
            return redirect(url_for("editorder", eid=oid))
        else:
            return redirect(url_for("orders"))
    else:
        return render_template("orders.html", orders=Orders.query.all(), cars=Cars.query.all())


@app.route("/addorder", methods=["POST", "GET"])
def addorder():
    if request.method == "POST":
        desc = request.form["desc"]
        owner = request.form["owner"]
        car_id = request.form["car_id"]
        if Cars.query.filter_by(_id=car_id).first():
            status = "New"
            order = Orders(desc, owner, car_id, status, date.today(), date.today())
            db.session.add(order)
            db.session.commit()
            return redirect(url_for("orders"))
        else:
            return redirect(url_for("addorder"))
    else:
        return render_template("addorder.html")


@app.route("/editorder/<eid>", methods=["POST", "GET"])
def editorder(eid):
    order = Orders.query.filter_by(_id=eid).first()
    if request.method == "POST":
        if request.form["action"] == "submit":
            desc = request.form["desc"]
            owner = request.form["owner"]
            car_id = request.form["car_id"]
            status = request.form["status"]
            order.desc = desc
            order.owner = owner
            order.car_id = car_id
            order.status = status
            order.moddate = date.today()
            db.session.commit()
            return redirect(url_for("orders"))
        else:
            Orders.query.filter_by(_id=eid).delete()
            db.session.commit()
            return redirect(url_for("orders"))
    else:
        return render_template("editorder.html", order=order)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
