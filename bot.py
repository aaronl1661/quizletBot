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
from selenium.webdriver.common.keys import Keys
from time import sleep
from multiprocessing import Process

#Windows Version 1.0.0





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
    #options.add_argument('headless')
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    results = []
    #parses through every url
    print(len(URLS))
    for i, urls in enumerate(URLS):
        js_string = "window.open('" + urls + "'); "
        driver.execute_script(js_string)
        print("new tab")
        # driver.switch_to.window(driver.window_handles[i])
        sleep(1)
        # driver.execute_script("window.open('your url','_blank');")
        # driver.get(urls)
    for i, urls in enumerate(URLS):
        driver.switch_to.window(driver.window_handles[i])    
        print(i)
        terms=[]
        definitions = []
        result = []
        correct_flashcard = []
        print("web start load")
        print("url gotten")
        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        flashcards = soup.findAll('span', {"class": "TermText notranslate lang-en" })
        print("term start")

#can multi thread this for loop to be faster
        
    # for i in enumerate(URLS):
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




    driver.close()
    os.system('cls')
    for result in results:
        if result != [[]]:
            print(result)
            print()

# https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/
# https://stackoverflow.com/questions/47543795/what-is-the-fastest-way-to-open-urls-in-new-tabs-via-selenium-python