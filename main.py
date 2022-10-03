from bs4 import BeautifulSoup
from pymongo import MongoClient
import math

# We use Selenium to load Dynamic HTMl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from notable_players import notable_players

MONGO_URI = 'mongodb+srv://pollo23:pollo23@cluster0.2odf0.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(MONGO_URI)

db = client['smash_zulia']


# Options for the web browsing
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

# Loading the page
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

tournament_url = 'https://www.start.gg/tournament/panter-arena-2/event/ultimate-singles/standings'
browser.get(tournament_url)

delay = 10 # seconds

try:
    # Wait for the page to load the Dynamic Data
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

    # Declare variables
    standings = [] # We fill this later with our data
    entrants_html = browser.find_element(By.CSS_SELECTOR, '.mui-1l4w6pd span.mui-x9rl7a-body1').get_attribute('innerHTML')
    pages = []
    tournament_title = browser.find_element(By.CSS_SELECTOR, 'title').get_attribute('innerHTML')

    # Find tournament title
    title_index = tournament_title.find('|')
    title = tournament_title[0:title_index].strip().replace(' ', '_')

    collection = db['tournaments']

    for i in entrants_html.split():
        if i.isdigit():
            pages.append(int(i))

    # Calculate amount of total pages
    entrants = pages[2]
    total_pages_float = entrants / 25
    total_pages = math.ceil(total_pages_float)

    # Calculate standings
    for i in range(total_pages):

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

        #Loop through the 'placings' and 'tags' lists and use the data to hydrate the 'standings' list
        for place, tag in zip(placings, tags):
            placing = place.text.strip()
            gamertag_ = tag.text.strip().split()
            gamertag = ' '.join(gamertag_)

            standings.append({'placing': placing, 'gamertag': gamertag})

        # Find the next page button
        next_button = browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')

        # Click the next page button
        browser.execute_script('arguments[0].click();', next_button)

    # collection.insert_many(standings)
    # print(f'The following list was added to the {title} collection: {standings}')

    # Calculate tournament dictionary to send it to the database
    tournament = {
        'name': title,
        # 'date': date,
        'entrants': entrants,
        'standings': standings
    }

    # Creating attendee list so I can search for notable players attending
    attendees = []

    for player in standings:
        attendees.append(player['gamertag'])
    
    # Calculating notable players from the tournament attendees
    top5 = []
    top10 = []
    top15 = []
    top20 = []

    for i in notable_players:
        for x in attendees:
            if i['tag'] == x:
                if i['rank'] == 'Top 5':
                    top5.append(x)
                elif i['rank'] == 'Top 10':
                    top10.append(x)
                elif i['rank'] == 'Top 15':
                    top15.append(x)
                elif i['rank'] == 'Top 20':
                    top20.append(x)

    print('NOTABLE PLAYERS')
    print(f'Top 5 ({len(top5)} players): {top5}')
    print(f'Top 10 ({len(top10)} players): {top10}')
    print(f'Top 15 ({len(top15)} players): {top15}')
    print(f'Top 20 ({len(top20)} players): {top20}')

    added_score_top5_players = len(top5) * 7
    added_score_top10_players = len(top5) * 5    
    added_score_top15_players = len(top5) * 3    
    added_score_top20_players = len(top5)   

    score = len(attendees) + added_score_top5_players + added_score_top10_players + added_score_top15_players + added_score_top20_players

    print(f'Tournament Score: {score}')

except TimeoutException:
    print ("Loading took too much time!")
