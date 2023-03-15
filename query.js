db.results.aggregate(
    [
        {
            '$match': {'player_id': ObjectId('635c5bebb907ee9fed2729ef')}
        },
        {
            '$lookup': {
                'from': 'players',
                'localField': 'player_id',
                'foreignField': '_id',
                'as': 'results'
            }
        },
        // {
        //     '$unwind': '$results'
        // },
        // {
        //     '$group': {
        //         '_id': '$player_id',
        //         'tag': {'$first': '$results.tag'},
        //         'total_wins_score': {'$sum': { '$sum': '$wins_score'}},
        //         'tournament_attendance': {'$sum': 1},
        //         'city': {'$first': '$results.city'},
        //         'results': {
        //                 '$push': {
        //                 'tournament_id': '$tournament_id',
        //                 'placing': '$placing',
        //                 'placing_score': '$placing_score',
        //                 'notable_wins': '$notable_wins', 
        //                 'wins_score': '$wins_score'
        //             }
        //         }
        //     }
        // },
    ]    
).pretty()