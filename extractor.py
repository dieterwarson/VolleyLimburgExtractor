from bs4 import BeautifulSoup
from selenium import webdriver
import time


class Match:
    def __init__(self, id, matchTime, homeTeam, score, guestTeam, location):
        self.id = id
        self.matchTime = matchTime
        self.homeTeam = homeTeam
        self.score = score
        self.guestTeam = guestTeam
        self.location = location


url = "http://www.volleylimburg.be/#/klvv/matches/2/3941"

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
time.sleep(0.5)
content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

match_data = soup.div(class_="sidebar-body-item ng-scope")

string_list = []

# get all table content
for match in match_data[0].find_all('tr'):
    if match != "":
        string_list.append(match.text)

data_list = []

# from string to list without empty lines
for match_element in string_list:
    data_list.append(list(filter(None, match_element.splitlines())))

object_list = []

# make an object for each match
for match_list in data_list:
    if len(match_list) == 5:
        object_list.append(Match(match_list[0], match_list[1], match_list[2], '', match_list[3], match_list[4]))
    else:
        object_list.append(Match(match_list[0], match_list[1], match_list[2], match_list[3], match_list[4], match_list[5]))

