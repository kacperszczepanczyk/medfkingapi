import time
import ssl
import urllib
import aiohttp
from bs4 import BeautifulSoup
from urllib.request import urlopen
from http.client import IncompleteRead
import json

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
#from flask_jsonpify import jsonify

#from medbot import Player

#db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

def printToConsole(msg):
    print("[" + str(time.asctime(time.localtime(time.time())) + "] " + str(msg)))


class Player:

    def __init__(self, name, profession, level):
        self.name = name
        self.profession = profession
        self.level = level

    def __gt__(self, other):
        return self.level > other

    def __lt__(self, other):
        return self.level < other

class OnlinePlayers(Resource):
    def get(self):

        onlinePlayers = list()
        context = ssl._create_unverified_context()
        url = 'http://medivia.online/community/online/legacy'

        print("Getting online players ")

        try:
            data = urllib.request.urlopen(url, context=context).read()
        except IncompleteRead:
            printToConsole("INCOMPLETE READ EXCEPTION")
            # print(data)
        except urllib.error.HTTPError:
            printToConsole("HTTP ERROR EXCEPTION")
            # print(data)
        except urllib.error.URLError:
            printToConsole("URL ERROR EXCEPTION")
            # print(data)
        except ConnectionResetError:
            printToConsole("CONNECTION RESET ERROR EXCEPTION")
        except aiohttp.client_exceptions.ClientOSError:
            printToConsole("CLIENT OS ERROR EXCEPTION")
            # print(data)
        except aiohttp.ClientOSError:
            printToConsole("CLIENT OS ERROR EXCEPTION")
            # print(data)
        except aiohttp.client_exceptions.ServerDisconnectedError:
            printToConsole("SERVER DISCONNECTED ERROR EXCEPTION")
            # print(data)
        except Exception:
            import traceback
            printToConsole("SOME OTHER EXCEPTION")
            # print(data)



        soup = BeautifulSoup(data, "html.parser")
        names = soup.find_all('div', class_='med-width-35')
        vocs = soup.find_all('div', class_='med-width-15')
        levels = soup.find_all('div', class_='med-width-25 med-text-right med-pr-40')

        players = list()
        for name, voc, level in zip(names, vocs, levels):
            players.append(Player(name.get_text(), voc.get_text(), level.get_text()))

        if len(players) > 2:
            del players[len(players) - 1]
            del players[0]

            for player in players:
                player.level = int(player.level)

            players.sort(reverse=True)
            onlinePlayers = list(players)
            print(onlinePlayers)
            return json.dumps([ob.__dict__ for ob in onlinePlayers])

            del players[:]
            del data

        else:
            print("Fetching online players stopped - 0 players online.")
            print(len(players))
            onlinePlayers.clear()


class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(OnlinePlayers, '/online_players')  # Route_1
api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3

if __name__ == '__main__':
    app.run(port='6098')