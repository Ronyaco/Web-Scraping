
#Importing libraries that will be used
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from requests_html import HTMLSession
import requests

# Defining the url, in this project will be targeting Amazon AU, searching "data science books"
url = "https://www.amazon.com.au/s?k=data+science+books&ref=nb_sb_noss_1"

# This function gets the data into page_soup variable
def get_data(url):

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    page = requests.get(url,headers = headers)
    page_soup = BeautifulSoup(page.content, "html.parser")
    return page_soup

#  Creating the csv file where the data will be written
filename = 'Data_Science_Books.csv'
f = open(filename,'w')
headers = 'title, author, price, rating\n'
f.write(headers)


# get_items take page_soup as parameter and identifies the books in the page using findAll 
# looping through each book found in the soup
# an writting in the csv that it is open 
def get_items(page_soup):
    
    containers =page_soup.findAll('div',{'data-component-type':"s-search-result"})
        
    for container in containers:
        
        # Book title
        title = '"'+container.div.span.div.div.h2.a.span.text+'"'
        

        # Adding a if, since there are some books that do not show the author
        if len(container.findAll('div',{'class':'a-row a-size-base a-color-secondary'}))<1:
            author = ''
        else:
            author = '"'+container.findAll('div',{'class':'a-row a-size-base a-color-secondary'})[0].text+'"'
        
        # There are some books that do not have price shown or have a different class
        # so we handle the two exceptions found.
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

        # Writing books found in the first page (soup)   
        f.write(title+','+ author+','+ price+','+ rating +'\n' )

# calling fuction get_items
page_soup = get_data(url)
get_items(page_soup)

# getting and building the link for the next page 
def get_next_page(page_soup):
    
    page = page_soup.find('ul',{'class':'a-pagination'})
    if not page_soup.find('li',{'class':'a-disabled a-last'}):
        next_url = 'https://www.amazon.com.au/'+ str(page.find('li',{'class':'a-last'}).find('a')['href'])
        return next_url
    else:
        return ''


# looping through the next page while there is one 
while get_next_page(page_soup) != '':
    
    page_soup = get_data(get_next_page(page_soup))
    
    get_items(page_soup)

#Closing the file

f.close()
    