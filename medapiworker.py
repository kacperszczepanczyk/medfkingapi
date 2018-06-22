from Parser import Parser
from multiprocessing import Process
from iron_cache import *
import json
import time

cache = IronCache()
parser_online = Parser()
parser_highscores = Parser()

worlds = ['legacy', 'spectrum', 'destiny', 'pendulum']
professions = ['warriors', 'scouts', 'clerics', 'sorcerers', 'none', 'all']


def cache_online_players(world):
    op = parser_online.get_online_players(str(world))
    v = json.dumps([ob.as_dict() for ob in op])
    cache.put(cache="online_players", key=world, value=v)
    print('Cached online players for ' + str(world))


def cache_highscores(world, profession):
    hs = parser_highscores.get_highscores(world, profession)
    v = json.dumps(hs)
    cache.put(cache="highscores", key=world + '_' + profession, value=v)
    print('Cached higscores for  ' + str(world) + '_' + profession)


def fetch_online_players(interval):
    while True:
        time.sleep(interval)
        for world in worlds:
            cache_online_players(world)


def fetch_highscores(interval):
    while True:
        time.sleep(interval)
        for world in worlds:
            for profession in professions:
                time.sleep(2)
                cache_highscores(world, profession)


if __name__ == '__main__':
    p = Process(target=fetch_online_players, args=(10,))
    p.start()
    p1 = Process(target=fetch_highscores, args=(60,))
    p1.start()
