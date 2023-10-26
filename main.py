import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import pandas as pd


def access_url(url): #READ dari CRUD
    r = requests.get(url)
    print(r.status_code)
    if r.status_code == 200:
        print("Web can be accessed")
    status_code = r.status_code
    result = r.text
    return result, status_code


def save_html(html, filename): #Create dari CRUD
    with open(f"{filename}.html", "w") as f:
        f.writelines(html)


def parsing(cards):
    result = []
    urls = []
    for card in cards:
        title = card.find("h3").find("a")["title"] #
        #href = card.find("h3").find("a")["href"]
        url_product = f"https://books.toscrape.com/catalogue/{card.find('h3').find('a')['href']}" #->https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
        urls.append(url_product)
        #price = card.find("p", class_="price_color").get_text() #.replace("Â","")
        #value_dict = {"title" : title, "price" : price, "href" : url_product}
        #result.append(value_dict)
    return urls #bentuknya list, kita bisa extend setiap list yg baru


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


if __name__ == "__main__":
    x = 50
    url_products = []
    final_result = []
    try:
        while True:
            url_target = f"https://books.toscrape.com/catalogue/page-{x}.html"
            html_data, status_code = access_url(url=url_target)
            if status_code == 404:
                break
            x = x+1
            print(url_target)
            soup = BeautifulSoup(html_data, 'html.parser') #ada dua parsing, yaitu lxml, dan html.parser
            cards = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
            result = parsing(cards)
            url_products.extend(result)
    except ConnectionError:
            print("website has been fully scrapped")
    print(url_products)
    for url_product in url_products:
        product, status_code = access_url(url_product)
        print(f"scraping : {url_product}")
        product_result = parsing_individual_product(product)
        final_result.append(product_result)
    
    df = pd.DataFrame(final_result)
    df.to_excel("output.xlsx", index=False)
    print(df)

"""
fixing description column
"""