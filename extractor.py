from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time


class Match:
    def __init__(self, id, matchTime, homeTeam, score, guestTeam, location):
        self.id = id
        self.matchTime = matchTime
        self.homeTeam = homeTeam
        self.score = score
        self.guestTeam = guestTeam
        self.location = location

    def get_match_date(self):
        return self.matchTime[0:10]



def html_get():
    url = "http://www.volleylimburg.be/#/klvv/matches/2/3941"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(0.5)
    return driver.page_source


def html_to_match_objects(html_page):

    soup = BeautifulSoup(html_page, 'html.parser')

    match_data = soup.div(class_="sidebar-body-item ng-scope")

    string_list = []

    # get all table content
    for match in match_data[0].find_all('tr'):
        if match != "":
            string_list.append(match.text)

    data_list = string_to_list(string_list)

    return generate_objects(data_list)


def string_to_list(input_list):
    # from string to list without empty lines
    result = []
    for match_element in input_list:
        result.append(list(filter(None, match_element.splitlines())))
    print(result)
    return result


def generate_objects(input_data):
    """
    make an object for each match
    :param input_data: list of match lists
    :return: list of match objects
    """
    object_list = []
    for match_list in input_data:
        if len(match_list) == 5:
            object_list.append(Match(match_list[0], match_list[1], match_list[2], '', match_list[3], match_list[4]))
        else:
            object_list.append(
                Match(match_list[0], match_list[1], match_list[2], match_list[3], match_list[4], match_list[5]))
    return object_list


def get_next_weekend():
    """
    get the next start of the weekend
    """
    d = datetime.date.today()
    # day 5 for saturday
    t = datetime.timedelta((7 + 5 - d.weekday()) % 7)
    return (d + t).strftime('%d-%m-%Y')


def get_next_matches():

    next_weekend = get_next_weekend()
    for match in matches:
        date = match.get_match_date()
        d = datetime.datetime.strptime(date, '%d/%m/%Y')
        current = datetime.datetime.today()
        difference = (d - current).days
        if -2 < difference < 6:
            print(vars(match))

    return


content = html_get()

matches = html_to_match_objects(content)

get_next_matches()
