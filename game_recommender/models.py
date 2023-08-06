from flask import current_app
from game_recommender import db, login_manager
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as TimedSerializer



@login_manager.user_loader
def load_user(user_id): # This function is required in order to reload the user object from user ID stored in session
    return User.query.get(int(user_id))

# One user can have multiple games and one game can have multiple users so we have many-to-many relationship. 
# For this reason, 'ratings' table is used whcih have many-to-many relationship between users and games as well as one-to-one relationship with ratings

# flask_login extension expects the User model to have certain methods: 1) is_authenticated 2) is_active 3) is_anonymous 4) get_id
# We can inherent from UserMixin class to add all of these

class User(db.Model, UserMixin): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default="default.jpg")
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"
    
    # Methods for handling timed tokens for password reset
    def get_reset_token(self):
        s = TimedSerializer(current_app.config["SECRET_KEY"])
        token = s.dumps({"user_id": self.id}) # Dump the payload into serializer
        return token
    
    @staticmethod
    def verify_reset_token(token, expire_sec=1800):
        s = TimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=expire_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    
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