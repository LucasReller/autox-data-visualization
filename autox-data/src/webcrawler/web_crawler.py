import re
import sys

import requests
from bs4 import BeautifulSoup

from webcrawler.model_builder import ModelBuilder

class WebCrawler:
    # example 2018 or newer url
    # https://forum.mnautox.com/results/2018/doty.html
    doty_extension_2018_newer = "doty.html"

    # example 2017 or older url
    # https://forum.mnautox.com/results/mnautoxreports/reports/static/2017/2017_MAC_DOTY.htm
    doty_path_2017_older = "mnautoxreports/reports/static/"
    doty_extension_2017_older = "_MAC_DOTY.htm"

    base_url = "https://forum.mnautox.com/results/"

    def __init__(self, year):
        self.season_list = []
        self.driver_list = []
        self.competitor_list = []
        self.event_list = []
        self.event_count = 0
        self.soup = None

        if int(year) >= 2018:
            self.base_url += (str(year) + '/' + self.doty_extension_2018_newer)
            self.pre_2018 = False
        else:
            self.base_url += (self.doty_path_2017_older + str(year) + '/' + year + self.doty_extension_2017_older)
            self.pre_2018 = True

        self.year = year

    def read_html(self):
        try:
            response = requests.get(self.base_url, headers = {'User-Agent': 'My User Agent 1.0'})
            self.soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == requests.codes.ok:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("Error reading html from: {url}\nException: ", e)
            return False

    def get_season_event_count(self):
        table = self.soup.find('table', attrs={'class': 'results'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        #find event count
        cols = rows[0].find_all('th')
        for col in cols:
            if not re.search('M[0-9]+', col.text) is None: #if text is M# then it's an event column
                self.event_count += 1
        return self.event_count

    def build_competitor_from_soup(self):
        table = self.soup.find('table', attrs={'class': 'results'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        index = 0
        # |rank|name|total_events|scored_events|total_points|diff_to_prev|diff_to_first|avg_points|event_1|...|event_n|btp|
        for row in rows:
            competitor = []
            events = []

            cols = row.find_all('td')

            # TODO if competitior does not exist, do create competitior and events
            if len(cols) > 0:
                competitor.append(cols[0].text)
                competitor.append(cols[1].text)
                competitor.append(cols[4].text)
                competitor.append(cols[7].text)
                self.competitor_list.append(competitor)

                # TODO check which events already exist, only add new events
                start_index = 0 - self.event_count-1
                for event in cols[start_index:-1]:
                    events.append(event.text)
                self.event_list.append(events)
                index+=1
