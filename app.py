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


@app.route("/edit_fund/<client_coverage_id>", methods=["GET", "POST"])
def edit_fund(client_coverage_id):
    if request.method == "POST":
        submit = {
            "client": request.form.get("client"),
            "owner": request.form.get("owner"),
            "fund_number": request.form.get("fund_number"),
            "first_cover": request.form.get("first_cover"),
            "second_cover": request.form.get("second_cover"),
            "third_cover": request.form.get("third_cover"),
            "contingency": request.form.get("contingency"),
            "deadline": request.form.get("deadline")
        }
        mongo.db.client_coverage.update(
            {"_id": ObjectId(client_coverage_id)}, submit)
        flash("Task Successfully Updated")

    fund = mongo.db.client_coverage.find_one({"_id": ObjectId(
            client_coverage_id)})
    return render_template("edit_fund.html", fund=fund)


@app.route("/delete_fund/<client_coverage_id>")
def delete_fund(client_coverage_id):
    mongo.db.client_coverage.remove({"_id": ObjectId(client_coverage_id)})
    flash("Fund successfully deleted")
    return redirect(url_for("get_rota"))


@app.route("/annual_leave")
def annual_leave():
    return render_template("annual_leave.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
