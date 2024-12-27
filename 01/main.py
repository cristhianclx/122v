from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>Hello, World! Christmas</p>"

@app.route("/status/")
def status():
    return {
        "status": "live"
    }

@app.route("/students/")
def students():
    return [{
        "id": 1,
        "name": "Jesus"
    }, {
        "id": 2,
        "name": "Raul"
    }]

@app.route("/students/<name>")
def students_by_name(name):
    return "<p>Hello, World! to {}</p>".format(name)

@app.route("/exchange/<currency>")
def exchange(currency):
    if currency == "USD":
        URL = "https://www.sunat.gob.pe/a/txt/tipoCambio.txt"
        data = requests.get(URL)
        raw = data.text.split("|")
        return {
            "date": raw[0],
            "buy": raw[1],
            "sell": raw[2],
        }
    # EUR - TODO
    return {"message": "NOT FOUND"}, 404