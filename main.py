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
import re

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
    tournament_date = browser.find_element(By.CSS_SELECTOR, 'div.sgg1f4az span.mui-1623fqp-body1').get_attribute('innerHTML')
    tournament_location = browser.find_element(By.CSS_SELECTOR, 'div.location-sgg8uCc9 span').get_attribute('innerHTML')

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

    # Upsets list to calculate notable wins
    upsets = []

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

        # Create a list with all the players in the 'Lost To:' column
        lost_to = soup.find_all(href=re.compile('entrant'), attrs={'class': "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover primary-sggda-XD root-sggMrwNO mui-9idtjk"})

        # Loop through the 'placings' and 'tags' lists and use the data to hydrate the 'standings' list
        for place, tag in zip(placings, tags):
            placing = place.text.strip()
            gamertag_ = tag.text.strip().split()
            gamertag = ' '.join(gamertag_)

            standings.append({'placing': placing, 'gamertag': gamertag})

        # Get upsets
        for loss in lost_to:
            loss_txt = loss.get_text()
            loss_index = loss_txt.find('|')
            upsets.append(loss_txt[loss_index+1:len(loss_txt)+1].strip())

        # Find the next page button
        next_button = browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')

        # Click the next page button
        browser.execute_script('arguments[0].click();', next_button)

    # collection.insert_many(standings)
    # print(f'The following list was added to the {title} collection: {standings}')

    # Fetch all the attendees and all the placings from the 'Standings' list
    attendees = []
    list_of_placings = []

    for player in standings:
        attendees.append(player['gamertag'])
        list_of_placings.append(player['placing'])
    
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

    added_score_top5_players = len(top5) * 7
    added_score_top10_players = len(top10) * 5    
    added_score_top15_players = len(top15) * 3    
    added_score_top20_players = len(top20)   
    notable_attendees = top5 + top10 + top15 + top20

    score = len(attendees) + added_score_top5_players + added_score_top10_players + added_score_top15_players + added_score_top20_players

    # ADD SCORE FIELD TO TOURNAMENT STANDINGS

    # 1. Remove duplicates from list
    list_of_unique_placings = [i for n, i in enumerate(list_of_placings) if i not in list_of_placings[:n]] 
    amount_of_placings = len(list_of_unique_placings)
    minimum_placing_score = round(score / amount_of_placings)

    # 2. Calculate each placing's score
    unique_placings_score = {}

    for n, i in enumerate(list_of_unique_placings):
        unique_placings_score.update({ i: score - minimum_placing_score * n })

    # 3. Update standings with proper score and notable wins
    for i in standings:
        sech = unique_placings_score.get(i['placing'])
        i.update({'score': sech})

    # Adding upsets
    upsets.insert(0, '')

    for n, i in enumerate(standings):
        i.update({'lost_to': [upsets[n], upsets[n+1]]})

    # Calculate tournament dictionary to send it to the database
    tournament = {
        'name': title,
        'date': tournament_date.strip(),
        'location': tournament_location.strip(),
        'entrants': entrants,
        'notable_players': {
            'total': len(notable_attendees),
            'top 5': top5,
            'top 10': top10,
            'top 15': top15,
            'top 20': top20
        },
        'score': score,
        'standings': standings
    }

    print(standings)

except TimeoutException:
    print ("Loading took too much time!")
