from selenium import webdriver
from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fuzzywuzzy import fuzz
import os
from contextlib import suppress
import regex as re

#with suppress(Exception):
url_num = 10 #input("How many websites to search? Input a digit please. ")
# while url_num.isdigit() is not True:
#     url_num = input("Pick a digit not a word.")
# url_num = int(url_num)
#Searches for URLS
URLS = []
unfiltered = input("What's the question? ")
keyphrase = "\"" + re.sub('[!,*)@#%(&$_?.^]', '', unfiltered) + "\""
print(keyphrase)
query = keyphrase + "\"quizlet\""
for results in search(query, tld='com', lang='en', num=10, start=0, stop=url_num, pause=2.0):
    URLS.append(results)

#initializes the webdriver
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors-spki-list')
options.add_argument('ignore-ssl-errors')
options.add_argument('headless')
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
results = []
#parses through every url
for i,url in enumerate(URLS):
    terms=[]
    definitions = []
    result = []
    driver.get(url)
    src = driver.page_source

    soup = BeautifulSoup(src, "html.parser")

    location = None

    for i, a in enumerate(soup.findAll('span', {"class": "TermText notranslate lang-en" })):
        if fuzz.ratio(a.text, keyphrase) > 60:
            terms.append(a.text)
            location = i
        #add so that the definition can be flipped                
        if location is not None:
            if i == location + 1:
                definitions.append(a.text)
    result.append(terms)
    result.append(definitions)
    results.append(result)

driver.close()
os.system('cls')
for result in results:
    if result != [[],[]]:
        print(result)


#https://repl.it/@DevinShende/Quizlet-Scraper#main.py