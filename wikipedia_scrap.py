import pandas as pd
import math
import requests
from bs4 import BeautifulSoup
import random
from pathlib import Path
import os
import uuid

def get_id():
    return str(uuid.uuid4())

def scrape_and_write(url,file_name):
    text = ''
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    div = soup.find('div',attrs={'id':'content'})
    f = open(file_name,'w',encoding='utf-16')
    p_tags = div.find_all('p')
    for p in p_tags:
        if(p.get_text().strip() != ''):
            sups = p.find_all('sup',attrs={'class':'reference'})
            text += ' '.join(p.get_text().strip().split())
            for sup in sups:
                text = text.replace(sup.get_text(),'')
            text += ' '
    f.write(text)
    f.close()
    nav = soup.find('nav',attrs={'id':'p-lang'})
    lis = nav.find_all('li')
    for li in lis:
        a = li.find('a')
        lang = a['lang']
        if lang == 'en':
            return a,True
    return None,False

def main():
    lang = 'hi'
    base_url = 'https://'+lang+'.wikipedia.org/wiki/'
    path = 'Scraped_Files'
    Path(path).mkdir(parents=True,exist_ok=True)
    page_df = pd.read_csv(lang+'wiki-20210201-all-titles.csv',sep = '\t')
    for title in page_df['page_title']:
        links_to_uuid = []
        url = base_url+title
        uuid = get_id()
        links_to_uuid.append([url,uuid])
        a,has_english = scrape_and_write(url,os.path.join(path,uuid+'-'+lang+'.txt'))
        if has_english:
            scrape_and_write(a['href'],os.path.join(path,uuid+'-en.txt'))
        df = pd.DataFrame(links_to_uuid)
        if(not os.path.exists('Links_to_UUID.csv')):
            df.to_csv('Links_to_UUID.csv',header=['URL','UUID'],index=False,mode='a')
        else:
            df.to_csv('Links_to_UUID.csv',header=False,index=False,mode='a')

    
if __name__ == '__main__':
    main()