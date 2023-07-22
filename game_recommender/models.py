from game_recommender import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id): # This function is required in order to reload the user object from user ID stored in session
    return User.query.get(int(user_id))

# One user can have multiple games and one game can have multiple users so we have many-to-many relationship. 
# For this reason, 'ratings' table is used whcih have many-to-many relationship between users and games as well as one-to-one relationship with ratings

class User(db.Model, UserMixin): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default="default.jpg")
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<Game: {self.title}>"


class Rating(db.Model):
    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    rating = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref("ratings", lazy=True))
    game = db.relationship("Game", backref=db.backref("ratings", lazy=True))

    def __repr__(self):
        return f"<Rating: ({self.user.username}, {self.game.title}, {self.rating})>"