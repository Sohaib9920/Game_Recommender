from flask import request, render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from game_recommender import db, ubyi_norm_0, df_last_id
from game_recommender.models import Rating, Game
from game_recommender.user_info.forms import UpdateAccountForm
from game_recommender.user_info.utils import save_picture

user_info = Blueprint("user_info", __name__)

@user_info.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("user_info.account"))
    
    elif request.method == "GET":  # So that fields are not filled when form is invalidated on POST request
        form.username.data = current_user.username
        form.email.data = current_user.email

    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).all()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("user_info/account.html", title="Account", image_file=image_file, form=form, game_ratings=game_ratings)
    

@user_info.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # Instead of quering database for each game name to get game object, query single time and store the result in {game name: game object}
        game_mapping = {game_object.title : game_object for game_object in Game.query.all()}

        # It is easier to initailly remove all the ratings of user and then re-add them at once after both updating existing games and inserting new games
        Rating.query.filter_by(user=current_user).delete()
        # Also initially remove the ratings of current user from dataframe
        df_user_id = df_last_id + current_user.id 
        ubyi_norm_0.loc[df_user_id] = 0

        for key, value in request.form.items():
            if key.startswith("games-"):
                game_name = value.strip() # must be striped as JS validation allows unstriped value of game name
                rating = int(request.form.get(f"ratings-{key.split('-')[1]}")) # make sure that the rating is integer
                
                # Add new ratings objects to user
                game_object = game_mapping.get(game_name) # JS validation makes sure that game_object for input game name exits
                rating_object = Rating(user = current_user, game = game_object, rating = rating)
                db.session.add(rating_object) 
                # Add new user ratings to dataframe
                ubyi_norm_0.at[df_user_id, game_name] = rating
        
        db.session.commit()
        return redirect(url_for("user_info.account"))

    # Render the tempelate with values of game names and ratings inserted so that we could re submit them (after updating) in post request       
    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).all()
    return render_template("user_info/profile.html", title="Profile", game_ratings=game_ratings)

