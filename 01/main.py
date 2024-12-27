from flask import Flask
from bs4 import BeautifulSoup
from datetime import datetime
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
    elif currency == "EUR":
        URL = "https://cuantoestaeldolar.pe/"
        data = requests.get(URL)
        raw = data.text
        soup = BeautifulSoup(raw, 'html.parser')
        items = soup.find_all("p", class_="ValueQuotation_text___mR_0")
        return {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "sell": float(items[6].text),
            "buy": float(items[7].text),
        }
    return {"message": "NOT FOUND"}, 404