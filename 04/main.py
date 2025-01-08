from flask import Flask, request
from flask_restful import Resource, Api
import requests
from spellchecker import SpellChecker
from bs4 import BeautifulSoup
from datetime import datetime


spell = SpellChecker()

app = Flask(__name__)

api = Api(app)


class StatusResource(Resource):
    def get(self):
        return {
            "status": "live"
        }


class PokemonByNameResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        data = raw.json()
        moves = []
        for m in data["moves"]:
            moves.append(m["move"]["name"])
        return {
            "id": name,
            "experience": data["base_experience"],
            "height": data["height"],
            "weight": data["weight"],
            "moves": moves,
        }


class CorrectSentenceResource(Resource):
    def post(self):
        q = request.get_json().get("q")
        print(q)
        new_sentence = []
        for n in q.split(" "):
            new_sentence.append(spell.correction(n))
        q_fixed = " ".join(new_sentence)
        return {"q": q_fixed}


class ExchangeResource(Resource):
    def get(self, currency):
        currency = currency.upper()
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
            URL = "https://cuantoestaeldolar.pe/otras-divisas"
            data = requests.get(URL)
            raw = data.text
            soup = BeautifulSoup(raw, 'html.parser')
            items = soup.find_all("p", class_="ValueCurrency_item_cost__Eb_37")
            return {
                "date": datetime.now().strftime("%d/%m/%Y"),
                "sell": float(items[4].text),
                "buy": float(items[5].text),
            }
        else:
            return {}, 400


api.add_resource(StatusResource, "/status/")
api.add_resource(PokemonByNameResource, "/pokemon/<name>/")
api.add_resource(CorrectSentenceResource, "/correct-sentence/")
api.add_resource(ExchangeResource, "/exchange/<currency>/")