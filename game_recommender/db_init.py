from game_recommender import app, db, ubyi_norm_0
from game_recommender.models import User, Game, Rating

## Create database tables ## 
# with app.app_context():
#     db.create_all()


## Show schema of database by running on terminal:
# sqlite3 instance/site.db
# .schema


## Adding game names to 'game' table ##
# with app.app_context():
#     for title in ubyi_norm_0.columns:
#         game = Game(title=title)
#         db.session.add(game)
#     db.session.commit()


## Check the games by running on terminal:
# sqlite3 instance/site.db
# .mode table
# SELECT * FROM games 


## Checking game table ##
# with app.app_context():
#     games = Game.query.all()
#     print(games)


## Add new dummy user to 'users' table
# with app.app_context():
    # sohaib = User(username="Sohiab123", email="sohaib9920.ahmed@gamil.com", password="jam225544")
    # db.session.add(sohaib)
    # db.session.commit()
    # print(User.query.first())


## Add second user, use query:
# INSERT INTO users (username, email, image_file, password) VALUES ("Ammar543", "kimono_007@gamil.com", "default.jpg", "ammar5680");


## Adding user ratings and games
# username="Sohiab123"
# game_list= [{"title": "Dota 2", "rating": 9},
#         {"title": "Fallout New Vegas", "rating": 9},
#         {"title": "Dark Souls Prepare to Die Edition", "rating": 9},
#         {"title": "Dishonored", "rating": 8},
#         {"title": "BioShock", "rating": 8}]

# with app.app_context():
#     # Instead of quering for every game, lets just make dict of {game_title: game_object} after single search query
#     game_mapping = {game_object.title:game_object for game_object in Game.query.all()}

#     # Get the given user object. For this user, get all game objects. Use them to create rating objects
#     user = User.query.filter_by(username=username).first()

#     for game_info in game_list:
#         game = game_mapping.get(game_info["title"])
#         # If that game was not previously existed then make it and add it to db and game_mapping
#         if game is None:
#             game = Game(title=game_info["title"])
#             db.session.add(game)
#             db.session.flush() # Flush to generate game_id. It kind of refreshes the db
#             game_mapping[game.title] = game

#         rating = Rating(rating=game_info["rating"], game_id=game.game_id, user_id=user.user_id)
#         db.session.add(rating)
    
#     db.session.commit()
#     print(Rating.query.all())


# ## Adding another user with differnt game_list:
# username="Ammar543"
# game_list = {"Dota 2": 9, "BioShock": 7, "Dishonored":8, "Dark Souls Prepare to Die Edition":9, "The Witcher 3 Wild Hunt": 10}
# with app.app_context():
#     game_mapping = {game_object.title:game_object for game_object in Game.query.all()}
#     user = User.query.filter_by(username=username).first()

#     for game_name, rating in game_list.items():
#         game = game_mapping.get(game_name)
#         # If that game was not previously existed then make it and add it to db and game_mapping
#         if game is None:
#             game = Game(title=game_name)
#             db.session.add(game)
#             db.session.flush() # Flush to generate game_id. It kind of refreshes the db
#             game_mapping[game.title] = game

#         rating = Rating(rating=rating, game_id=game.game_id, user_id=user.user_id)
#         db.session.add(rating)
    
#     db.session.commit()
#     print(Rating.query.all())

    

        
        

        