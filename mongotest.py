# Libraries imported: Beautiful Soup, Selenium Webdriver, pymongo, math, re, dotenv, os, xpath_soup function, notable_players list.
from bs4 import BeautifulSoup
from pymongo import MongoClient
import math
from xpath_soup import xpath_soup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from notable_players import notable_players
from dotenv import load_dotenv
import os
import re

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client['smash_zulia']
collection = db['tournaments']

# Options for the web browsing
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

# Loading the page
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

tournament_url = 'https://www.start.gg/tournament/neo-lucina-s-coliseum-8/event/super-smash-bros-ultimate-singles/standings'
browser.get(tournament_url)

delay = 10 # seconds

try:
    # Wait for the page to load the Dynamic Data
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

    # Declare variables
    standings = [] # We fill this later with our data
    entrants_html = browser.find_element(By.CSS_SELECTOR, '.mui-1l4w6pd span.mui-x9rl7a-body1').get_attribute('innerHTML')
    pages = []
    tournament_title = browser.find_element(By.CSS_SELECTOR, 'div.name-sggF8StQ').get_attribute('innerHTML')

    print(tournament_title)
    
        
except TimeoutException:
    print ("Loading took too much time!")