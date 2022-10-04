from turtle import update


class Player:
    def __init__(self, gamertag, rank, city):
        self.gamertag = gamertag
        self.rank = rank
        self.city = city

    def object(self):
        return {
            'tag': self.gamertag,
            'rank': self.rank,
            'city': self.city
        }

notable_players = [
    Player( 'Pancakes' , 'Top 5', 'Maracaibo').object(),
    Player( 'Angelini' , 'Top 5', 'Maracaibo').object(),
    Player('Tobio', 'Top 5', 'Maracaibo').object(),
    Player('Jerich', 'Top 5', 'Maracaibo').object(),
    Player('A-Crown', 'Top 5', 'Maracaibo').object(),
    Player('AndresAA', 'Top 5', 'Maracaibo').object(),
    Player('Cismu', 'Top 10', 'Maracaibo').object(),
    Player('Karin Benzema', 'Top 10', 'Maracaibo').object(),
    Player('Zeliox SwordCloud', 'Top 10', 'Maracaibo').object(),
    Player('LuichoX', 'Top 10', 'Maracaibo').object(),
    Player('Spade', 'Top 10', 'Maracaibo').object(),
    Player('Anriot', 'Top 15', 'Maracaibo').object(),
    Player('Vulpini', 'Top 15', 'Maracaibo').object(),
    Player('Lamotomami', 'Top 15', 'Maracaibo').object(),
    Player('Jean Papitas', 'Top 15', 'Maracaibo').object(),
    Player('Cax', 'Top 15', 'Maracaibo').object(),
    Player("Ale Hershey's", 'Top 20', 'Maracaibo').object(),
    Player("LuG", 'Top 20', 'Maracaibo').object(),
    Player("Isaac", 'Top 20', 'Maracaibo').object(),
    Player("Hidan", 'Top 20', 'Maracaibo').object(),
    Player("DIO", 'Top 20', 'Maracaibo').object(),
    Player('Tashi', 'Top 5', 'Ojeda').object(),
    Player('X-Pelox', 'Top 5', 'Ojeda').object(),
    Player('Hiro', 'Top 5', 'Cabimas').object(),
    Player('Janrok', 'Top 5', 'Ojeda').object(),
    Player('Trokermon', 'Top 5', 'Cabimas').object(),
    Player('Palo', 'Top 10', 'Ojeda').object(),
    Player('Kylar', 'Top 10', 'Cabimas').object(),
    Player('Kyros', 'Top 10', 'Cabimas').object(),
    Player('King Reaper', 'Top 10', 'Cabimas').object(),
    Player('Tongel', 'Top 10', 'Cabimas').object(),
    Player('Toxucroc', 'Top 15', 'Cabimas').object(),
    Player('Scarface', 'Top 15', 'Cabimas').object(),
    Player('Esaka!?', 'Top 15', 'Cabimas').object(),
    Player('Che', 'Top 15', 'Cabimas').object(),
    Player('Retsu', 'Top 15', 'Cabimas').object(),
    Player('Diowo', 'Top 20', 'Cabimas').object(),
    Player('Moon', 'Top 20', 'Cabimas').object(),
    Player('Queen', 'Top 20', 'Cabimas').object(),
    Player('Jacky', 'Top 20', 'Cabimas').object(),
    Player('Satoru', 'Top 20', 'Cabimas').object(),
]