from bs4 import BeautifulSoup

with open('assets/PanterArena2.html', 'r') as html_file:
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'lxml')

    placings = soup.find_all('h3', class_='mui-thceyd-header20')
    tags = soup.find_all('span', class_='tss-16pvhoc-gamerTag')
    standings = []

    for place, tag in zip(placings, tags):
        placing = place.text.strip()
        gamertag_ = tag.text.strip().split()
        gamertag = ' '.join(gamertag_)

        standings.append({'placing': placing, 'gamertag': gamertag})

    print(standings) 

   

    
