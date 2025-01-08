from flask import Flask, request
from flask_restful import Resource, Api
import requests


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
        # LABORATORIO
        # use pyspellchecker
        # return {"q": "texto arreglado"}


class ExchangeResource(Resource):
    def get(self, currency):
        # LABORATORIO
        # if USD -> 
        # if EUR -> 
        print("-")


api.add_resource(StatusResource, "/status/")
api.add_resource(PokemonByNameResource, "/pokemon/<name>/")
api.add_resource(CorrectSentenceResource, "/correct-sentence/")
api.add_resource(ExchangeResource, "/exchange/<currency>")