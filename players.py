import os
from pprint import pprint
import tabulate
import random

from bson.objectid import ObjectId
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
        '_id': 0,
        'player_id': '$standings.player_id',
        'tournament_id': '$_id',
        'tag': '$standings.gamertag', 
        'placing': '$standings.placing', 
        'tournament': '$name',
        'city': '$city', 
        'placing_score': '$standings.placing_score',
        'notable_wins': {'$size': '$standings.notable_wins'}, 
        'wins_score': '$standings.wins_score' 
    }
}

stage_group_results_by_gamertag = {
    '$group': {
        '_id': '$player_id',
        'tag': {'$first': '$tag'},
        'total_wins_score': {'$sum': { '$sum': '$wins_score'}},
        'tournament_attendance': {'$sum': 1},
        'results': {'$push': {
                'result_id': '$result_id', 
                'placing': '$placing',
                'tournament': '$tournament', 
                'placing_score': '$placing_score',
                'notable_wins': '$notable_wins', 
                'wins_score': '$wins_score'
            }
        }
    }
}

stage_sort_by_attendance = {
    '$sort': {
        'tournament_attendance': pymongo.DESCENDING
    }
}

stage_sort_by_wins_score = {
    '$sort': {
        'total_wins_score': pymongo.DESCENDING
    }
}

# gamertag = ''
# stage_match_by_alt_tags = {
#     '$match': {
#         'tag': {'$in': alt_tags}
#     }        
# }

stage_sort_by_highest_placing = {
    '$sort': {
        'placing_score': pymongo.DESCENDING
    }
}

# --- Build pipelines ---
pipeline1 = [
    stage_unwind_standings,
    stage_project_results,
    stage_group_results_by_gamertag,
    stage_sort_by_wins_score
]

pipeline2 = [
    stage_unwind_standings,
    stage_project_results
]

# # --- Create players list, group results by player and add winscore ---
# player_pointer = tournament_collection.aggregate(pipeline1)
# players = []

# for player in player_pointer:
#     players.append(
#         {
#             'tag': player['_id'],
#             'total_wins_score': player['total_wins_score'],
#             'tournament_attendance': player['tournament_attendance'],
#             # 'results': player['results']
#         }
#     )

# # --- Find best 5 results for every player to calculate total placing score ---
results_pointer = tournament_collection.aggregate(pipeline2)

# placings = []
# for result in results_pointer:
#     pipeline3 = [
#         {
#             '$match': {
#                 'tag': result['tag']
#             }
#         },
#         {
#             '$sort': {
#                 'placing_score': pymongo.DESCENDING
#             }        
#         },
#         {
#             '$limit': 7
#         },
#         {
#             '$group': {
#                 '_id': '$tag',
#                 'total_placing_score': {'$sum': { '$sum': ['$placing_score']}}
#             }
#         }
#     ]

#     pipeline2.extend(pipeline3)
#     placing_scores_pointer = tournament_collection.aggregate(pipeline2)
#     for placing in placing_scores_pointer:
#         placings.append(placing)
    
#     del pipeline2[2::]

# # --- Attach total placing score to every item in the players list ---
# for player in players:
#     for z in placings:
#         if player['tag'] == z['_id']:
#             player.update({'total_placing_score': z['total_placing_score']})

# # --- Calculate total score ---
# for player in players:
#     if player['tournament_attendance'] >= 5:
#         total_score = round((player['total_placing_score'] / 5) + player['total_wins_score'], 2)
#         player.update({'total_score': total_score})
#     elif player['tournament_attendance'] == 4:
#         total_score = round((player['total_placing_score'] / 4) + player['total_wins_score'], 2)
#         player.update({'total_score': total_score})
#     elif player['tournament_attendance'] <= 3:
#         total_score = round((player['total_placing_score'] / 3) + player['total_wins_score'], 2)
#         player.update({'total_score': total_score})

# # --- Sort players by highest total score ---
# def sort_by_highest_total_score(e):
#     return e['total_score']

# players.sort(reverse=True, key=sort_by_highest_total_score)

results_collection = db['results']

for result in results_pointer:
    results_collection.insert_one(result)

# # Create table
# header = players[0].keys()
# rows = [x.values() for x in players]

# print(tabulate.tabulate(rows, header))

# players_collection = db['players']
# players_collection.insert_many(players)