import requests as res 
import json 
from bs4 import BeautifulSoup
from src.Scrapper import Scrapper

def nextpage(id,next):
    url2 = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{next_cursor}%3D%3D%22%7D'
    url2 = url2.format(id=id,next_cursor=next)
    print(url2)

#userid = input("please enter target's id :")
#url = 'https://www.instagram.com/%s/?hl=zh-tw'%userid
url = 'https://www.instagram.com/yuivy0708/?hl=zh-tw'
retv = res.get(url)
soup = BeautifulSoup(retv.text,'html.parser')

img_js = str((soup.find_all('script',attrs={'type':'text/javascript'})[3]))
imgs = json.loads(img_js[img_js.find('{'):img_js.rfind('}')+1])

req_id = imgs['entry_data']['ProfilePage'][0]['graphql']['user']['id']
imgs = imgs['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']




if __name__ == '__main__':
    #userid = input("please enter targer's id: ")
    #base_url ='https://www.instagram.com/%s/?hl=zh-tw'%userid
    userid = 'yuivy0708'
    base_url = 'https://www.instagram.com/yuivy0708/?hl=zh-tw'

    scrap = Scrapper(userid,base_url)
    scrap.FirstPage()
    scrap.StartScrap()
    scrap.StartDownload(6)#use n threads 