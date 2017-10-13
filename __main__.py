import requests
import time
import os
import urllib.request
from bs4 import BeautifulSoup
from lxml.html import fromstring
from multiprocessing import Pool
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def search_google(url):
    chrome = webdriver.Chrome('C:/Python27/Scripts/chromedriver.exe')
    chrome.get(url)
    time.sleep(1)
    element = chrome.find_element_by_css_selector("body")
    for i in range(30):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    chrome.find_element_by_id("smb").click()  # new page
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    time.sleep(1.5)
    source_code = chrome.page_source
    chrome.close()
    return source_code


def get_image(loc, link):
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    try:
        r = requests.get("https://www.google.com" + link, headers=headers)
    except:
        print("HTTP get error")
    title = str(fromstring(r.content).findtext(".//title"))
    link = title.split(" ")[-1]
    print("Downloading: " + link)
    try:
        filename = urllib.request.urlretrieve(link, loc + "/" + link.split("/")[-1])
    except:
        pass

########### Edit From Here ###########

# This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
search_keyword = ['stop', '40kph']

# to be added to each search keyword
keywords = ' sign road'

########### End of Editing ###########

# Download Image Links
i = 0
if __name__ == "__main__":
    while i < len(search_keyword):
        parent = "images/"
        search_keywords = search_keyword[i]
        search = search_keywords.replace(' ', '%20')
        pure_keyword = keywords.replace(' ', '%20')
        url = "https://www.google.com/search?as_st=y&tbm=isch&as_q=" + search + pure_keyword + \
              "&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:svga,itp:photo,ift:jpg"
        source = search_google(url)

        # Parse the page source and download pics
        soup = BeautifulSoup(str(source), "html.parser")

        # check directory and create if necessary
        loc = parent + search_keyword[i]
        if not os.path.isdir(loc):
            os.makedirs(loc)

        # get the links
        links = soup.find_all("a", class_="rg_l")
        links = [link.get("href") for link in links]

        with Pool(processes=4) as pool: # 4 threads
            func = partial(get_image, loc)
            pool.map(func, links)

        i = i + 1
