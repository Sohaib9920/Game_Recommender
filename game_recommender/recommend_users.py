import pandas as pd
import numpy as np
from collections import Counter


def calculate_similarity(user1_ratings, user2_ratings):
    correlation_coefficient = np.corrcoef(user1_ratings, user2_ratings)[0,1]
    return (1 + correlation_coefficient) / 2 * 100


def recommend_users_by_similarity(ratings_df, user_ratings, n):
    """
    Recommends top similar users to a new user based on their game ratings similarity.

    Parameters:
        ratings_df (pandas.DataFrame): DataFrame containing user ratings where user IDs are the index and game names are the columns.
        user_ratings (dict): A dictionary containing the game ratings of the new user, where keys are game names (str) and values are ratings (int).
        n (int): The number of top similar users to recommend.

    Returns:
        tuple: A tuple containing two elements:
            - list: A list of dictionaries containing the recommended users and their similarity percentages. Each dictionary has the keys:
                    - "similarity" (float): The similarity percentage (ranging from 0 to 100) of the recommended user with the new user.
                    - "recommended_games" (list): A list of up to 5 game names that the recommended user has highly rated and the new user has not played yet.
            - list: A list of tuples containing the five most common recommended game names among all the recommended users along with their respective frequencies.

    Example:
        ratings_df = ...  # Your existing DataFrame with user ratings
        user_ratings = {'Game1': 3, 'Game2': 5, 'Game3': 2, ...}  # Replace ... with other game ratings
        n = 20  # Number of top users to consider for similarity
        recommendations, top3_games = recommend_users_by_similarity(ratings_df, user_ratings, n)
    """

    # copy the original ratings dataframe in order to avoid adding same user multiple times on multiple function calls
    ratings_df = ratings_df.copy()

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
    top5 = game_counts.most_common(5)
    
    return recommendations, top5


def recommend_users_by_common_games(ratings_df, user_ratings, n):
    """
    Recommends top users based on the number of common games played with a new user.

    Parameters:
        ratings_df (pandas.DataFrame): DataFrame containing user ratings where user IDs are the index and game names are the columns.
        user_ratings (dict): A dictionary containing the game ratings of the new user, where keys are game names (str) and values are ratings (int).
        n (int): The number of top users to recommend.

    Returns:
        tuple: A tuple containing two elements:
            - list: A list of dictionaries containing the recommended users and the number of common games played with the new user. Each dictionary has the keys:
                    - "n_common_games" (int): The number of common games played by the recommended user with the new user.
                    - "recommended_games" (list): A list of up to 5 game names that the recommended user has highly rated and the new user has not played yet.
            - list: A list of tuples containing the five most common recommended game names among all the recommended users along with their respective frequencies.

    Example:
        ratings_df = ...  # Your existing DataFrame with user ratings
        user_ratings = {'Game1': 3, 'Game2': 5, 'Game3': 2, ...}  # Replace ... with other game ratings
        n = 20  # Number of top users to consider for recommendation
        recommendations, top3_games = recommend_users_by_common_games(ratings_df, user_ratings, n)
    """
    
    # copy the original ratings dataframe in order to avoid adding same user multiple times on multiple function calls
    ratings_df = ratings_df.copy() 

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
        recommendations.append({"n_common_games":top_users[user_id], "recommended_games":recommended_games})
        recommendations_list.extend(recommended_games)

    # Find 3 most common games among the recommendations
    game_counts = Counter(recommendations_list)
    top5 = game_counts.most_common(5)
    
    return recommendations, top5