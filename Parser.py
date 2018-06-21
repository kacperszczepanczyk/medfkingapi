import aiohttp
import urllib
import ssl
from Utils import *
from http.client import IncompleteRead
from bs4 import BeautifulSoup


class Parser:

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
        print("Getting online players on " + str(world))

        data = self.get_source_data(url)
        soup = BeautifulSoup(data, "html.parser")
        names = soup.find_all('div', class_='med-width-35')
        vocs = soup.find_all('div', class_='med-width-15')
        levels = soup.find_all('div', class_='med-width-25 med-text-right med-pr-40')

        players = list()
        for name, voc, level in zip(names, vocs, levels):
            players.append(Player(name.get_text(), voc.get_text(), level.get_text()))

        if players and len(players) > 2:
            del players[len(players) - 1]
            del players[0]

            for player in players:
                player.level = int(player.level)

            players.sort(reverse=True)
            online_players = list(players)
            return online_players

        else:
            online_players.clear()
            return online_players

    def get_player_details(self, name):
        url = 'http://medivia.online/community/online/' + str(world)
        print("Getting detailed info for " + str(name))

    def get_highscores(self, world, profession):
        highscores = list()
        highscore = {}
        skills = ['maglevel', 'fist', 'club', 'sword', 'axe', 'distance', 'shielding', 'fishing', 'mining']
        for skill in skills:
            url = 'https://medivia.online/highscores/' + world + '/' + profession + '/' + skill
            data = self.get_source_data(url)
            soup = BeautifulSoup(data, "html.parser")
            names = soup.find_all('div', class_='med-width-66')
            skill_values = soup.find_all('div', class_='med-width-35 med-text-right med-pr-40')
            print("Updating highscore: " + url)
            #highscore = {}
            highscore[skill] = {}
            for name, skill_value in zip(names, skill_values):
                highscore[skill][name.get_text()] = skill_value.get_text()
                #print(name.get_text() + skill_value.get_text())

           # highscores.append(highscore)
        print(highscore)
        return highscore






















