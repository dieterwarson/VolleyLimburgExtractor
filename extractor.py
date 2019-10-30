from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import time

team_ids = ["/2/4209", "/2/4230", "/2/4230", "/2/4232", "/2/4250", "/2/4251", "/2/4253", "/2/4256", "/2/4256", "/2/4257", "/2/4199", "/2/4200", "/2/4201", "/2/4205", "/2/4271", "/2/4282", "/2/4290", "/2/4291", "/1/4019"]


class Match:
    def __init__(self, id, matchTime, homeTeam, score, guestTeam, location):
        self.id = id
        self.matchTime = matchTime[:16]
        self.homeTeam = homeTeam
        self.score = score
        self.guestTeam = guestTeam
        self.location = location

    def get_match_date(self):
        return self.matchTime[0:10]

    def print_match(self):
        print(self.matchTime + "    " + self.homeTeam + " - " + self.guestTeam + "      " + self.location)


def get_match(link):
    content = html_get(link)

    matches = html_to_match_objects(content)

    dvh_matches = get_next_matches(matches)

    for match_result in dvh_matches:
        match_result.print_match()


def html_get(link):
    url = "http://www.volleylimburg.be/#/klvv/matches" + link
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(0.5)
    return driver.page_source


def html_to_match_objects(html_page):

    soup = BeautifulSoup(html_page, 'html.parser')

    title_div = soup.div(class_="sidebar-body-title ng-binding")

    if title_div != "":
        title = title_div[0].text
        print(title)
    
    match_data = soup.div(class_="sidebar-body-item ng-scope")

    if match_data == 0:
        return

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


def get_next_matches(matches_list):
    next_matches = []
    next_weekend = get_next_weekend()
    for match in matches_list:
        date = match.get_match_date()
        d = datetime.datetime.strptime(date, '%d/%m/%Y')
        current = datetime.datetime.today()
        difference = (d - current).days
        if -2 < difference < 6:
            if filter_team(match):
                next_matches.append(match)

    return next_matches


def filter_team(match):
    filter_name = "dames volley hasselt"
    if match.homeTeam[0:len(filter_name)] == filter_name or match.guestTeam[0:len(filter_name)] == filter_name:
        return True
    return False


for team_id in team_ids:
    get_match(team_id)
