import pandas as pd
import numpy as np
from collections import Counter


def calculate_similarity(user1_ratings, user2_ratings):
    correlation_coefficient = np.corrcoef(user1_ratings, user2_ratings)[0,1]
    return (1 + correlation_coefficient) / 2 * 100


def recommended_users_by_similarity(ratings_df, user_ratings, n):
    # Generate a new user ID and add the user_ratings to ratings_df
    new_user_id = ratings_df.index[-1] + 1
    ratings_df.loc[new_user_id] = 0
    for game, rating in user_ratings.items():
        ratings_df.at[new_user_id, game] = rating
    
    # Find top users ordered by similarity
    new_user_ratings = ratings_df.loc[new_user_id].values
    similarities = ratings_df.apply(lambda x: calculate_similarity(new_user_ratings, x), axis=1)
    top_users = similarities.drop(new_user_id).nlargest(n).astype(int)

    # Find games that the new user has not played yet
    games_not_played = ratings_df.columns[ratings_df.loc[new_user_id] == 0]
    
    # Recommend games from top users that the new user has not played yet
    recommendations = []
    recommendations_list = []
    for user_id in top_users.index:
        user_top_games = ratings_df.loc[user_id][ratings_df.loc[user_id] > 0].nlargest(10).index
        recommended_games = [game for game in user_top_games if game in games_not_played][:5]
        recommendations.append({"similarity":top_users[user_id], "recommended_games":recommended_games})
        recommendations_list.extend(recommended_games)

    # Find 3 most common games among the recommendations
    game_counts = Counter(recommendations_list)
    top3 = game_counts.most_common(3)
    
    return recommendations, top3


def recommended_users_by_common_games(ratings_df, user_ratings, n):
    # Generate a new user ID and add the user_ratings to ratings_df
    new_user_id = ratings_df.index[-1] + 1
    ratings_df.loc[new_user_id] = 0
    for game, rating in user_ratings.items():
        ratings_df.at[new_user_id, game] = rating
    
    # Find top users ordered by similarity
    users_games = (ratings_df > 0).astype(int)
    new_user_games = (ratings_df.loc[new_user_id] > 0).astype(int)
    top_users = users_games.dot(new_user_games.T).sort_values(ascending=False).drop(new_user_id).head(n)

    # Find games that the new user has not played yet
    games_not_played = ratings_df.columns[ratings_df.loc[new_user_id] == 0]
    
    # Recommend games from top users that the new user has not played yet
    recommendations = []
    recommendations_list = []
    for user_id in top_users.index:
        user_top_games = ratings_df.loc[user_id][ratings_df.loc[user_id] > 0].nlargest(15).index
        recommended_games = [game for game in user_top_games if game in games_not_played][:5]
        recommendations.append({"common_games":top_users[user_id], "recommended_games":recommended_games})
        recommendations_list.extend(recommended_games)

    # Find 3 most common games among the recommendations
    game_counts = Counter(recommendations_list)
    top3 = game_counts.most_common(3)
    
    return recommendations, top3