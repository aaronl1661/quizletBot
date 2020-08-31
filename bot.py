key = '4C4C4544-0058-4410-8054-B7C04F375631'
from selenium import webdriver
from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd
import requests
from fuzzywuzzy import fuzz
import os
from contextlib import suppress
import regex as re
# from config import key, current_machine_id
from selenium.webdriver.common.keys import Keys
from time import sleep
from _thread import start_new_thread
from threading import Thread
from multiprocessing.pool import ThreadPool
import datetime
from selenium.webdriver.firefox.options import Options
import math
import subprocess
#Windows Version 1.0.0

#Global Variables
total_results = []
results = []
current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
#multi threading functions
def open_tab(url, driver):
    # js_string = "window.open('" + url + "'); "
    # driver.execute_script(js_string)

    return True

def parse_tab(results, driver, keyphrase):
    src = driver.page_source
    # print('src', src)
    soup = BeautifulSoup(src, "lxml")
    # print('soup', soup)
    flashcards = soup.findAll('span', {"class": "TermText notranslate lang-en" })
    # print("flashcards")
    # print(flashcards)
    # print(driver.current_url)
    result = []
    correct_flashcard = []
    for term, definition in zip(flashcards[::2], flashcards[1::2]):
        if fuzz.token_sort_ratio(term.text, keyphrase) > 85:
            correct_flashcard.append(term.text)
            correct_flashcard.append(definition.text)
        elif fuzz.token_sort_ratio(definition.text, keyphrase) > 85:
            correct_flashcard.append(definition.text)
            correct_flashcard.append(term.text)
        else:
            continue
    result.append(correct_flashcard)
    results.append(result)
    return True
def question_answer(i, unfiltered):
    results = [i + 1]
    url_num = 5 #input("How many websites to search? Input a digit please. ")
    # while url_num.isdigit() is not True:
    #     url_num = input("Pick a digit not a word.")
    # url_num = int(url_num)
    #Searches for URLS
    URLS = []

    keyphrase = "\"" + re.sub('[!,*)@#%(&$_?.^]"', '', unfiltered) + "\""
    query = keyphrase + "\"quizlet\""
    for url in search(query, tld='com', lang='en', num=10, start=0, stop=url_num, pause=2.0):
        URLS.append(url)

    
    #initializes the webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('ignore-certificate-errors-spki-list')
    # options.add_argument('ignore-ssl-errors')
    # # options.add_argument("--headless")
    # #options.add_argument('--disable_gpu')
    # driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    # driver.add_cookie({"name": "app_session_id", "value": "adc19a7b-7506-4364-a4a8-733906d6602e"})
    #parses through every url
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    # tab_threads = []
    for i, urls in enumerate(URLS):
        # js_string = "window.open('" + urls + "'); "
        # driver.execute_script(js_string)
        # print("new tab")
            # process = Thread(target=open_tab, args=[urls,driver])
            # # start_new_thread(open_tab, (urls, driver))
            # process.start()
            # tab_threads.append(process)
            # sleep(.1)
        driver.switch_to.window(driver.window_handles[i])
        driver.get(urls)
        driver.execute_script("window.open(''); ")

        # driver.switch_to.window(driver.window_handles[i])
        # sleep(1)
        # driver.execute_script("window.open('your url','_blank');")
        # driver.get(urls)
    # for process in tab_threads:
    #     process.join()
    print("tabs open")
    # sleep(3)
    threads = []
    for i in range(0, len(URLS)):
        # print('loop entered')
        driver.switch_to.window(driver.window_handles[i])
        process = Thread(target=parse_tab, args=[results, driver, keyphrase])
        # print('thread created')
        process.start()
        # print('thread started')
        threads.append(process)

        # start_new_thread(parse_tab, (driver,))
    for process in threads:
        process.join()
    driver.quit()
    total_results.append(results)
    return True

#START OF MAIN 

if current_machine_id == key :
#with suppress(Exception):
    number_of_questions = input("How many questions? ")
    while number_of_questions.isdigit() is not True:
        if type(number_of_questions) is int:
            break
        number_of_questions = input("Pick a digit not a word.")
    number_of_questions = int(number_of_questions)
    
    threads = []
    all_questions = [[]]
    for i in range(0, int(number_of_questions / 5)):
        all_questions.append([])


    for i in range(0 , math.ceil(number_of_questions / 5)):

        for j in range(0, 5):
            if i*5 + j +1 > number_of_questions:
                break
            unfiltered = input("What's the question? ")
            all_questions[i].append(unfiltered)

    # initializes the webdriver
    # options = webdriver.ChromeOptions()
    # options.add_argument('ignore-certificate-errors-spki-list')
    # options.add_argument('ignore-ssl-errors')
    # # options.add_argument("--headless")
    # #options.add_argument('--disable_gpu')
    # driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    for i, questions in enumerate(all_questions):
        for j, question in enumerate(questions) :
            process = Thread(target=question_answer, args=[i*5 +j , question])
            process.start()
            threads.append(process)
        for process in threads:
            process.join()

    # os.system('cls')
    # temp_result = []
    # for i in range(0, len(total_results)):
    #     for j in range(0, len(total_results)):
    #         if total_results[i][0] == i + 1:
    #             print("entered")
    #             temp_result.append(total_results[i])
    #             break
    # print(temp_result)
    print("DONE!")
    f = open("answers.txt", "a+")
    print("\n", file=f)
    for results in total_results:
        for result in results:
            if result != [[]]:
                print(result, file=f)
    f.close()
    os.system('answers.txt')
    exit()
else:
    print("You thought you could copy the file and get away with it?")
# https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/
# https://stackoverflow.com/questions/47543795/what-is-the-fastest-way-to-open-urls-in-new-tabs-via-selenium-python
