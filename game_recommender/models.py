from game_recommender import db


# One user can have multiple games and one game can have multiple users so we have many-to-many relationship. 
# For this reason, 'ratings' table is used whcih have many-to-many relationship between users and games as well as one-to-one relationship with ratings

class User(db.Model): 
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default="default.jpg")
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Game(db.Model):
    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"<Game: {self.title}>"


class Rating(db.Model):
    __tablename__ = "ratings"
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"))
    rating = db.Column(db.Integer)

    user = db.relationship("User", backref=db.backref("ratings", lazy=True))
    game = db.relationship("Game", backref=db.backref("ratings", lazy=True))

    def __repr__(self):
        return f"<Rating: ({self.user.username}, {self.game.title}, {self.rating})"