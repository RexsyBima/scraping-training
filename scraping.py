import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import pandas as pd

#fitur parsing produk
def access_url(url): #READ dari CRUD
    r = requests.get(url)
    if r.status_code == 200:
        print("Web can be accessed")
    result = r.text
    return result


def save_html(html, filename): #Create dari CRUD
    with open(f"{filename}.html", "w") as f:
        f.writelines(html)


def parsing_individual_product(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    product = soup.find('div', class_="product_main")
    product_information = soup.find('table', class_="table table-striped").find_all('td')
    product_description = soup.find('article', class_='product_page').find_all('p')
    #print(product_description[-1].get_text())
    #print(type(product_information[0].get_text()))
    return {"title" : product.find("h1").get_text(), 
            "price" : product.find("p", class_="price_color").get_text().replace("Â", ""),
            "UPC" : product_information[0].get_text(),
            "Product Type" : product_information[1].get_text(),
            "description" : product_description[-1].get_text(),
            "stock" : product_information[-2].get_text().replace("In stock (", "").replace(" available)", ""),
            "review numbers" : product_information[-1].get_text()
            }

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

html_data = access_url(url)
result = parsing_individual_product(html_data)
#print(result)
print(result)
