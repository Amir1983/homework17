from flask import Flask, render_template, request,  make_response,  redirect, url_for
from models import User
import random

app = Flask(__name__)

@app.route("/")
def hello():
    email_address = request.cookies.get("email")

    if email_address:

        user = User.fetch_one(query=["email", "==", email_address])

    else:

        user = None

    return render_template("Startseite.html", user=user)
@app.route("/anmeldung", methods=["POST"])
def startseite():
    name = request.form.get("name")

    email = request.form.get("email")


    geheimzahl = random.randint(1, 10)


    user = User.fetch_one(query=["email", "==", email])

    if not user:


        user = User(name=name, email=email, geheimzahl=geheimzahl)

        user.create()


    response = make_response(redirect(url_for('hello')))

    response.set_cookie("email", email)

    return response


@app.route("/aboutus")
def aboutus():

    return render_template("aboutus.html")

@app.route("/geheimzahl", methods=["POST"])
def geheimzahl():
    zahl = int(request.form.get("zahl"))

    email_address = request.cookies.get("email")


    user = User.fetch_one(query=["email", "==", email_address])

    if zahl == user.geheimzahl:

        message = "Gewoonen, die Geheime Zahl lautet: {0}".format(str(zahl))

        neue_geheimzahl = random.randint(1, 10)


        User.edit(obj_id=user.id, geheimzahl=neue_geheimzahl)

    elif zahl > user.geheimzahl:

        message = "Deine Zahl ist zu groß... gib was kleineres ein!."

    elif zahl < user.geheimzahl:

        message = "Deine Zahl ist zu klein... gib was größeres ein!."

    return render_template("geheimzahl.html", message=message)

if __name__ =='__main__':
    app.run(debug=True)