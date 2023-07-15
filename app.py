import numpy as np
import pandas as pd
from matrix_factorization import ExplicitMF
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

# Load the data and initialize the recommender
ubyi_norm_0 = pd.read_csv("ubyi_norm_0.csv", index_col=0)
als = ExplicitMF(n_iters=5, n_factors=80, reg=0.01)
column_names = ubyi_norm_0.columns.values

# Explanation of Matrix Factorization for Recommender Systems

# The 'ubyi_norm_0' dataframe represents a user-by-item matrix where rows correspond to users, columns correspond to games, and the values represent game ratings. 
# In this case, the ratings have been normalized using log(hours played) and scaled to a rating range of 1 to 10. Any missing values in the dataframe have been replaced with 0 for model fitting.

# The Matrix Factorization model used here is known as ExplicitMF. It is based on the concept explained in the video tutorial "https://www.youtube.com/watch?v=ZspR5PZemcs" and the article "https://towardsdatascience.com/recommendation-system-matrix-factorization-d61978660b4b".
# The main idea behind Matrix Factorization is to break down the target matrix (User x Games) into two separate matrices: one for users (User x user_features) and one for games (Games x games_features). 
# These matrices contain latent features that capture the underlying characteristics of users and games.
# The goal of the Matrix Factorization model is to find the optimal values for these latent features that minimize the error between the predicted ratings in the User x Games matrix and the actual ratings in the 'ubyi_norm_0' dataframe.
# Gradient descent is employed as an optimization algorithm to iteratively update the latent feature values and reduce the error between the predicted and actual ratings. The process continues until the error converges to a minimum.
# By performing Matrix Factorization, the model can predict ratings for user-game pairs that were not originally present in the 'ubyi_norm_0' dataframe. This enables the generation of personalized recommendations based on the predicted ratings.
# Overall, Matrix Factorization provides an effective approach for building recommender systems by uncovering latent features and predicting user-item interactions with minimal error.


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        game_ratings = {}
        for i in range(1, 4): 
            game_name = request.form.get(f'game{i}_name')

            if game_name in column_names:
                game_rating = float(request.form.get(f'game{i}_rating'))
                game_ratings[game_name] = game_rating

        # Generate a new user ID and add the ratings to ubyi_norm_0
        new_user_id = ubyi_norm_0.index[-1] + 1
        ubyi_norm_0.loc[new_user_id] = 0
        for game, rating in game_ratings.items():
            ubyi_norm_0.at[new_user_id, game] = rating

        # Re-fit the ALS model with updated ubyi_norm_0
        als.fit(ubyi_norm_0.to_numpy())

        # Execute the recommendation function
        ratings = np.dot(als.user_factors, als.item_factors.T)
        ubyi_mf = pd.DataFrame(ratings, index=ubyi_norm_0.index.values, columns=ubyi_norm_0.columns.values)
        games_to_consider_mask = ubyi_norm_0.loc[new_user_id] == 0
        top5 = ubyi_mf.loc[new_user_id, games_to_consider_mask].sort_values(ascending=False)[:5].index.values
        recommendations = [{'rank': idx+1, 'game': game} for idx, game in enumerate(top5)]

        return render_template('recommendations.html',title="Recommendations", recommendations=recommendations)
    
    return render_template('index.html', title="Recommender")


@app.route('/get_recommended_names', methods=['GET'])
def get_recommended_names():
    column_names = ubyi_norm_0.columns.values
    return {'recommended_names': column_names.tolist()}   


if __name__ == '__main__':
    app.run(debug=False)
