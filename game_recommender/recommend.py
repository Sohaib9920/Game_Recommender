import pandas as pd 
import numpy as np

def recommend_games(ratings_df, user_ratings, als_model):
    """
    Recommends games to a user based on their ratings and a matrix factorization model.

    Parameters
    ----------
    ratings_df : pandas.DataFrame
        DataFrame containing user ratings for games. Rows represent users, columns represent games.

    user_ratings : dict
        Dictionary containing ratings provided by the user. Keys are game names and values are ratings.

    als_model : object
        An instance of the matrix factorization model used for prediction.

    Returns
    -------
    recommendations : list
        A list of top 5 recommended games for the user, sorted by rating.

    """
    
    # Generate a new user ID and add the user_ratings to ratings_df
    new_user_id = ratings_df.index[-1] + 1
    ratings_df.loc[new_user_id] = 0
    for game, rating in user_ratings.items():
        ratings_df.at[new_user_id, game] = rating

    # Fit the Alternating Least Squares (ALS) model with the updated ratings_df
    als_model.fit(ratings_df.to_numpy())

    # Get the predicted ratings DataFrame. Add index and columns to create a DataFrame
    predicted_ratings_matrix = np.dot(als_model.user_factors, als_model.item_factors.T)
    user_by_item_df = pd.DataFrame(predicted_ratings_matrix, 
                                   index=ratings_df.index.values, 
                                   columns=ratings_df.columns.values)
    
    # Recommend the top 5 games with the highest rating that the user has not played
    games_to_consider_mask = ratings_df.loc[new_user_id] == 0
    recommendations = user_by_item_df.loc[new_user_id, games_to_consider_mask].sort_values(ascending=False)[:5].index.values

    return recommendations

