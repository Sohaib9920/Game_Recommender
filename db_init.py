from game_recommender import app, db, ubyi_norm_0
from game_recommender.models import User, Game, Rating

## Drop all tables if existed ##
# with app.app_context():
#     db.drop_all()

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


# Add new dummy user to 'users' table
# with app.app_context():
#     sohaib = User(username="Sohaib123", email="sohaib123.ahmed@gamil.com", password="jam225544")
#     db.session.add(sohaib)
#     db.session.commit()
#     print(User.query.first())


## Add second user, use query:
# INSERT INTO users (username, email, image_file, password) VALUES ("Ammar543", "kimono_007@gamil.com", "default.jpg", "ammar5680");


# # Adding user ratings and games
# username="Sohaib123"
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

#         rating = Rating(rating=rating, game_id=game.id, user_id=user.id)
#         db.session.add(rating)
    
#     db.session.commit()
#     print(Rating.query.all())

with app.app_context():
    user = User.query.filter_by(username="sohaib456").first()
    game_ratings = Rating.query.filter_by(user_id=user.id).order_by(Rating.rating.desc()).all()
    print(game_ratings)
    for rating in game_ratings:
        print(rating.game.title, rating.rating)
        
        

        