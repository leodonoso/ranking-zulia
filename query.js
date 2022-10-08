// Group all results and get the total wins score of each player
db.tournaments.aggregate(
    [
        {
            $unwind: '$standings'
        },
        {
            $project: {
                tag: '$standings.gamertag', 
                placing: '$standings.placing', 
                tournament: '$name', 
                placing_score: '$standings.placing_score', 
                wins_score: '$standings.wins_score' 
            }
        },
        // {
        //     $match: {
        //         tag: 'Pancakes'
        //     }        
        // },
        {
            $group: {
                _id: '$tag',
                // total_placing_score: {'$sum': { $sum: ['$placing_score']}},
                total_wins_score: {'$sum': { $sum: ['$wins_score']}},
                tournament_attendance: {'$sum': 1},
                results: {'$push': {
                        placing: '$placing', 
                        tournament: '$tournament', 
                        placing_score: '$placing_score', 
                        wins_score: '$wins_score'
                    }
                }
            }
        }
    ]
).pretty()

// Group all results, sort by the best 5 placing scores, and calculate total placing score
db.tournaments.aggregate(
    [
        {
            $unwind: '$standings'
        },
        {
            $project: {
                tag: '$standings.gamertag', 
                placing: '$standings.placing', 
                tournament: '$name', 
                placing_score: '$standings.placing_score', 
                wins_score: '$standings.wins_score' 
            }
        },
        {
            $match: {
                tag: 'Tobio'
            }        
        },
        {
            $sort: {
                'placing_score': -1
            }        
        },
        {
            $limit: 5
        },
        {
            $group: {
                _id: '$tag',
                total_placing_score: {'$sum': { $sum: ['$placing_score']}},
                // total_wins_score: {'$sum': { $sum: ['$wins_score']}},
                // tournament_attendance: {'$sum': 1},
                // results: {'$push': {
                //         placing: '$placing', 
                //         tournament: '$tournament', 
                //         placing_score: '$placing_score', 
                //         wins_score: '$wins_score'
                //     }
                // }
            }
        }
    ]
).pretty()