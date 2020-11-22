import os
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)


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


@app.route("/add_leave", methods=["GET", "POST"])
def add_leave():
    if request.method == "POST":
        fund = {
            "employee": request.form.get("employee"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
        }
        mongo.db.annual_leave.insert_one(fund)
        flash("Leave Successfully Added. Please update Calendar")
        return redirect(url_for("get_hols"))
    return render_template("see_annual_leave_db_entries.html")


@app.route("/get_hols")
def get_hols():
    hols = mongo.db.annual_leave.find()
    return render_template("see_annual_leave_db_entries.html", hols=hols)


@app.route("/add_public_hol", methods=["GET", "POST"])
def add_public_hol():
    if request.method == "POST":
        fund = {
            "country": request.form.get("country"),
            "hol_date": request.form.get("hol_date"),
            "hol_name": request.form.get("hol_name"),
        }
        mongo.db.public_holidays.insert_one(fund)
        flash("Public Hol Successfully Added.")
        return redirect(url_for("get_public_hols"))
    return render_template("see_public_hol_db_entries.html")


@app.route("/get_public_hols")
def get_public_hols():
    phols = mongo.db.public_holidays.find()
    return render_template("see_public_hol_db_entries.html", phols=phols)


@app.route("/edit_annual_leave/<annual_leave_id>", methods=["GET", "POST"])
def edit_annual_leave(annual_leave_id):
    if request.method == "POST":
        submit = {
            "employee": request.form.get("employee"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        }
        mongo.db.annual_leave.update(
            {"_id": ObjectId(annual_leave_id)}, submit)
        flash("Leave Updated. Pleae update Google Calendar")

    hols = mongo.db.annual_leave.find_one({"_id": ObjectId(
            annual_leave_id)})
    return render_template("edit_annual_leave.html", hols=hols)


@app.route("/delete_leave/<annual_leave_id>")
def delete_leave(annual_leave_id):
    mongo.db.annual_leave.remove({"_id": ObjectId(annual_leave_id)})
    flash("Leave deleted. Please update calendar")
    return redirect(url_for("get_hols"))


@app.route("/edit_public_hols/<public_holidays_id>", methods=["GET", "POST"])
def edit_public_hols(public_holidays_id):
    if request.method == "POST":
        submit = {
            "country": request.form.get("country"),
            "hol_date": request.form.get("hol_date"),
            "hol_name": request.form.get("hol_name")
        }
        mongo.db.public_holidays.update(
            {"_id": ObjectId(public_holidays_id)}, submit)
        flash("Public Holiday Updated.")

    phols = mongo.db.public_holidays.find_one({"_id": ObjectId(
            public_holidays_id)})
    return render_template("edit_public_holidays.html", phols=phols)


@app.route("/delete_public_hols/<public_holidays_id>")
def delete_public_hols(public_holidays_id):
    mongo.db.public_holidays.remove({"_id": ObjectId(public_holidays_id)})
    flash("Public Hol deleted.")
    return redirect(url_for("get_public_hols"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
