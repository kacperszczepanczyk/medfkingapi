from flask import Flask
from flask_restful import Resource, Api
from iron_cache import *
from Parser import *
from Memcache import Memcache
from medapiworker import *


app: Flask = Flask(__name__)
api = Api(app)
cache = IronCache()
memcache = Memcache()
parser = Parser()


class OnlinePlayers(Resource):
    def get(self, world):
       # item = cache.get(cache="online_players", key=str(world))
        item = memcache.cache.get(str(world))
        #return item.value
        return item


class Highscores(Resource):
    def get(self, world, profession):
        #item = cache.get(cache="highscores", key=str(world) + '_' + profession)
        item = memcache.cache.get('highscores_' + world + '_' + profession)
        return item
        #return item.value


class PlayerInfo(Resource):
    def get(self, name):
        return parser.get_player_info(name)

'''
class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID
'''

api.add_resource(OnlinePlayers, '/online_players/<world>')
api.add_resource(Highscores, '/highscores/<world>/<profession>')
api.add_resource(PlayerInfo, '/player_info/<name>')

if __name__ == '__main__':
    thread_manager(10)
    app.run(port='')
