import pandas as pd 
import csv
import selenium 
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
import csv
import datetime as datetime
import os
import re

########################################
# Helper methods
########################################

user = 'belle' # set user for your own computer
login = False
lengthOfScroll = 2
searchTerm = ['unschooling']

def startBrowser():
    options = webdriver.ChromeOptions()
    userdatadir = f'/Users/{user}/Library/Application Support/Google/Chrome/'
    profile = 'Profile 1'
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_argument(f"--profile-directory={profile}")
    browser = webdriver.Chrome(options=options)
    logging.info("Opening browser!")
    browser.get("https://www.instagram.com")
    if (login):
        time.sleep(100)
    else:
        time.sleep(30)
    return browser


def downloadPage(browser, filePath):
    try:
        with open(filePath, "w", encoding='utf-8') as f:
            f.write(browser.page_source)
    except:
        print("Could not download page!")

def readInstagram(intermediateFilePath, finalFilePath):
    with open(intermediateFilePath, 'r') as f:
        contents = f.read()
        soup = BS(contents, "html.parser")
        elements = soup.select('.x78zum5.xdt5ytf.x5yr21d.xa1mljc.xh8yej3.x1bs97v6.x1q0q8m5.xso031l.x11aubdm.xnc8uc2')
        
        
        links = []
        for el in elements:
            e = []
            l = el.find_all('a')
            count = 0
            for link in l:
                h = link['href']
                if re.match(r"^/p/.+?/$", h):  # Regex pattern to match "/p/anything/"
                    e.append(h)
                    break
                count += 1

            if count == len(link):
                e.append('no link')
            sponsored = [span.get_text() for span in el.find_all('span', class_='x1fhwpqd x132q4wb x5n08af')]
            if len(sponsored) > 0:
                e.append(sponsored[0])
            else:
                e.append('not sponsored')
            username = [span.get_text() for span in el.find_all('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')]
            if len(username) > 0:
                e.append(username[0])
            else:
                e.append('no username')

            time_contents = [time['datetime'] for time in el.find_all('time')]
            if len(time_contents) > 0:
                e.append(time_contents[0])
            else:
                e.append('no time')

            likes_comments = [span.get_text() for span in el.find_all('span', class_='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')]
            if len(likes_comments) > 1:
                e.append(likes_comments[0])
                e.append(likes_comments[1])
            elif len(likes_comments) > 0:
                e.append(likes_comments[0])
                e.append('no comments')
            else:
                e.append('no likes')
                e.append('no comments')

            links.append(e)
        print(links)
        
        max_columns = 6

        fileExists = os.path.isfile(finalFilePath)
        isEmpty = os.stat(finalFilePath).st_size == 0 if fileExists else True
        header = ['id', 'username', 'time', 'likes', 'comments', 'sponsored']
        with open(finalFilePath, "a") as file:
            writer = csv.writer(file)
            if isEmpty:
                writer.writerow(header)
            for item in links:
                # Pad the item to ensure it has exactly max_columns elements
                padded_item = item + [''] * (max_columns - len(item))
                writer.writerow(padded_item)




def getInstagram(browser):
    if not os.path.isdir('./intermediate'):
        os.mkdir('./intermediate')

    if not os.path.isdir('./data'):
        os.mkdir('./data')

    if not os.path.isdir('./screenshots'):
        os.mkdir('./screenshots')

    intermediateFilePath = f'./intermediate/{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.html'
    finalFilePath = f'./data/{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.csv'

    for i in range(0, lengthOfScroll):
        if (i != 0):
            ActionChains(browser)\
                .scroll_by_amount(0, 600)\
                .perform()
        time.sleep(5)
        browser.save_screenshot(f'./screenshots/{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.png')
        downloadPage(browser, intermediateFilePath)
        readInstagram(intermediateFilePath, finalFilePath)
    
    return finalFilePath

def getUniquePosts(infilePath, outfilePath):
    record = pd.read_csv(infilePath) 
    unique = record['id'].unique()
    header = ['id', 'username', 'time', 'likes', 'comments', 'sponsored']
    with open(outfilePath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for item in unique:
                writer.writerow(item)

########################################
# Run unschooling queries
########################################

browser = startBrowser()

if login == False:
    filePath = getInstagram(browser)

browser.quit()
