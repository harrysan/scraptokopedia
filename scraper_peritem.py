# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 10:34:19 2019

@author: Harry
"""

import requests
import json
from bs4 import BeautifulSoup as bs
#import re
"""import csv
import urllib"""

imgsrc = []

class ScraperTokped:
    def __init__(self, URL):
        
        FULL_URL = "https://ace.tokopedia.com/search/product/v3?st=product&q={}&rows=15000&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product".format(URL)
        REQ = requests.Session()
        headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
        response = REQ.get(FULL_URL,headers=headers).content.decode("utf-8")
        data = json.loads(response)
        edges = data['data']["products"]
        
        #SOUP = BeautifulSoup(RESPONSE.content, 'html.parser')
        total_data = data['header']['total_data']
        waktu_proses = data['header']['process_time']
            
        print('Total Data with key '+URL+' is '+str(total_data))
        print('Process time '+str(waktu_proses))
        
        username = input('Paste username here :')
        
        produk = self.GET_PRODUCT(username,edges)
        if produk == False:
            produk('Product not found, try again..')
            return
        
     
    def GET_PRODUCT(self, username, edges):
        try:
            #jika dalam satu username memiliki barang dengan nama yang sama
            for edge in edges:
                if edge['shop']['name'] in username:
                    nama = edge['name']
                    harga = edge['price_int']
                    stok = edge['stock']
                    url = edge['url']
                    kategori = edge['category_breadcrumb']
                    departemen = edge['department_name']
                    
                    print(edge)
                    print('nama = '+nama)
                    print('harga = '+str(harga))
                    print('stok = '+str(stok))
                    print('url = '+url)
                    print('kategori = '+kategori)
                    print('departemen = '+departemen)
                    
                    self.GET_PRODUCT_DETAIL(edge['url'])
                    for i in range(0,len(imgsrc)):
                        print('gambar '+str(i)+' '+imgsrc[i])
            
            produk = 1
            return produk
        except:
            return False
        
    def GET_PRODUCT_DETAIL(self, urldet):
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
            hal = requests.get(urldet,headers=headers).content
            soup = bs(hal,"html.parser")
            
            #deskripsi
            deskripsi = soup.find("div", {'class': 'product-summary__content'}).get_text()
            print('deskripsi = '+deskripsi)
            
            gambar = soup.findAll("div", {'class': 'content-img-relative'})
            for div in gambar:
                imgsrc.append(div.find('img')['src'])
                #print(div.find('img')['src'])
            #get data detail single page product
            
            
        except:
            return False

#INISIALISASI INPUTAN (NAMA Barang)        
URL = input('Paste the name product here :')
ScraperTokped(URL)