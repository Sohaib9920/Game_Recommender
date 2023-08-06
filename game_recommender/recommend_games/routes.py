from flask import render_template, Blueprint, current_app
from game_recommender.recommend_games.forms import RecommenderForm
from game_recommender.recommend_games.recommender import recommend

recommend_games = Blueprint("recommend_games", __name__)

FAVOURITE_RATING = 7

@recommend_games.route("/", methods=["GET", "POST"])
def home():
    form = RecommenderForm()
    if form.validate_on_submit():
        user_ratings = {}
        for i in range(5): 
            game_name = form.games[i].data.strip() # must strip as js validation ignore trailing spaces and allow these values in payload
            user_ratings[game_name] = FAVOURITE_RATING # JavaScript is used to validate valid names and avoid duplicates.

        recommendations = recommend(current_app.ubyi_norm_0, user_ratings, current_app.als) # this function do not alter original dataframe
        return render_template("recommend_games/recommendations.html", title="Recommendations", recommendations=recommendations)
    
    return render_template("recommend_games/recommender.html", title="Recommender", form=form)


@recommend_games.route("/get_recommended_names", methods=["GET"])
def get_recommended_names():
    game_names = current_app.ubyi_norm_0.columns.values.tolist()
    return {"recommended_names": game_names}  