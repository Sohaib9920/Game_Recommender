import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from flask_mail import Mail
from game_recommender.config import Config
from game_recommender.matrix_factorization import ExplicitMF


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "user_authentication.login" # Specify where to redirect when login is required
login_manager.login_message_category = "info"
sess = Session() # initializes the session functionality in the Flask app
mail = Mail()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)
    mail.init_app(app)

    # Load the data and initialize the recommender
    data_file_path = os.path.join(app.root_path, "ubyi_norm_0.csv")
    ubyi_norm_0 = pd.read_csv(data_file_path, index_col=0)
    df_last_id = ubyi_norm_0.index[-1]
    als = ExplicitMF(n_iters=5, n_factors=20, reg=0.01)

    with app.app_context():
        app.df_last_id = df_last_id
        app.als = als
        # Insert user ratings from database into dataframe
        from game_recommender.utils import add_db_users
        add_db_users(ubyi_norm_0) 
        app.ubyi_norm_0 = ubyi_norm_0

    from game_recommender.recommend_games.routes import recommend_games
    from game_recommender.recommend_users.routes import recommend_users
    from game_recommender.user_authentication.routes import user_authentication
    from game_recommender.user_info.routes import user_info

    app.register_blueprint(recommend_games)
    app.register_blueprint(recommend_users)
    app.register_blueprint(user_authentication)
    app.register_blueprint(user_info)
    
    return app