import requests as res 
import shutil
import threading
import numpy as np 
from bs4 import BeautifulSoup
from tqdm import tqdm 
from time import sleep
import os 
import json 


class Scrapper():
    def __init__(self,userid,base_url):
        self.userid = userid
        self.base_url = base_url
        self.img_urls = []
        self.id = None
        self.next_cursor = None
        self.next_url = None 
        self.next = False

        if not os.path.exists(self.userid):
            os.mkdir(self.userid)
        else:
            shutil.rmtree(self.userid)
            os.mkdir(self.userid)

    def UpdateNextUrl(self):
        url = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{next_cursor}%3D%3D%22%7D'
        self.next_url = url.format(id=self.id,next_cursor = self.next_cursor)
  
    def FirstPage(self):
        #instagram first page has 12 pictures 
        #and has next page's cursor 
        retv = res.get(self.base_url)
        soup = BeautifulSoup(retv.text,'html.parser')

        img_js = str((soup.find_all('script',attrs={'type':'text/javascript'})[3]))
        imgs = json.loads(img_js[img_js.find('{'):img_js.rfind('}')+1])

        self.id = imgs['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.next_cursor = imgs['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'][:-2]
        self.next = True
        imgs = imgs['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        
        for i in imgs:
            self.img_urls.append(i['node']['display_url'])
        
        self.UpdateNextUrl()
    def StartScrap(self):
        while self.next:
            retv = res.get(self.next_url)
            imgs = json.loads(str(retv.text))
            try:
                self.next_cursor = imgs['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'][:-2]
            except:
                print('final page')
                
            self.next = imgs['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

            imgs = imgs['data']['user']['edge_owner_to_timeline_media']['edges']
            for i in tqdm(imgs):
                self.img_urls.append(i['node']['display_url'])
            self.UpdateNextUrl()

    def download(self,img_list,index):
        for url in tqdm(img_list):
            response = res.get(url)
            with open(self.userid+'/'+str(index)+'.jpg', 'wb') as f:
                f.write(response.content)
            index+=1
            
    def StartDownload(self,thread_num):
        chunk_size = len(self.img_urls)//thread_num
        thread_list = []
        download_list = []
        for i in range(thread_num):
            temp = []
            if i == thread_num-1:
                temp = self.img_urls[i*chunk_size:]
            else:
                temp = self.img_urls[i*chunk_size:(i+1)*chunk_size]

            download_list.append(temp)
        
        for i in range(thread_num):
            t = threading.Thread(target=self.download,args=(download_list[i],i*chunk_size))
            thread_list.append(t)
            t.start()
        
        for i in thread_list:
            i.join()
        print('complete download')



