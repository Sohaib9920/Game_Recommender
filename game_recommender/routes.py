from flask import request, render_template, url_for, flash, redirect, session
from game_recommender import app, db, bcrypt, ubyi_norm_0, als, game_names, FAVOURITE_RATING
from game_recommender.forms import RecommenderForm, RegistrationForm, LoginForm, UpdateAccountForm, ResetRequestForm, ResetPasswordForm
from game_recommender.models import User, Rating, Game
from game_recommender.recommend import recommend_games
from flask_login import login_user, logout_user, login_required, current_user
from game_recommender.utils import save_picture, send_reset_message, add_db_users
from game_recommender.recommend_users import recommend_users_by_common_games, recommend_users_by_similarity

# Getting the last user id in initail dataframe when no new user from database is added
df_last_id = ubyi_norm_0.index[-1]

# Insert user ratings from database into dataframe
with app.app_context():
    add_db_users(ubyi_norm_0)


@app.route("/", methods=["GET", "POST"])
def home():
    form = RecommenderForm()
    if form.validate_on_submit():
        user_ratings = {}
        for i in range(5): 
            game_name = form.games[i].data.strip() # must strip as js validation ignore trailing spaces and allow these values in payload
            user_ratings[game_name] = FAVOURITE_RATING # JavaScript is used to validate valid names and avoid duplicates.

        recommendations = recommend_games(ubyi_norm_0, user_ratings, als) # this function do not alter original dataframe
        return render_template("recommendations.html", title="Recommendations", recommendations=recommendations)
    
    return render_template("recommender.html", title="Recommender", form=form)


@app.route("/recommend_users")
@login_required
def recommend_users():
    if current_user.ratings:
        user_ratings = {}
        for rating_object in current_user.ratings:
            user_ratings[rating_object.game.title] = rating_object.rating

        n_recommendations = 20
        # The following functions do not alter original dataframe
        common_recommendations, common_top5 = recommend_users_by_common_games(ubyi_norm_0, user_ratings, n_recommendations)
        similarity_recommendations, similarity_top5 = recommend_users_by_similarity(ubyi_norm_0, user_ratings, n_recommendations)

        # Store the recommendations and top5 values in the session
        session['common_recommendations'] = common_recommendations
        session['common_top5'] = common_top5
        session['similarity_recommendations'] = similarity_recommendations
        session['similarity_top5'] = similarity_top5
    else:
        flash("Please add games to your Gamer Profile first", "danger")
        return redirect(url_for("profile"))
    return render_template("recommend_users.html", title="Recommend Users", common_top5=common_top5, similarity_top5=similarity_top5)

# In order to make sure that recommended_users routes are accessed AFTER visiting recommend_users route,
# We make forms for each button for each route and use POST request to access these routes

@app.route("/recommended_users/common", methods=["POST"]) 
@login_required
def recommended_users_common():
    common_recommendations = session.get('common_recommendations')
    return render_template("recommended_users_common.html", title="Recommended Users", 
                           common_recommendations=common_recommendations)


@app.route("/recommended_users/similarity", methods=["POST"])
@login_required
def recommended_users_similarity():
    similarity_recommendations = session.get('similarity_recommendations')
    return render_template("recommended_users_similarity.html", title="Recommended Users", 
                           similarity_recommendations=similarity_recommendations)


@app.route("/get_recommended_names", methods=["GET"])
def get_recommended_names():
    return {"recommended_names": game_names}  


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: # where is_authenticated is property from inherited UserMixin class in User class 
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit(): # shortcut for `from.is_submitted() and form.validate()`. Check if it is a POST request and if form is valid. So you dont need to pass request.form
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success") # Store list of flash messages in custom session by flask
        return redirect(url_for("login"))
        
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged In", "success")
            next = request.args.get("next")
            return redirect(next if next else url_for("home"))           
        else:
            flash("Login Unsuccessful. Please check your email and password.", "danger")
        
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("account"))
    
    elif request.method == "GET":  # So that fields are not filled when form is invalidated on POST request
        form.username.data = current_user.username
        form.email.data = current_user.email

    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).all()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form, game_ratings=game_ratings)
    

@app.route("/profile", methods=["GET", "POST"])
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
        return redirect(url_for("account"))

    # Render the tempelate with values of game names and ratings inserted so that we could re submit them (after updating) in post request       
    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).all()
    return render_template("profile.html", title="Profile", game_ratings=game_ratings)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_message(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("login"))
    
    return render_template("reset_request.html", title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = User.verify_reset_token(token)
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success") 
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form = form)

