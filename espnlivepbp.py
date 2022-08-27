import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

league=input('enter nfl or ncaaf: ')
week=input('which league week: ')
csv_file=league+week+'.csv'

if league == 'ncaaf':
    url='https://www.espn.com/college-football/scoreboard/_/group/80'
else:
    url='https://www.espn.com/nfl/scoreboard'

page= requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
regex=re.compile('DriveChart2D__PlayText')
regexdd=re.compile('DriveChart2D__DownAndDistance')

try:
    curplay=soup.find('p',{"class":regex}).text
except AttributeError:
    curplay=None

try:
    dd=soup.find('div',{"class":regexdd}).text
except AttributeError:
    dd=None

pd.set_option('display.max_colwidth', None)
df = pd.DataFrame({'Current Play':[curplay],'Down&Distance':[dd]})
print(df.to_csv(index=False,header=False))
while True:
    page= requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    curplays=[]
    dds=[]
    teams=[]
    scores=[]
    scoreset=[]
    for x in soup.find_all('p',{"class":regex}):
        curplays.append(x.text)
        curplays=[item.replace('Last Play: ',"") for item in curplays]
    for z in soup.find_all('div',{"class":regexdd}):
        dds.append(z.text)
    for j in soup.find_all('div',{"class":"DriveChart2D__Marker"}):
        if j.parent.text in teams:
            continue
        else:
            teams.append(j.parent.text)
    for sc in soup.find_all('div',{"class":"ScoreCell__Score h4 clr-gray-01 fw-heavy tar ScoreCell_Score--scoreboard pl2"}):
        scores.append(sc.text)
    for i in range(0,len(scores),2):
        scoreset.append(scores[i:i+2])
    for y in curplays:
        if y in df['Current Play'].unique():
            continue
        else:
            try:
                df2= pd.DataFrame({'Current Play':[y],'Down&Distance':[dds[curplays.index(y)]]})
            except IndexError:
                continue
            teams=[item.replace('205020',"") for item in teams]
            df2.insert(0,'Teams',[teams[curplays.index(y)]])
            df2.insert(1,'Score',[scoreset[curplays.index(y)]])
            df2.to_csv(csv_file,mode='a',index=False,header=False)
            print(df2.to_csv(index=False,header=False))
            df=pd.concat([df,df2],axis=0,ignore_index=True)
            time.sleep(10)
