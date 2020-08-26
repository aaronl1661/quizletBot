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
from _thread import start_new_thread
from threading import Thread
from multiprocessing.pool import ThreadPool
import datetime

#Windows Version 1.0.0

#multi threading functions
def open_tab(url, driver):
    js_string = "window.open('" + urls + "'); "
    driver.execute_script(js_string)
    return True
results = []
def parse_tab(i ,driver):
    driver.switch_to.window(driver.window_handles[i])
    print('getting source')
    print(driver.window_handles[i])
    src = driver.page_source
    print('src recieved and now parsing')
    soup = BeautifulSoup(src, "lxml")
    print('parsing finished')
    flashcards = soup.findAll('span', {"class": "TermText notranslate lang-en" })
    print('found flashcards')
    result = []
    correct_flashcard = []
    for term, definition in zip(flashcards[::2], flashcards[1::2]):
        if fuzz.ratio(term.text, keyphrase) > 80:
            correct_flashcard.append(term.text)
            correct_flashcard.append(definition.text)
        elif fuzz.ratio(definition.text, keyphrase) > 80:
            correct_flashcard.append(definition.text)
            correct_flashcard.append(term.text)
        else:
            continue
    result.append(correct_flashcard)
    results.append(result)
    print(result)
    return result

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
    # options.add_argument('--headless')
    #options.add_argument('--disable_gpu')
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    results = []
    #parses through every url

    for i, urls in enumerate(URLS):
        # js_string = "window.open('" + urls + "'); "
        # driver.execute_script(js_string)
        # print("new tab")
        print(urls)
        start_new_thread(open_tab, (urls, driver))
        sleep(.1)
        # driver.switch_to.window(driver.window_handles[i])
        # sleep(1)
        # driver.execute_script("window.open('your url','_blank');")
        # driver.get(urls)
    threads = []
    for i in range(0, len(URLS)):
        print(datetime.time())
        process = Thread(target=parse_tab, args=[i ,driver])
        process.start()
        threads.append(process)

        # start_new_thread(parse_tab, (driver,))
    for process in threads:
        process.join()
    driver.close()
    
    os.system('cls')
    print('done')
    print(results)
    exit()
    # os.system('cls')
    # for result in results:
    #     if result != [[]]:
    #         print(result)
    #         print()

# https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/
# https://stackoverflow.com/questions/47543795/what-is-the-fastest-way-to-open-urls-in-new-tabs-via-selenium-python