#! python3

import bs4, requests, logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members

def getTopTeam(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div > div:nth-of-type(1) > div:nth-of-type(4) > div > div.header > span.name.js-link')
    team = Team(elems[0].text, '')
    return team

def getPossibleMonths(year):
    res = requests.get(baseUrl, headers = headers) # Go to the most recent rankings
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    divs = soup.find_all("div", {"class": "filter-column-content"}) # find all divs with this class
    monthsDiv = divs[1] # select the second one as that is the one that holds the months
    monthsDivChildren = monthsDiv.find_all('a') # get all of the children of that div

    monthsDictionary = {} # key = month, value = href
    
    for a in monthsDivChildren:
        monthsDictionary[a.text] = a['href']

    return monthsDictionary
    
#body > div.bgPadding > div > div.colCon > div.leftCol > div > div.sidebar-box > div.sidebar-first-level > div > div > div:nth-child(4) > a.sidebar-single-line-item.selected
#body > div.bgPadding > div > div.colCon > div.leftCol > div > div.sidebar-box > div.sidebar-first-level > div > div > div:nth-child(4) > a:nth-child(2)
#body > div.bgPadding > div > div.colCon > div.leftCol > div > div.sidebar-box > div.sidebar-first-level > div > div > div:nth-child(4) > a:nth-child(3)

#divTag = soup.find_all("div", {"class": "tablebox"}):

#for tag in divTag:
 #   tdTags = tag.find_all("td", {"class": "align-right"})
  #  for tag in tdTags:
   #     print tag.text

baseUrl = "https://www.hltv.org/ranking/teams" # brings you to the most reset rankings

urlWithInsertions = "https://www.hltv.org/ranking/teams/{}/{}/{}" # https://www.hltv.org/ranking/teams/YEAR/MONTH/DAY

possibleYears = [2018, 2017, 2016, 2015]

year = 0000
month = ""
day = 00
months = getPossibleMonths(2018)

for key in months:
    print(key + ": " + months[key])
    


#year = int(input("Year: "))

#month = str(input("Month: "))
#print("Year: {}, Month: {}".format(year, month))

