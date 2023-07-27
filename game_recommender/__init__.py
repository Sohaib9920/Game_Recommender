import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from game_recommender.matrix_factorization import ExplicitMF
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # make using secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" # store session data in server filesystem

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # Specify where to redirect when login is required
login_manager.login_message_category = "info"
Session(app) # initializes the session functionality in the Flask app


data_file_path = os.path.join(app.root_path, "ubyi_norm_0.csv")

# Load the data and initialize the recommender
ubyi_norm_0 = pd.read_csv(data_file_path, index_col=0)
als = ExplicitMF(n_iters=5, n_factors=20, reg=0.01)
game_names = ubyi_norm_0.columns.values.tolist()
FAVOURITE_RATING = 7

from game_recommender import routes

## Explanation of Matrix Factorization for Recommender Systems ##

# The 'ubyi_norm_0' dataframe represents a user-by-item matrix where rows correspond to users, columns correspond to games, and the values represent game ratings. 
# In this case, the ratings have been normalized using log(hours played) and scaled to a rating range of 1 to 10. Any missing values in the dataframe have been replaced with 0 for model fitting.

# The Matrix Factorization model used here is known as ExplicitMF. It is based on the concept explained in the video tutorial "https://www.youtube.com/watch?v=ZspR5PZemcs" and the article "https://towardsdatascience.com/recommendation-system-matrix-factorization-d61978660b4b".
# The main idea behind Matrix Factorization is to break down the target matrix (User x Games) into two separate matrices: one for users (User x user_features) and one for games (Games x games_features). 
# These matrices contain latent features that capture the underlying characteristics of users and games.
# The goal of the Matrix Factorization model is to find the optimal values for these latent features that minimize the error between the predicted ratings in the User x Games matrix and the actual ratings in the 'ubyi_norm_0' dataframe.
# Gradient descent is employed as an optimization algorithm to iteratively update the latent feature values and reduce the error between the predicted and actual ratings. The process continues until the error converges to a minimum.
# By performing Matrix Factorization, the model can predict ratings for user-game pairs that were not originally present in the 'ubyi_norm_0' dataframe. This enables the generation of personalized recommendations based on the predicted ratings.
# Overall, Matrix Factorization provides an effective approach for building recommender systems by uncovering latent features and predicting user-item interactions with minimal error.


## How cookies and sessions work ##

# 1) User Opens the Website: 
#    When a user visits your website for the first time, their browser sends a request to your server.
#    The server processes the request and generates a response. If the server is configured to use sessions, it includes a Set-Cookie header in the response to initiate a new session for the user.

# 2) Setting up the Session:
#    When the user's browser receives the response with the Set-Cookie header, it stores the cookie locally.
#    The cookie contains a session ID, which is a unique identifier for the user's session on your website.

# 3) User Interacts with Website:
#    The session ID is sent back to the server in every subsequent HTTP request through the Cookie header, allowing the server to recognize the user's session.

# 4) Using the Session Object:
#    The Flask session object provides a dictionary-like interface to work with session data.
#    The session data is stored on server's session storage (e.g., memory, filesystem, database).
#    Data stored in the session will persist throughout the user's visit to your website.

# 5) Flash Messages:
#    In addition to storing general session data, you can use the flash function provided by Flask to add temporary messages (flash messages) to the session.

# 6) User Leaves the Website:
#    When the user closes their browser or the session expires (due to inactivity or session timeout), the session data on the server is cleared.
#    If the user returns to your website later, a new session ID will be generated for them, and the process starts again.
#    If app.config["SESSION_PERMANENT"] = True, then session ID in cookie will remain same on reponing the browser and hence user session is preserved
#    Even though we can store user 