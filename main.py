from bs4 import BeautifulSoup

# Importing stuff to wait for the page to load the standings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Trying to load dynamic HTMl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Options for the web browsing
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

# Loading the page
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get('https://www.start.gg/tournament/panter-arena-2/event/ultimate-singles/standings')

delay = 10 # seconds

try:
    # Wait for the page to load the Dynamic Data
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

    # Parse data into HTML source code
    HTMLcontent = browser.page_source

    # Create soup to start scraping
    soup = BeautifulSoup(HTMLcontent, 'lxml')
    
    # Create a list with all the placings
    placings = soup.find_all('h3', class_='mui-thceyd-header20')

    # Create a list with all the gamertags
    tags = soup.find_all('span', class_='tss-16pvhoc-gamerTag')

    # Initiate an empty list to later fill it with the standings
    standings = []

    #Loop through the 'placings' and 'tags' lists and use the data to hydrate the 'standings' list
    for place, tag in zip(placings, tags):
        placing = place.text.strip()
        gamertag_ = tag.text.strip().split()
        gamertag = ' '.join(gamertag_)

        standings.append({'placing': placing, 'gamertag': gamertag})

    print(standings)
    # It fucking works I'm so happy

except TimeoutException:
    print ("Loading took too much time!")

# next_page = soup.find('button', { 'aria-label': "Go to next page" })

# test = soup.find('tbody')
# print(standings) 

# html_text = requests.get('https://www.start.gg/tournament/panter-arena-2/event/ultimate-singles/standings')

   

    
