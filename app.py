from flask import Flask
from flask_restful import Resource, Api, abort
from flask import jsonify
import json

app = Flask(__name__)
api = Api(app)

## BASIC USER DATA

def readFile(filename):
    try:
        with open(filename,'r') as f:
            return json.load(f)
    except:
        return abort(404, message='Could not read {}'.format(filename))

class Index(Resource):
    def get(self):
        return "/data for full data ... /user/<userID> for specific user"

class GetAllData(Resource):
    def get(self):
        return readFile('data.json')
       

class GetUser(Resource):
    def get(self, user_id):
        data = readFile('data.json')
        if data.get('user'+user_id) is not None:
            return data['user'+user_id]
        abort(404, message='User {} doesn`t exist'.format(user_id))


api.add_resource(Index, '/')
api.add_resource(GetAllData, '/data')
api.add_resource(GetUser, '/user/<string:user_id>')


## POKEMON DATA



class Pokedex(Resource):
    def get(self):
        return readFile('pokemon.json')

class PokemonByID(Resource):
    def get(self, ID):
        data = readFile('pokemon.json')
        if int(ID) > len(data['pokemon']) or int(ID) < 0:
            abort(404, message='There are total 151 pokemon registered. ID {} is out of range'.format(ID))
        return data['pokemon'][int(ID)-1]

class GetAllTypes(Resource):
    def get(self):
        data = readFile('pokemon.json')
        return getTypes(data)

class GetPokemonByType(Resource):
    def get(self, pokeType):
        data = readFile('pokemon.json')
        if pokeType.lower() not in [x.lower() for x in getTypes(data)]:
            abort(400, message='Type {} doesn`t exist, for list of pokemon types check /pokedex/getAllTypes'.format(pokeType))
        res = {}
        pokemon = {}
        data = data['pokemon']
        for poke in data:
            if pokeType.lower() not in [x.lower() for x in poke['type']]:
                continue
            res[poke['id']] = poke['name']
        return res

class GetEvolutions(Resource):
    def get(self, pokemon):
        data = readFile('pokemon.json')
        data = data['pokemon']
        res = {}
        pokemonID = int(pokemon) if pokemon.isdigit() else getPokemonId(data,pokemon)
        if pokemonID is None or (pokemonID > len(data) or pokemonID < 0):            
            if pokemon.isdigit():
                abort(404, message='There are total 151 pokemon registered. ID {} is out of range'.format(pokemon))
            abort(404, message='{} is not a pokemon'.format(pokemon))
        for poke in data:
            if pokemonID != int(poke['id']):
                continue
            if 'prev_evolution' in poke:
                res['prev_evolution'] = poke['prev_evolution']
            if 'next_evolution' in poke:
                res['next_evolution'] = poke['next_evolution']
            if not bool(res):
                res['message'] = 'There are no evolutions of {}'.format(getPokemonName(data,pokemonID))

        return res


def getTypes(data):
    types = []
    for pokemon in data['pokemon']:
        for item in pokemon['type']:
            types.append(item)
    return list(set(types))

def getPokemonName(data ,Id):
    for poke in data:
        if int(poke['id']) != int(Id):
            continue
        return poke['name']
def getPokemonId(data, name):
    for poke in data:
        if poke['name'].lower() != name.lower():
            continue
        return poke['id']

api.add_resource(Pokedex, '/pokedex')
api.add_resource(PokemonByID, '/pokedex/pokemon/<string:ID>')
api.add_resource(GetAllTypes, '/pokedex/getAllTypes')
api.add_resource(GetPokemonByType, '/pokedex/getPokemonByType/<string:pokeType>')
api.add_resource(GetEvolutions, '/pokedex/getEvolutions/<string:pokemon>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

