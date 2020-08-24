from selenium import webdriver
from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fuzzywuzzy import fuzz
import os
from contextlib import suppress
import regex as re
from config import key, current_machine_id

if current_machine_id == key:
#with suppress(Exception):
    url_num = 5 #input("How many websites to search? Input a digit please. ")
    # while url_num.isdigit() is not True:
    #     url_num = input("Pick a digit not a word.")
    # url_num = int(url_num)
    #Searches for URLS
    URLS = []
    unfiltered = input("What's the question? ")
    keyphrase = "\"" + re.sub('[!,*)@#%(&$_?.^]"', '', unfiltered) + "\""
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
        print(url)
        terms=[]
        definitions = []
        result = []
        correct_flashcard = []
        print("web start load")
        driver.get(url)
        print("url gotten")
        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        location = None
        flashcards = soup.findAll('span', {"class": "TermText notranslate lang-en" })
        print("term start")
        for term, definition in zip(flashcards[::2], flashcards[1::2]):
            if fuzz.ratio(term.text, keyphrase) > 80:
                correct_flashcard.append(term.text)
                correct_flashcard.append(definition.text)
            elif fuzz.ratio(definition.text, keyphrase) > 80:
                correct_flashcard.append(definition.text)
                correct_flashcard.append(term.text)
            else:
                continue
        print("term end")
        result.append(correct_flashcard)
        #result.append(terms)
        #result.append(definitions)
        results.append(result)
        # for i, a in (0, enumerate():
        #     if fuzz.ratio(a.text, keyphrase) > 60:
        #         terms.append(a.text)
        #         location = i
        #     #add so that the definition can be flipped                
        #     if location is not None:
        #         if i == location + 1:
        #             definitions.append(a.text)
        #result.append(terms)


    driver.close()
    os.system('cls')
    for result in results:
        if result != [[]]:
            print(result)
            print()
