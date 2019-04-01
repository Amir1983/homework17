from flask import Flask, render_template, request,  make_response
import random

app = Flask(__name__)

@app.route("/")
def hello():
    geheimzahl = request.cookies.get("geheimzahl")
    response = make_response(render_template("Startseite.html"))

    if not geheimzahl:
        neue_geheimzahl = random.randint(1, 10)
        response.set_cookie("geheimzahl", str(neue_geheimzahl))

    return response

@app.route("/aboutus")
def aboutus():

    return render_template("aboutus.html")

@app.route("/geheimzahl", methods=["POST"])
def geheimzahl():
    zahl = int(request.form.get("zahl","0"))
    geheimzahl = int(request.cookies.get("geheimzahl"))

    if geheimzahl == zahl:
        message = "Super! Die Geheime Nummer: {0}".format(str(geheimzahl))

        response = make_response(render_template("gewonnen.html", message=message))

        response.set_cookie("geheimzahl", str(random.randint(1, 10)))  # set the new secret number

        return response
    elif zahl > geheimzahl:

        message = "Deine Zahl ist nicht Korrekt... nimm eine kleinere Zahl."

        return render_template("geheimzahl.html", message=message)

    elif zahl < geheimzahl:

        message = "Deine Zahl ist nicht Korrekt... nimm eine größere Zahl.."

        return render_template("geheimzahl.html", message=message)


@app.route("/gewonnen", methods=["POST"] )
def winner():
    user_name = request.cookies.get("user_name")
    name = request.form.get("name")
    nachname = request.form.get("nachname")
    adresse = request.form.get("adresse")

    print(name)
    print(nachname)
    print(adresse)
    response = make_response(render_template("Startseite.html", name=user_name ))
    response.set_cookie("user_name", name)
    return response


if __name__ =='__main__':
    app.run(debug=True)