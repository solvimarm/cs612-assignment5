from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify
import json

app = Flask(__name__)
api = Api(app)

class GetAllData(Resource):
    def get(self):
        with open('data.json', 'r') as file:
            data = json.load(file)
            return data

class GetUser(Resource):
    def get(self, user_id):
        with open('data.json', 'r') as file:
            data = json.load(file)
            if data.get('user'+user_id) is not None:
                return data['user'+user_id]
            return None

api.add_resource(GetAllData, '/')
api.add_resource(GetUser, '/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)

