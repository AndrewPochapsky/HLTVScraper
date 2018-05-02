#! python3

import bs4, requests, logging, os
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

#logging.disable(logging.CRITICAL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

class Team:
    def __init__(self, name, points):
        self.name = name
        self.points = points

#get the top team given a url
def getTopTeams(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

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
        if child.text.strip() == year:
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

#Returns list of formatted results: 'X. Name (points)'
def getFormattedResults(teams):
    results = []
    for i in range(1, len(teams) + 1):
        results.append(str(i) + '. ' + teams[i -1].name + ' ' + teams[i -1].points)
        if i == 10:
            results.append('-' * 30)
            
    return results

baseUrl = "https://www.hltv.org" 

possibleYears = ['2018', '2017', '2016', '2015'] # TODO: consider getting the years dynamically from HLTV

year = ''
month = ''
maxRank = -1 # TODO: implement max ranks
saveToFile = None # bool

formattedYears = '(' + ', '.join(possibleYears) + '): '

yearMessage = "Enter a Year | "+ formattedYears

while True:
     year = str(input(yearMessage))
     if year not in possibleYears:
        print("Invalid Year")
     else:
        break

possibleMonths = getPossibleMonths(year)

formattedMonths = '(' + ', '.join(possibleMonths)+ '): '
monthMessage = "Enter a Month | " + formattedMonths

while True:
     try:   
         month = str(input(monthMessage))
         value = possibleMonths[month]
         break # this line only gets executed if key is valid, since otherwise an exception is thrown
     except:
         print("Invalid Month")
         
response = ''
while True:
    response = str(input("Save to file(y/n): "))
    logging.debug('response: ' + response)
    if response != 'y' and response != 'n':
        print("Invalid response")
    else:
        break
saveToFile = (response == 'y') # if response is 'y' then save to file

teams = getTopTeams(baseUrl + possibleMonths[month])
results = getFormattedResults(teams)

if not saveToFile:
    print("\nTop Ranked Teams of {} in {} are: ".format(month, year))
    for item in results:
        print(item)
        
else: 
    # Change the working directory to where the script is located
    abspath = os.path.abspath(__file__) 
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    directory = 'output\\'
    fileName = '{}-{}'.format(month, year) + '.txt'

    if not os.path.exists(directory):
        os.mkdir(directory)

    txtFile = open(directory + fileName, 'w')

    for item in results:
        txtFile.write(item + '\n')
 
    txtFile.close()
    print('Data saved to ' + os.path.abspath(directory + fileName))




