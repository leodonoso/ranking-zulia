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

# Get a reference to the  "tournaments" collection:
tournament_collection = db["tournaments"]

# Get a reference to the  "cities" collection:
cities_collection = db["cities"]

# Define Pipeline Stages

stage_lookup_player = {
    '$lookup': {
            'from': 'players',
            'localField': 'player_id',
            'foreignField': '_id',
            'as': 'results'
        }
}

stage_unwind_results = {
        '$unwind': '$results'
    }

stage_group_results_by_player = {
        '$group': {
            '_id': '$player_id',
            'tag': {'$first': '$results.tag'},
            'total_wins_score': {'$sum': { '$sum': '$wins_score'}},
            'tournament_attendance': {'$sum': 1},
            'city': {'$first': '$results.city'},
            'results': {
                    '$push': {
                    'tournament_id': '$tournament_id',
                    'placing': '$placing',
                    'placing_score': '$placing_score',
                    'notable_wins': '$notable_wins', 
                    'wins_score': '$wins_score'
                }
            }
        }
    }

update_pipeline = [
    stage_lookup_player,
    stage_unwind_results,
    stage_group_results_by_player,
]

updated_player_pointer = results_collection.aggregate(update_pipeline)

dummy_list = []

for player in updated_player_pointer:
    # Get player city's document TEMPORAL
    city_document = cities_collection.find_one({'_id': player['city']})

    # Get all the results from every player
    results = player['results']

    if city_document == None:
        tourney_for_city = tournament_collection.find_one({'_id': results[0]['tournament_id']})
        player.update({'city': tourney_for_city['city']})

    # Find tournaments traveled to
    tournaments_traveled = 0
    for result in results:
        result_tournament_id = result['tournament_id']

        result_tournament = tournament_collection.find_one({'_id': result_tournament_id})

        if player['city'] != result_tournament['city']:
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

    player.update({
        'total_placing_score': total_placing_score,
        'tournaments_traveled_to': tournaments_traveled,
        'total_score': total_score
    })

    # Update players collection
    player_collection.update_one({'_id': player['_id']}, { "$set": { 
        'tournament_attendance': player['tournament_attendance'],
        'total_wins_score': player['total_wins_score'],
        'city': player['city'],
        'total_placing_score': total_placing_score,
        'tournaments_traveled_to': tournaments_traveled,
        'total_score': total_score
    }})
