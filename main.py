#! python3

import bs4, requests, logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}

def getTopTeam(url):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body > div.bgPadding > div > div.colCon > div.contentCol > div > div:nth-of-type(1) > div:nth-of-type(4) > div > div.header > span.name.js-link')
    return elems[0].text;


#https://www.hltv.org/ranking/teams/YEAR/MONTH/DAY



print(getTopTeam('https://www.hltv.org/ranking/teams/2018/april/23'))

#Ask user for year

#Ask user for month

#Check to see which days are available and then ask user to pick one of them

#Display info
