import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from game_recommender.matrix_factorization import ExplicitMF
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # Specify where to redirect when login is required
login_manager.login_message_category = "info"


data_file_path = os.path.join(app.root_path, "ubyi_norm_0.csv")

# Load the data and initialize the recommender
ubyi_norm_0 = pd.read_csv(data_file_path, index_col=0)
als = ExplicitMF(n_iters=5, n_factors=20, reg=0.01)
game_names = ubyi_norm_0.columns.values.tolist()
FAVOURITE_RATING = 7

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

from game_recommender import routes