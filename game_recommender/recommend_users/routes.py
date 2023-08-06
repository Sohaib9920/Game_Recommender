from flask import render_template, url_for, flash, redirect, session, current_app
from flask_login import login_required, current_user
from game_recommender.recommend_users.recommender import recommend_users_by_common_games, recommend_users_by_similarity

from flask import Blueprint

recommend_users = Blueprint("recommend_users", __name__)

@recommend_users.route("/recommend_users")
@login_required
def home():
    if current_user.ratings:
        user_ratings = {}
        for rating_object in current_user.ratings:
            user_ratings[rating_object.game.title] = rating_object.rating

        n_recommendations = 20
        # The following functions do not alter original dataframe
        common_recommendations, common_top5 = recommend_users_by_common_games(current_app.ubyi_norm_0, user_ratings, n_recommendations)
        similarity_recommendations, similarity_top5 = recommend_users_by_similarity(current_app.ubyi_norm_0, user_ratings, n_recommendations)

        # Store the recommendations and top5 values in the session
        session['common_recommendations'] = common_recommendations
        session['common_top5'] = common_top5
        session['similarity_recommendations'] = similarity_recommendations
        session['similarity_top5'] = similarity_top5
    else:
        flash("Please add games to your Gamer Profile first", "danger")
        return redirect(url_for("user_info.profile"))
    return render_template("recommend_users/recommend.html", title="Recommend Users", common_top5=common_top5, similarity_top5=similarity_top5)

# In order to make sure that recommended_users routes are accessed AFTER visiting recommend_users route,
# We make forms for each button for each route and use POST request to access these routes

@recommend_users.route("/recommend_users/common", methods=["POST"]) 
@login_required
def users_common():
    common_recommendations = session.get('common_recommendations')
    return render_template("recommend_users/users_common.html", title="Recommended Users", 
                           common_recommendations=common_recommendations)


@recommend_users.route("/recommend_users/similarity", methods=["POST"])
@login_required
def users_similarity():
    similarity_recommendations = session.get('similarity_recommendations')
    return render_template("recommend_users/users_similarity.html", title="Recommended Users", 
                           similarity_recommendations=similarity_recommendations)