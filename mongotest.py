from notable_players import notable_players
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from xpath_soup import xpath_soup


tournament = {'name': 'Panter_Arena_#2', 'date': 'Jul 24th, 2022', 'location': 'Av. Bella Vista, Maracaibo 4002, Zulia, Venezuela', 'entrants': 42, 'notable_players': {'total': 20, 'top 5': ['Pancakes', 'Angelini', 'Tobio', 'Jerich', 'AndresAA', 'Tashi', 'X-Pelox', 'Hiro'], 'top 10': ['Cismu', 'Zeliox SwordCloud', 'LuichoX', 'Spade'], 'top 15': ['Anriot', 'Jean Papitas', 'Cax', 'Toxucroc'], 'top 20': ["Ale Hershey's", 'Hidan', 'DIO', 'Diowo']}, 'score': 134, 'standings': [{'placing': '1', 'gamertag': 'Pancakes', 'score': 134, 'losses': ['', 'AndresAA']}, {'placing': '2', 'gamertag': 'X-Pelox', 'score': 122, 'losses': ['Pancakes', 'Pancakes']}, {'placing': '3', 'gamertag': 'Jerich', 'score': 110, 'losses': ['X-Pelox', 'Pancakes']}, {'placing': '4', 'gamertag': 'AndresAA', 'score': 98, 'losses': ['Jerich', 'Pancakes']}, {'placing': '5', 'gamertag': 'Tobio', 'score': 86, 'losses': ['X-Pelox', 'AndresAA']}, {'placing': '5', 'gamertag': 'Angelini', 'score': 86, 'losses': ['X-Pelox', 'Pancakes']}, {'placing': '7', 'gamertag': 'Zeliox SwordCloud', 'score': 74, 'losses': ['Jerich', 'Pancakes']}, {'placing': '7', 'gamertag': 'Spade', 'score': 74, 'losses': ['Angelini', 'Tobio']}, {'placing': '9', 'gamertag': 'Hidan', 'score': 62, 'losses': ['Jerich', 'Pancakes']}, {'placing': '9', 'gamertag': 'Cismu', 'score': 62, 'losses': ['Spade', 'Zeliox SwordCloud']}, {'placing': '9', 'gamertag': 'LuichoX', 'score': 62, 'losses': ['AndresAA', 'Tobio']}, {'placing': '9', 'gamertag': 'Hiro', 'score': 62, 'losses': ['Zeliox SwordCloud', 'Spade']}, {'placing': '13', 'gamertag': 'Toxucroc', 'score': 50, 'losses': ['Pancakes', 'LuichoX']}, {'placing': '13', 'gamertag': "Ale Hershey's", 'score': 50, 'losses': ['X-Pelox', 'Hidan']}, {'placing': '13', 'gamertag': 'Jean Papitas', 'score': 50, 'losses': ['Jerich', 'Hiro']}, {'placing': '13', 'gamertag': 'DIO', 'score': 50, 'losses': ['Toxucroc', 'Cismu']}, {'placing': '17', 'gamertag': 'Flye', 'score': 38, 'losses': ['Zeliox SwordCloud', "Ale Hershey's"]}, {'placing': '17', 'gamertag': 'Anriot', 'score': 38, 'losses': ['Tobio', 'Hidan']}, {'placing': '17', 'gamertag': 'Farre', 'score': 38, 'losses': ['Tobio', 'Jean Papitas']}, {'placing': '17', 'gamertag': 'Blate', 'score': 38, 'losses': ['Cismu', 'LuichoX']}, {'placing': '17', 'gamertag': 'Lum1', 'score': 38, 'losses': ["Ale Hershey's", 'Hiro']}, {'placing': '17', 'gamertag': 'Konami', 'score': 38, 'losses': ['Angelini', 'DIO']}, {'placing': '17', 'gamertag': 'Diowo', 'score': 38, 'losses': ['Angelini', 'Toxucroc']}, {'placing': '17', 'gamertag': 'Rookie355', 'score': 38, 'losses': ['AndresAA', 'Cismu']}, {'placing': '25', 'gamertag': 'Cax', 'score': 26, 'losses': ['Konami', 'Diowo']}, {'placing': '25', 'gamertag': 'Tino22', 'score': 26, 'losses': 
['Spade', 'Blate']}, {'placing': '25', 'gamertag': 'Danilopaz1', 'score': 26, 'losses': ['Hiro', 'Flye']}, {'placing': '25', 'gamertag': 'Valgarite', 'score': 26, 'losses': ['Jean Papitas', 'Hidan']}, {'placing': '25', 'gamertag': 'Difox', 'score': 26, 'losses': ['LuichoX', 
'Rookie355']}, {'placing': '25', 'gamertag': 'LIMIT', 'score': 26, 'losses': ['Pancakes', 'DIO']}, {'placing': '25', 'gamertag': 'Agui', 'score': 26, 'losses': ['Anriot', 'Farre']}, {'placing': '25', 'gamertag': 'apselito', 'score': 26, 'losses': ['X-Pelox', 'Lum1']}, {'placing': '33', 'gamertag': 'Tashi', 'score': 14, 'losses': ['Blate', 'Flye']}, {'placing': '33', 'gamertag': 'Bassprototype14', 'score': 14, 
'losses': ['apselito', 'Difox']}, {'placing': '33', 'gamertag': 'luisipop', 'score': 14, 'losses': ['LIMIT', 'Agui']}, {'placing': '33', 
'gamertag': 'Odinlv', 'score': 14, 'losses': ['Diowo', 'Valgarite']}, {'placing': '33', 'gamertag': 'Sly!', 'score': 14, 'losses': ['Danilopaz1', 'Tino22']}, {'placing': '33', 'gamertag': 'Shark', 'score': 14, 'losses': ['Hidan', 'Cax']}, {'placing': '33', 'gamertag': 'Luigio', 'score': 14, 'losses': ['Farre', 'DIO']}, {'placing': '33', 'gamertag': 'GyroZPP', 'score': 14, 'losses': ['Rookie355', 'Lum1']}, {'placing': '33', 'gamertag': 'Cachapa', 'score': 14, 'losses': ['Difox', 'apselito']}, {'placing': '33', 'gamertag': 'Jackson', 'score': 14, 'losses': ['Tino22', 'Danilopaz1']}]}

