#! python3

import bs4, requests, logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.disable(logging.CRITICAL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members

#get the top team given a url
def getTopTeam(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div > div:nth-of-type(1) > div:nth-of-type(4) > div > div.header > span.name.js-link')
    team = Team(elems[0].text, '')
    return team

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

    url = "https://www.hltv.org" + yearLink

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
month = ""

formattedYears = ', '.join(possibleYears)

yearMessage = "Enter a Year | ("+ formattedYears + "): "

userInput = True
while userInput:
     year = str(input(yearMessage))
     if(year not in possibleYears):
        print("Invalid Year")
     else:
        userInput = False

possibleMonths = getPossibleMonths(year)


formattedMonths = ', '.join(possibleMonths)
monthMessage = "Enter a Month | (" + formattedMonths + "): "

userInput = True

while userInput:
     try:   
         month = str(input(monthMessage))
         value = possibleMonths[month]
         userInput = False # this line only gets executed if key is valid, since otherwise an exception is thrown
     except:
         print("Invalid Month")

print("\nTop team of {} in {}: ".format(month, year))

team = getTopTeam(baseUrl + possibleMonths[month])
print(team.name)






