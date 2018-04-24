import requests
import re
from bs4 import BeautifulSoup
import pygsheets
import pandas as pd

def scrape():
    URL = ('https://gcc.cshape.net/GuestInfo.aspx')
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all('tr')
    event = []
    for row in table_rows:
        parsing = ''
        for item in row:
            derp = stripHtml(item)
            parsing = parsing + ' ' + str(derp)
        event.append(str.strip(parsing))
    del event[0:4]
    print(event)
    #authorization
    
    gc = pygsheets.authorize(service_file='/Users/user/import_key.json')
    
    #create empy dataframe
    df = pd.DataFrame()
    
    #create a column
    df['Ground Control Schedule'] = event
    
    #open the google spreadsheet where py to gsheet test is the name of my sheet)
    sh = gc.open('BJJ Schedule')
    
    wks = sh[0]
    
    wks.set_dataframe(df,(1,1))
    
def stripHtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', str(data))


scrape()
