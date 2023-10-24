import requests
from bs4 import BeautifulSoup
import pandas as pd

url_target = "https://books.toscrape.com/"

def access_url(url): #READ dari CRUD
    r = requests.get(url)
    if r.status_code == 200:
        print("Web can be accessed")
    result = r.text
    return result

def save_html(html, filename): #Create dari CRUD
    with open(f"{filename}.html", "w") as f:
        f.writelines(html)

result = access_url(url=url_target)
save_html(result, "output")

soup = BeautifulSoup(result, 'html.parser') #ada dua parsing, yaitu lxml, dan html.parser
cards = soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
result = []
for card in cards:
    title = card.find("h3").find("a")["title"] #
    price = card.find("p", class_="price_color").get_text().replace("Â","")
    value_dict = {"title" : title, "price" : price}
    result.append(value_dict)

df = pd.DataFrame(result)
df.to_excel("output.xlsx", index=False)
print(df)

"""
<div class="page_inner">
    <div class="row">
        <div class="col-sm-8 h1"><a href="index.html">Books to Scrape</a><small> We love being scraped!</small></div>
    </div>
</div>
"""