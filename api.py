from flask import Flask
from flask_restful import Resource, Api
from iron_cache import *


app: Flask = Flask(__name__)
api = Api(app)
cache = IronCache()


class OnlinePlayers(Resource):
    def get(self, world):
        item = cache.get(cache="online_players", key=str(world))
        return item.value


class Highscores(Resource):
    def get(self, world, profession):
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        #return jsonify(result)


'''
class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID
'''

api.add_resource(OnlinePlayers, '/online_players/<world>')
api.add_resource(Highscores, '/player_details/<player_name>')

if __name__ == '__main__':
    app.run(port='')
