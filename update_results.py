# tuki = {
#     '_id': 'a',
# "player_id": '',
# "tournament_id": '',
# "tag": '',
# "placing": "1",
# 'tournament': "NEO: Lucina's Coliseum #8",
# "city": "Maracaibo",
# "placing_score": "155",
# "notable_wins": '',
# 'wins_score': 43}

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

# Get a reference to the "tournaments" collection:
tournament_collection = db["tournaments"]

# Create pipeline
pipeline = [
    {
        '$unwind': '$standings'
    },
    {
        '$project': {
            "player_id": '$standings.player_id',
            "tournament_id": '$_id',
            "tag": '$standings.gamertag',
            "placing": "$standings.placing",
            'tournament': "$name",
            "city": "$city",
            "placing_score": "$standings.placing_score",
            "notable_wins": {'$size': '$standings.notable_wins'},
            'wins_score': '$standings.wins_score'
        }
    }
]

new_results_pointer = tournament_collection.aggregate(pipeline)
# old_results_pointer = results_collection.find()
for new_result in new_results_pointer:
    print(new_result)
    new_result['_id'] = ObjectId()
    results_collection.insert_one(new_result)


# for new_result in new_results_pointer:
#     for old_result in old_results_pointer:
#         if new_result['player_id'] == old_result['player_id'] and new_result['tournament_id'] == old_result['tournament_id']:
#             results_collection.update_one({'player_id': new_result['player_id']}, [{'$set': {
#                 "player_id": new_result["player_id"],
#                 "tournament_id": new_result["tournament_id"],
#                 "tag": new_result["tag"],
#                 "placing": new_result["placing"],
#                 'tournament': new_result["tournament"],
#                 "city": new_result["city"],
#                 "placing_score": new_result["placing_score"],
#                 "notable_wins": new_result["notable_wins"],
#                 'wins_score': new_result["wins_score"]
#             }
#         }])
#         else:
#             # new_result['_id'] = ObjectId()
#             # print(new_result)
#             # # results_collection.insert_one(new_result)
#             pass

# # Remove duplicates
# results_pointer = results_collection.find()

