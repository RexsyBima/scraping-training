import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import pandas as pd


def access_url(url): #READ dari CRUD
    r = requests.get(url)
    #print(r.status_code)
    if r.status_code == 200:
        print("Web can be accessed")
    result = r.text
    return result

#url = "https://books.toscrape.com/catalogue/page-51.html"
#result = access_url(url)

x=0
while True:
    print(x)
    x=x+1