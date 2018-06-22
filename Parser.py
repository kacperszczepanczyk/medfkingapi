import urllib
import ssl
import requests
from Utils import *
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Parser:

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_source_data_async(self, url):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            return html

    def get_source_data_req(self, url):
        try:
            return requests.get(url)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return ''

    def get_source_data(self, url):
        context = ssl._create_unverified_context()
        return urllib.request.urlopen(url, context=context).read()
    '''
        try:
            return urllib.request.urlopen(url, context=context).read()
        except IncompleteRead:
            print("INCOMPLETE READ EXCEPTION")
            # print(data)
        except urllib.error.HTTPError:
            print("HTTP ERROR EXCEPTION")
            # print(data)
        except urllib.error.URLError:
            print("URL ERROR EXCEPTION")
            # print(data)
        except ConnectionResetError:
            print("CONNECTION RESET ERROR EXCEPTION")
        except aiohttp.client_exceptions.ClientOSError:
            print("CLIENT OS ERROR EXCEPTION")
            # print(data)
        except aiohttp.ClientOSError:
            print("CLIENT OS ERROR EXCEPTION")
            # print(data)
        except aiohttp.client_exceptions.ServerDisconnectedError:
            print("SERVER DISCONNECTED ERROR EXCEPTION")
            # print(data)
        except:
            print("SOME OTHER EXCEPTION")
            # print(data)
    '''

    def get_online_players(self, world):
        online_players = list()
        url = 'http://medivia.online/community/online/' + str(world)

        parser_loop = asyncio.get_event_loop()
        data = parser_loop.run_until_complete(self.get_source_data_async(url))

        soup = BeautifulSoup(data, "html.parser")
        names = soup.find_all('div', class_='med-width-35')
        vocs = soup.find_all('div', class_='med-width-15')
        levels = soup.find_all('div', class_='med-width-25 med-text-right med-pr-40')

        players = list()
        counter = 0
        players_dict = {}
        for name, voc, level in zip(names, vocs, levels):
            players.append(Player(name.get_text(), voc.get_text(), level.get_text()))
            players_dict[counter]['name'] = name.get_text()
            players_dict[counter]['profession'] = voc.get_text()
            players_dict[counter]['level'] = level.get_text()
            counter = counter + 1

        print(players_dict)

        if players and len(players) > 2:
            del players[len(players) - 1]
            del players[0]

            for player in players:
                player.level = int(player.level)

            online_players = list(players)
            return online_players

        else:
            online_players.clear()
            return online_players

    def get_highscores(self, world, profession):
        highscores = {}
        skills = ['maglevel', 'fist', 'club', 'sword', 'axe', 'distance', 'shielding', 'fishing', 'mining']
        for skill in skills:
            url = 'https://medivia.online/highscores/' + world + '/' + profession + '/' + skill
            parser_loop = asyncio.get_event_loop()
            data = parser_loop.run_until_complete(self.get_source_data_async(url))
            #data = self.get_source_data(url)
            soup = BeautifulSoup(data, "html.parser")
            names = soup.find_all('div', class_='med-width-66')
            skill_values = soup.find_all('div', class_='med-width-35 med-text-right med-pr-40')
            highscores[skill] = {}
            for name, skill_value in zip(names, skill_values):
                highscores[skill][name.get_text()] = skill_value.get_text()

        return highscores






















