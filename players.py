import os
from pprint import pprint

import bson
from dotenv import load_dotenv
import pymongo

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGO_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["smash_zulia"]

# Get a reference to the "movies" collection:
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
                'results': {'$push': {
                        'placing': '$placing', 
                        'tournament': '$tournament', 
                        'placing_score': '$placing_score', 
                        'wins_score': '$wins_score'
                    }
                }
            }
        }

gamertag = ''
stage_match_by_gamertag = {
    '$match': {
        'tag': gamertag
    }        
}

stage_sort_by_highest_placing = {
    '$sort': {
        'placing_score': pymongo.DESCENDING
    }
}

# --- Build pipeline ---
pipeline = [
        stage_unwind_standings,
        stage_project_results,
        stage_group_results_by_gamertag
    ]

player_pointer = tournament_collection.aggregate(pipeline)
players = []

for player in player_pointer:
    players.append(
        {
            'tag': player['_id'],
            'total_wins_score': player['total_wins_score'],
            'tournament_attendance': player['tournament_attendance'],
            'results': player['results']
        }
    )

print(len(players))
