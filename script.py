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


# 0.0 Initialize Webdrivers
# 1. Open 5 tabs at a time for each question
# 2. Parse through tabs at the same time

total_results = []
results = []
#multi threading functions
def open_tab(url, driver):
    js_string = "window.open('" + url + "'); "
    driver.execute_script(js_string)
    return True

def parse_tab(results, driver, keyphrase):

    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    flashcards = soup.findAll('span', {"class": "TermText notranslate lang-en" })
    result = []
    correct_flashcard = []
    for term, definition in zip(flashcards[::2], flashcards[1::2]):
        if fuzz.ratio(term.text, keyphrase) > 85:
            correct_flashcard.append(term.text)
            correct_flashcard.append(definition.text)
        elif fuzz.ratio(definition.text, keyphrase) > 85:
            correct_flashcard.append(definition.text)
            correct_flashcard.append(term.text)
        else:
            continue
    result.append(correct_flashcard)
    results.append(result)
    return True

#with suppress(Exception):
url_num = 5
TOTAL_URLS = []
number_of_questions = input("How many questions? ")
while number_of_questions.isdigit() is not True:
    if type(number_of_questions) is int:
        break
    number_of_questions = input("Pick a digit not a word.")
number_of_questions = int(number_of_questions)
all_questions = []

for i in range(0, number_of_questions):
    unfiltered = input("What's the question? ")
    keyphrase = "\"" + re.sub('[!,*)@#%(&$_?.^]"', '', unfiltered) + "\""
    all_questions.append(keyphrase)
    query = keyphrase + "\"quizlet\""
    URLS = []
    for url in search(query, tld='com', lang='en', num=url_num, start=0, stop=url_num, pause=2.0):
        URLS.append(url)
    TOTAL_URLS.append(URLS)
    # all_questions.append(unfiltered)

# print(TOTAL_URLS)

# initializes the webdriver
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors-spki-list')
options.add_argument('ignore-ssl-errors')
# options.add_argument("--headless")
#options.add_argument('--disable_gpu')
driver = webdriver.Chrome(executable_path="./chromedriver", options=options)

url_length = 0
tab_threads = []
for url in TOTAL_URLS:
    for links in url:
        process = Thread(target=open_tab, args=[links,driver])
        process.start()
        # start_new_thread(open_tab, (links, driver))
        tab_threads.append(process)
        url_length+=1

for process in tab_threads:
    process.join()

print("tabs open")

threads = []
driver.switch_to.window(driver.window_handles[0])
driver.execute_script("window.close();")


for i, url in enumerate(TOTAL_URLS):
    for j, links in enumerate(url):
        print("entered_loop")
        driver.switch_to.window(driver.window_handles[url_length - (j + (len(url) * i)) - 1])
        print(driver.current_url)
        process = Thread(target=parse_tab, args=[results, driver, all_questions[i]])
        threads.append(process)

for process in threads:
    process.start()

for process in threads:
    process.join()

driver.close()
total_results.append(results)


os.system('cls')
print('done !')
temp_result = []
# for i in range(0, len(total_results) - 1):
#     if total_results[i + 1][0] < total_results[i][0]:
#         temp_result.extend(total_results[i])
#         del(total_results[i])
#         total_results[i].extend(total_results[i + 1])
#         del(total_results[i +1])
#         total_results[i +1 ].extend(temp_result)
f = open("answers.txt", "w")
for results in total_results:
    for result in results:
        print(result, file=f)
f.close()
exit()