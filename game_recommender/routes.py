from flask import request, render_template, url_for, flash, redirect, session
from game_recommender import app, db, bcrypt, ubyi_norm_0, als, game_names, FAVOURITE_RATING
from game_recommender.forms import RecommenderForm, RegistrationForm, LoginForm, UpdateAccountForm
from game_recommender.models import User, Rating, Game
from game_recommender.recommend import recommend_games
from flask_login import login_user, logout_user, login_required, current_user
from game_recommender.utils import save_picture
from game_recommender.recommend_users import recommend_users_by_common_games, recommend_users_by_similarity


@app.route("/", methods=["GET", "POST"])
def home():
    form = RecommenderForm()
    if form.validate_on_submit():
        user_ratings = {}
        for i in range(5): 
            game_name = form.games[i].data.strip() # must strip as js validation ignore trailing spaces and allow these values in payload
            user_ratings[game_name] = FAVOURITE_RATING # JavaScript is used to validate valid names and avoid duplicates.

        recommendations = recommend_games(ubyi_norm_0, user_ratings, als)
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
        common_recommendations, common_top3 = recommend_users_by_common_games(ubyi_norm_0, user_ratings, n_recommendations)
        similarity_recommendations, similarity_top3 = recommend_users_by_similarity(ubyi_norm_0, user_ratings, n_recommendations)

        # Store the recommendations and top3 values in the session
        session['common_recommendations'] = common_recommendations
        session['common_top3'] = common_top3
        session['similarity_recommendations'] = similarity_recommendations
        session['similarity_top3'] = similarity_top3
    else:
        session['common_recommendations'] = None
        session['common_top3'] = None
        session['similarity_recommendations'] = None
        session['similarity_top3'] = None

    return render_template("recommend_users.html", title="Recommended Users")


@app.route("/recommended_users/common")
@login_required
def recommended_users_common():
    common_recommendations = session.get('common_recommendations')
    common_top3 = session.get('common_top3')

    return render_template("recommended_users_common.html", title="Recommended Users", 
                           common_recommendations=common_recommendations, common_top3=common_top3)


@app.route("/recommended_users/similarity")
@login_required
def recommended_users_similarity():
    similarity_recommendations = session.get('similarity_recommendations')
    similarity_top3 = session.get('similarity_top3')

    return render_template("recommended_users_similarity.html", title="Recommended Users", 
                           similarity_recommendations=similarity_recommendations, similarity_top3=similarity_top3)


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

    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).limit(10).all()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form, game_ratings=game_ratings)
    

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # Instead of quering database for each game name to get game object, query single time and store the result in {game name: game object}
        game_mapping = {game_object.title : game_object for game_object in Game.query.all()}

        # It is easier to initailly remove all the ratings of user and then re-add them at once after both updating existing games and inserting new games
        current_user.ratings = []

        for key, value in request.form.items():
            if key.startswith("games-"):
                game_name = value.strip() # must be striped as JS validation allows unstriped value of game name
                rating = int(request.form.get(f"ratings-{key.split('-')[1]}")) # make sure that the rating is integer
                
                print(f'-{game_name}-')
                print(type(rating))

                # Add new ratings objects to user
                game_object = game_mapping.get(game_name) # JS validation makes sure that game_object for input game name exits
                rating_object = Rating(user = current_user, game = game_object, rating = rating)
                db.session.add(rating_object)
        
        db.session.commit()
        return redirect(url_for("profile"))

    # Render the tempelate with values of game names and ratings inserted so that we could re submit them (after updating) in post request       
    game_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.rating.desc()).all()
    return render_template("profile.html", title="Profile", game_ratings=game_ratings)



