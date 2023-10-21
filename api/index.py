from flask import Flask, request, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta

import certifi

ca = certifi.where()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sin1117:1234@heckweb.qw9xpz1.mongodb.net/myweb?"
mongo = PyMongo(app, tlsCAFile=ca)
app.config["SECRET_KEY"] = "abcd"

@app.route("/")
def index():
    date = request.args.get("date")
    offset = request.args.get("offset")

    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=int(offset))).strftime("%Y-%m-%d")
    
    reservation = mongo.db.heckweb
    reserved = reservation.find({"date": date})
    relist = list(reserved)
    print(relist)

    return render_template("index.html", reserved=relist, date=date)

@app.route("/floor_plan")
def floor_plan():
    return render_template("floor_plan.html")

@app.route('/reservation.html', methods=['GET', 'POST'])
def reservation():
    room = request.args.get('room')

    if request.method == 'POST':
        space = request.form.get("space")
        date = request.form.get("datepicker")
        time = request.form.getlist("time")
        name = request.form.get("name")
        password = request.form.get("password")
        
        reservation = mongo.db.heckweb
        post = {
            "space": space,
            "date": date,
            "time": time,
            "name": name,
            "password": password
        }
        reservation.insert_one(post)
        flash("예약되었습니다.")
        return redirect(url_for("index"))
    
    return render_template('reservation.html', space=room)




@app.route("/re", methods=["POST", "GET"])
def re() :
    if request.method == 'GET' :
        space = request.args.get("space")
        date = request.args.get("datepicker")

        timelist = []
        reservation = mongo.db.heckweb
        reserved = reservation.find({"space":space, "date":date})
        for i in reserved:
            for j in i["time"]:
                timelist.append(j)
        return render_template('reservation.html', space=space, date=date, reserved=timelist)
    
    else:
        space = request.form.get("space")
        date = request.form.get("date")
        time = request.form.getlist("time")
        name = request.form.get("name")
        password = request.form.get("password")
        
        reservation = mongo.db.heckweb
        post = {
            "space": space,
            "date": date,
            "time": time,
            "name": name,
            "password": password
        }
        reservation.insert_one(post)
        flash("예약되었습니다.")
        return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete():
    idx = request.form.get("idx")
    password = request.form.get("password")
    
    reservation = mongo.db.heckweb
    reserved = reservation.find_one({"_id": ObjectId(idx)})
    
    if password == reserved["password"]:
        reservation.delete_one({"_id": ObjectId(idx)})
        flash("삭제되었습니다.")
    else:
        flash("비밀번호가 올바르지 않습니다.")
    
    return redirect(url_for("index"))

@app.route("/notice")
def notice():
    return render_template("notice.html")

if __name__ == "__main__":
    app.run(debug=True, port=1117)
