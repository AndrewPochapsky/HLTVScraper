#! python3

import bs4, requests, logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.disable(logging.CRITICAL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Team:
    def __init__(self, name, points):
        self.name = name
        self.points = points

#get the top team given a url
def getTopTeams(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #elems = soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div > div:nth-of-type(1) > div:nth-of-type(4) > div > div.header > span.name.js-link')
    #team = Team(elems[0].text, '', '')

    teams = []

    teamDivs = soup.find_all('div', {'class': 'ranked-team standard-box'}) # Get all ranked teams divs
    for teamDiv in teamDivs:
        name = teamDiv.find('span', {'class': 'name js-link'})
        points = teamDiv.find('span', {'class': 'points'})
        team = Team(name.text, points.text)
        teams.append(team)
    
    return teams

#Get all of the possible months given a year
def getPossibleMonths(year):
    res = requests.get(baseUrl + '/ranking/teams/', headers = headers) # Go to the most recent rankings
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    divs = soup.find_all("div", {"class": "filter-column-content"}) # find all divs with this class
    yearsDiv = divs[0]  # select the first one as that is the one that holds the years

    yearLink = ''
    yearsDivChildren = yearsDiv.find_all('a') # get all of the children of that div
    for child in yearsDivChildren:
        if(child.text.strip() == year):
            yearLink = child['href']

    url = baseUrl + yearLink

    res = requests.get(url, headers = headers) # Go to the rankings of 'year'
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    divs = soup.find_all("div", {"class": "filter-column-content"}) # find all divs with this class
    monthsDiv = divs[1] # select the second one as that is the one that holds the months 
    
    monthsDivChildren = monthsDiv.find_all('a') # get all of the children of that div

    monthsDictionary = {} # key = month, value = href
    
    for a in monthsDivChildren:
        monthsDictionary[a.text.strip()] = a['href']

    return monthsDictionary

baseUrl = "https://www.hltv.org" 

possibleYears = ['2018', '2017', '2016', '2015']

year = ''
month = ''
maxRank = -1

formattedYears = '(' + ', '.join(possibleYears) + '): '

yearMessage = "Enter a Year | "+ formattedYears

while True:
     year = str(input(yearMessage))
     if(year not in possibleYears):
        print("Invalid Year")
     else:
        break#userInput = False

possibleMonths = getPossibleMonths(year)

formattedMonths = '(' + ', '.join(possibleMonths)+ '): '
monthMessage = "Enter a Month | " + formattedMonths

userInput = True

while True:
     try:   
         month = str(input(monthMessage))
         value = possibleMonths[month]
         break # this line only gets executed if key is valid, since otherwise an exception is thrown
     except:
         print("Invalid Month")

print("\nTop Ranked Teams of {} in {} are: ".format(month, year))

teams = getTopTeams(baseUrl + possibleMonths[month])

for i in range(1, len(teams) + 1):
    print(str(i) + '. ' + teams[i -1].name + ' ' + teams[i -1].points)
    if(i == 10):
        print('-' * 30)