standings = tournament.get('standings')
attendees = ['Pancakes','X-Pelox','Jerich','Angelini','Tobio', 'Tashi']

# Options for the web browsing
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

# Loading the page
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

tournament_url = 'https://www.start.gg/tournament/panter-arena-2/event/ultimate-singles/standings?page=2'
browser.get(tournament_url)

delay = 10 # seconds

try:
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tss-16pvhoc-gamerTag')))
    pageHTML = browser.page_source
    soup = BeautifulSoup(pageHTML, 'lxml')

    # for i in range(total_pages)
    #     tags = []
    #     tags_indexes = []
    #     dqd_players = []

    #     tags_el = soup.find_all('span', class_='tss-16pvhoc-gamerTag')
    #     tr = soup.find('tr', class_="mui-1c8m30i")
        
    #     # 1. Find span element in the page for the notable players
    #     for i in notable_players:
    #         for x in tags_el:
    #             if i['tag'] == x.string:
    #                 tags_indexes.append(tags_el.index(x))

    #     # 2. Log all the elements's indexes in a list to look for them in the gamertag elements list
    #     for i in tags_indexes:
    #         tags.append(tags_el[i])

    #     # 3. Find the TR parent element of each gamertag's element, click it, and check if they were DQd
    #     for i in tags:
    #         for x in i.parents:
    #             if x.name == tr.name:
    #                 xpath = xpath_soup(x)
    #                 xtr = browser.find_element(By.XPATH, xpath)
    #                 browser.execute_script('arguments[0].click();', xtr)
    #                 john = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'scoreContainer-sggQ92-p')))
                    
    #                 titor = john.get_attribute('innerHTML')
    #                 if "DQ" in titor:
    #                     dqd_players.append(i.string)
    
    # print(dqd_players)
                
    # for i in notable_players:
    #     for x in tags:
    #         if i['tag'] == x:

    
        
except TimeoutException:
    print ("Loading took too much time!")