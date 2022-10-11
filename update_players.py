import os
from pprint import pprint
import tabulate

from bson.objectid import ObjectId
from dotenv import load_dotenv
import pymongo

from repeated_players import repeated_players

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGO_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "smash_zulia" database:
db = client["smash_zulia"]

# Get a reference to the "results" collection:
results_collection = db["results"]

# Get a reference to the  "players" collection:
player_collection = db["players"]

pipeline = [
    {
        '$match': {}
    },
    {
        '$lookup': {
            'from': 'players',
            'localField': 'player_id',
            'foreignField': '_id',
            'as': 'results'
        }
    },
    {
        '$unwind': '$results'
    },
    {
        '$group': {
            '_id': '$player_id',
            'tag': {'$first': '$tag'},
            'total_wins_score': {'$sum': { '$sum': '$wins_score'}},
            'tournament_attendance': {'$sum': 1},
            'city': {'$first': '$results.city'},
            'results': {
                    '$push': {
                    'tournament_id': '$tournament_id',
                    'placing': '$placing',
                    'tournament': '$tournament',
                    'tournament_city': '$city', 
                    'placing_score': '$placing_score',
                    'notable_wins': '$notable_wins', 
                    'wins_score': '$wins_score'
                }
            }
        }
    },
]

updated_player_pointer = results_collection.aggregate(pipeline)

dummy_list = []


for player in updated_player_pointer:
    # Get all the results from every player
    results = player['results']

    # Find tournaments traveled to
    tournaments_traveled = 0
    for result in results:
        if player['city'] != result['tournament_city']:
            tournaments_traveled += 1

    # Find total placing score
    def myFunc(e):
        return e['placing_score']

    results.sort(key=myFunc)

    total_placing_score = 0
    for result in results[0:7]:
        placing_score = result.get('placing_score')
        total_placing_score += placing_score

    # Get current total score
    ratio = 0
    if player['tournament_attendance'] >= 5:
        ratio = 5
    elif player['tournament_attendance'] == 4:
        ratio = 4
    if player['tournament_attendance'] <= 3:
        ratio = 3

    placing_score_ratio = total_placing_score / ratio

    # Travel buff
    travel_buff = 0

    if tournaments_traveled >= 2:
        travel_buff = 0.2
    elif tournaments_traveled == 1:
        travel_buff = 0.1
    
    bonus_points = placing_score_ratio * travel_buff

    total_score = player['total_wins_score'] + placing_score_ratio + bonus_points

    player_collection.update_one({'_id': player['_id']}, { "$set": { 
        'tournament_attendance': player['tournament_attendance'],
        'total_wins_score': player['total_wins_score'],
        'total_placing_score': total_placing_score,
        'tournaments_traveled_to': tournaments_traveled,
        'total_score': total_score
    }})
