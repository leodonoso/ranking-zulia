import os
from pprint import pprint
import tabulate

import bson
from dotenv import load_dotenv
import pymongo

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGO_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "smash_zulia" database:
db = client["smash_zulia"]

# Get a reference to the "tournaments" collection:
tournament_collection = db["tournaments"]

# --- Define pipeline stages ---
stage_unwind_standings = {'$unwind': '$standings'}

stage_project_results = {
    '$project': {
        'tag': '$standings.gamertag', 
        'placing': '$standings.placing', 
        'tournament': '$name', 
        'placing_score': '$standings.placing_score', 
        'wins_score': '$standings.wins_score' 
    }
}

stage_group_results_by_gamertag = {
    '$group': {
        '_id': '$tag',
        'total_wins_score': {'$sum': { '$sum': '$wins_score'}},
        'tournament_attendance': {'$sum': 1},
        # 'results': {'$push': {
        #         'placing': '$placing', 
        #         'tournament': '$tournament', 
        #         'placing_score': '$placing_score', 
        #         'wins_score': '$wins_score'
        #     }
        # }
    }
}

# --- Build Pipelines ---
pipeline1 = [
    stage_unwind_standings,
    stage_project_results
]

results_pointer = tournament_collection.aggregate(pipeline1)

# --- Find results from two players ---
atucu = [['Tashi', 'LA CREATURA'], ['Karin Benzema', 'Revolver Cunaguaro'], ['anoel doble a', 'Jovani Vasquez']]

players = []

for names in atucu:
    pipeline2 = [
        {
            '$match': {
                'tag': {'$in': names}
            }
        },
        {
            '$set': {
                'tag': names[0]
            }
        },
        stage_group_results_by_gamertag
    ]

    pipeline1.extend(pipeline2)

    repeated_player_pointer = tournament_collection.aggregate(pipeline1)

    for rplayer in repeated_player_pointer:
        players.append({
            'tag': rplayer['_id'],
            'total_wins_score': rplayer['total_wins_score'],
            'tournament_attendance': rplayer['tournament_attendance'],
            # 'results': rplayer['results']
        })
    
    del pipeline1[2::]

# --- Total Placing Score ---

placings = []
for names in atucu:
    pipeline2 = [
        {
            '$match': {
                'tag': {'$in': names}
            }
        },
        {
            '$sort': {
                'placing_score': pymongo.DESCENDING
            }        
        },
        {
            '$limit': 5
        },  
        {
            '$set': {
                'tag': names[0]
            }
        },
        {
            '$group': {
                '_id': '$tag',
                'total_placing_score': {'$sum': { '$sum': ['$placing_score']}}
            }
        }
    ]

    pipeline1.extend(pipeline2)
    placings_pointer = tournament_collection.aggregate(pipeline1)
    for placing in placings_pointer:
        placings.append(placing)

    del pipeline1[2::]

# --- Add total placing score to each player ---
for player in players:
    for placing in placings:
        if player['tag'] == placing['_id']:
            player.update({'total_placing_score': placing['total_placing_score']})

# --- Calculate total score ---
for player in players:
    if player['tournament_attendance'] >= 5:
        total_score = round((player['total_placing_score'] / 5) + player['total_wins_score'], 2)
        player.update({'total_score': total_score})
    elif player['tournament_attendance'] == 4:
        total_score = round((player['total_placing_score'] / 4) + player['total_wins_score'], 2)
        player.update({'total_score': total_score})
    elif player['tournament_attendance'] <= 3:
        total_score = round((player['total_placing_score'] / 3) + player['total_wins_score'], 2)
        player.update({'total_score': total_score})

# Create table
header = players[0].keys()
rows = [x.values() for x in players]

# --- Delete repeated players from database ---
# for names in atucu:
#     db['players'].delete_many({ 'tag': {'$in': names}})

players_collection = db['players']
players_collection.insert_many(players)