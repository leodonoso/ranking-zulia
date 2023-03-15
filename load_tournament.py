# Libraries imported: Beautiful Soup, Selenium Webdriver, pymongo, math, re, dotenv, os, xpath_soup function, notable_players list.
from datetime import datetime
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
import tabulate
from bson.objectid import ObjectId


load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client['smash_zulia']
collection = db['tournaments']

# Options for the web browsing
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

# Loading the page
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

tournament_url = 'https://www.start.gg/tournament/neo-lucina-s-coliseum-10/event/super-smash-bros-ultimate-singles/standings'
browser.get(tournament_url)

delay = 15 # seconds

try:
    # Wait for the page to load the Dynamic Data
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

    # Declare variables
    standings = [] # We fill this later with our data
    entrants_html = browser.find_element(By.CSS_SELECTOR, '.mui-1l4w6pd span.mui-x9rl7a-body1').get_attribute('innerHTML')
    pages = []
    title = browser.find_element(By.CSS_SELECTOR, 'div.name-sggF8StQ').get_attribute('innerHTML')
    tournament_date = browser.find_element(By.CSS_SELECTOR, 'div.sgg1f4az span.mui-1623fqp-body1').get_attribute('innerHTML')
    tournament_location = browser.find_element(By.CSS_SELECTOR, 'div.location-sgg8uCc9 span').get_attribute('innerHTML')

    for i in entrants_html.split():
        if i.isdigit():
            pages.append(int(i))

    # Calculate amount of total pages
    entrants = pages[2]
    total_pages_float = entrants / 25
    total_pages = math.ceil(total_pages_float)

    # Upsets list to calculate notable wins
    upsets = []

    # --- Calculate standings ---
    for i in range(total_pages):

        # Wait for the page to load the Dynamic Data
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

        # Parse webdriver into HTML source code
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

    # --- Fetch all the attendees and all the placings from the 'Standings' list ---
    attendees = []
    list_of_placings = []

    for player in standings:
        attendees.append(player['gamertag'])
        list_of_placings.append(player['placing'])
    
    # --- Adding upsets to standings array ---
    if (len(attendees) * 2) - 1 == len(upsets):
        upsets.insert(0, '')
    
    if (len(attendees) * 2) - 2 == len(upsets):
        upsets.insert(0, '')
        upsets.insert(0, '')

    i = 0

    for x in standings:
        x.update({'losses': [upsets[i], upsets[i+1]]})
        i+=2  

    # --- Calculate notable players from the tournament attendees ---
    notable_attendees = []

    for i in notable_players:
        for x in attendees:
            if i['tag'] == x:
                if i['rank'] == 'Top 5':
                    z = {'tag': x, 'rank': 'Top 5'}
                    notable_attendees.append(z)
                elif i['rank'] == 'Top 10':
                    z = {'tag': x, 'rank': 'Top 10'}
                    notable_attendees.append(z)
                elif i['rank'] == 'Top 15':
                    z = {'tag': x, 'rank': 'Top 15'}
                    notable_attendees.append(z)
                elif i['rank'] == 'Top 20':
                    z = {'tag': x, 'rank': 'Top 20'}
                    notable_attendees.append(z)        

    # --- Check for DQd players and remove them from the notable_attendees list ---
    dq_players_el = []
    tags_indexes = []
    dq_players = []

    for i in range(total_pages):
        # Wait for the page to load the Dynamic Data
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))

        # Parse webdriver into HTML source code and create soup
        HTMLcontent = browser.page_source
        soup = BeautifulSoup(HTMLcontent, 'lxml')

        # Create a list with all the gamertags
        tags = soup.find_all('span', class_='tss-16pvhoc-gamerTag')

        # Find 'tr' for later
        tr = soup.find('tr', class_="mui-1c8m30i")

        # 3. Find the tr parent element of each span element, click it, and check if the player was DQd
        for i in tags:
            for x in i.parents:
                if x.name == tr.name: # If the parent is a 'tr' element...
                    # Log the xpath of the parent element so we can click it using selenium
                    xpath = xpath_soup(x)
                    xtr = browser.find_element(By.XPATH, xpath)

                    # Click the tr to check for DQs
                    browser.execute_script('arguments[0].click();', xtr)
                    dq_element = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'scoreContainer-sggQ92-p')))
                    
                    dq_string = dq_element.get_attribute('innerHTML')
                    if "DQ" in dq_string:
                        dq_players.append(i.string)
                    # Go back to standings
                    go_back_el = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[tabindex="-1"]')))

                    go_back_el.send_keys(Keys.ESCAPE)

                    WebDriverWait(browser, 2)

        # Find the previous page button
        prev_button = browser.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to previous page"]')
        # Click the previous page button
        browser.execute_script('arguments[0].click();', prev_button)
        
    # --- Remove DQd players from notable attendeees, standings list and attendee list ---
    for x in dq_players:
        for i in notable_attendees:
            if i['tag'] == x:
                notable_attendees.remove(i)
        
        for y in standings:
            if y['gamertag'] == x:
                standings.remove(y)
        
        attendees.remove(x)

    # --- Calculate 'score' field for tournament. ---    
    score = len(attendees)

    for x in notable_attendees:
        if x['rank'] == 'Top 5':
            score += 7
        elif x['rank'] == 'Top 10':
            score += 5
        elif x['rank'] == 'Top 15':
            score += 3
        elif x['rank'] == 'Top 20':
            score += 1

    # --- Calculate 'score' for each placing ---

    # 1. Remove duplicates from list of placings
    list_of_unique_placings = [i for n, i in enumerate(list_of_placings) if i not in list_of_placings[:n]] 
    amount_of_placings = len(list_of_unique_placings)
    minimum_placing_score = round(score / amount_of_placings)

    # 2. Calculate each placing's score
    unique_placings_score = {}

    for n, i in enumerate(list_of_unique_placings):
        unique_placings_score.update({ i: score - minimum_placing_score * n })

    # 3. Update standings with proper score
    for i in standings:
        sech = unique_placings_score.get(i['placing'])
        i.update({'placing_score': sech})

    # --- Calculate tournament wins, notable wins and wins_score ---
    for z in attendees:
        indexes = []
        tournament_wins = []

        for i in standings:
            # Find the values for the 'losses' key in every dictionary item in the standings list
            x = i.get('losses')

            #  If any of those values matches the current player tag (z), then log the index of it's item so I can
            # search it in the standings list later
            
            # If it matches twice, log the index twice
            if x[0] == z and x[1] == z:
                a = standings.index(i)
                indexes.append(a)
                indexes.append(a)

            elif x[0] == z or x[1] == z:
                a = standings.index(i)
                indexes.append(a)

        # Populate 'tournament_wins' list using the indexes we logged
        for i in indexes:
            tournament_wins.append(standings[i]['gamertag'])
        
        # Calculate notable wins
        notable_wins = []
        for i in tournament_wins:
            for x in notable_attendees:
                if i == x['tag']:
                    if x['rank'] == 'Top 5':
                        notable_wins.append({'gamertag': i, 'rank': x['rank'], 'score': 10})
                    if x['rank'] == 'Top 10':
                        notable_wins.append({'gamertag': i, 'rank': x['rank'], 'score': 6})
                    if x['rank'] == 'Top 15':
                        notable_wins.append({'gamertag': i, 'rank': x['rank'], 'score': 3})
                    if x['rank'] == 'Top 20':
                        notable_wins.append({'gamertag': i, 'rank': x['rank'], 'score': 2})

        # Calculate total score
        wins_score = 0
        for i in notable_wins:
            wins_score += i['score']

        # Find index of player in standings list and update it's data
        for i in standings:
            if z == i['gamertag']:
                i.update({'wins': tournament_wins})
                i.update({'notable_wins': notable_wins})
                i.update({'wins_score': wins_score})
        
        # Clear data for next attendee
        tournament_wins.clear
        notable_wins.clear
        wins_score = 0

    new_player_ids = []

    # --- Get player IDs for standings ---
    for x in standings:
        awiri = x.get('gamertag')
        sech = db['players'].count_documents({'alt_tags': awiri})

        if sech >= 1:
            sucutu = db['players'].find({'alt_tags': awiri})
            for sucu in sucutu:
                x.update({'player_id': sucu['_id']})
        else:
            x.update({'player_id': ObjectId()})

            new_player_ids.append({
                '_id': x['player_id'],
                'tag': awiri,
                'alt_tags': [awiri],
                'city': None
            })

    for x in standings:
        abliquitus = x.get('losses')
        ibitanga = x.get('wins')
        bosocamber = x.get('notable_wins')

        # Get player IDs in the losses array
        for n, i in enumerate(abliquitus):
            sech = db['players'].count_documents({'alt_tags': i})

            if sech >= 1:
                sucutu = db['players'].find({'alt_tags': i})
                for sucu in sucutu:
                    abliquitus[n] = sucu['_id']

        # Get player IDs in the wins and notable wins array
        for n, i in enumerate(ibitanga):
            sech = db['players'].count_documents({'alt_tags': i})

            if sech >= 1:
                sucutu = db['players'].find({'alt_tags': i})
                for sucu in sucutu:
                    ibitanga[n] = sucu['_id']
            else:
                for npi in new_player_ids:
                    if i == npi['tag']:
                        ibitanga[n] = npi['_id']
        
        for n, i in enumerate(bosocamber):
            sech = db['players'].count_documents({'alt_tags': i['gamertag']})

            if sech >= 1:
                sucutu = db['players'].find({'alt_tags': i['gamertag']})
                for sucu in sucutu:
                    i.update({'player_id': sucu['_id']})
            else:
                for npi in new_player_ids:
                    if i['gamertag'] == npi['tag']:
                        i.update({'player_id': npi['_id']})    

    # --- Get tournament city ---
    if 'Cabimas' in tournament_location:
        city = ObjectId('635848341c20664c84d148f6')
    else:
        city = ObjectId('6358480d1c20664c84d148f5')

    # --- Get tournament date ---
    tourneydate = tournament_date.strip()
    
    suki = tourneydate.split(' ')

    num = ''

    for sech in suki[1]:
        if sech.isdigit():
            num = num + sech

    suki[1] = num

    awatus = ' '.join(suki)

    date = datetime.strptime(awatus, '%b %d %Y')

    tournament_id = ObjectId()

    # --- Calculate tournament dictionary to send it to the database ---
    tournament = {
        '_id': tournament_id,
        'name': title,
        'date': date,
        'city': city,
        'entrants': len(attendees),
        'notable_players': {
            'total': len(notable_attendees),
            'players': notable_attendees,
        },
        'score': score
    }

    # --- Create Results and Matches list to send to the database.
    results  = []
    matches = []

    for x in standings:
        results.append({
            'tournament_id': tournament_id,
            'player_id': x['player_id'],
            'placing': x['placing'],
            'placing_score': x['placing_score'],
            'notable_wins': len(x['notable_wins']),
            'wins_score': x['wins_score']
        })

        for w in x['wins']:
            matches.append({
                'tournament_id': tournament_id,
                'winner_id': x['player_id'],
                'loser_id': w,
                'upset_score': 0
            })
        
        for nw in x['notable_wins']:
            for m in matches:
                if nw['player_id'] == m['loser_id']:
                    m.update({'upset_score': nw['score']})

    collection.insert_one(tournament)

    print(f'The {title} tournament was added to the Smash Zulia tournaments collection')
    
    db['results'].insert_many(results)

    print('Added new results')

    db['matches'].insert_many(matches)

    print('Added new matches')

    if len(new_player_ids) > 1:
        db['players'].insert_many(new_player_ids)
        print('Added new players')

except TimeoutException:
    print ("Loading took too much time!")
