import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_rota")
def get_rota():
    rota = mongo.db.client_coverage.find()
    return render_template("allocation.html", rota=rota)


@app.route("/add_fund", methods=["GET", "POST"])
def add_fund():
    if request.method == "POST":
        fund = {
            "client": request.form.get("client"),
            "owner": request.form.get("owner"),
            "fund_number": request.form.get("fund_number"),
            "first_cover": request.form.get("first_cover"),
            "second_cover": request.form.get("second_cover"),
            "third_cover": request.form.get("third_cover"),
            "contingency": request.form.get("contingency"),
            "deadline": request.form.get("deadline")
        }
        mongo.db.client_coverage.insert_one(fund)
        flash("Task Successfully Added")
        return render_template("allocation.html")
    return render_template("add_fund.html")    


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)