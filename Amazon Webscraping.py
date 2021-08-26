import os
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from requests_html import HTMLSession
import requests
import smtplib
import time
import datetime
import csv
import pandas as pd


url = "https://www.amazon.com.au/s?k=data+science+books&ref=nb_sb_noss_1"

def get_data(url):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    page = requests.get(url,headers = headers)
    page_soup = BeautifulSoup(page.content, "html.parser")
    return page_soup

filename = 'Data_Science_Books.csv'
f = open(filename,'w')
headers = 'title, author, price, rating\n'
f.write(headers)

def get_items(page_soup):
    
    containers =page_soup.findAll('div',{'data-component-type':"s-search-result"})
        
    for container in containers:
        
        title = '"'+container.div.span.div.div.h2.a.span.text+'"'
        
        if len(container.findAll('div',{'class':'a-row a-size-base a-color-secondary'}))<1:
            author = ''
        else:
            author = '"'+container.findAll('div',{'class':'a-row a-size-base a-color-secondary'})[0].text+'"'
        
        try :
            price = container.div.div.div.findAll('div',{'class':"a-row a-size-base a-color-base"})[1].span.span.text[1:]
        except IndexError:
            price = ''
        except AttributeError:
            price = ''         
        if len(container.div.findAll('div',{'class':"a-row a-size-small"})) == 0:
            rating = ''
        else:
            rating = container.div.findAll('div',{'class':"a-row a-size-small"})[0].text[:3]
            
        f.write(title+','+ author+','+ price+','+ rating +'\n' )

page_soup = get_data(url)
get_items(page_soup)


def get_next_page(page_soup):
    
    page = page_soup.find('ul',{'class':'a-pagination'})
    if not page_soup.find('li',{'class':'a-disabled a-last'}):
        next_url = 'https://www.amazon.com.au/'+ str(page.find('li',{'class':'a-last'}).find('a')['href'])
        return next_url
    else:
        return ''

while get_next_page(page_soup) != '':
    
    page_soup = get_data(get_next_page(page_soup))
    
    get_items(page_soup)
    
f.close()
    