from flask import request, render_template, url_for, flash, redirect
from game_recommender import app, db, bcrypt, ubyi_norm_0, als, game_names, FAVOURITE_RATING
from game_recommender.forms import RecommenderFrom, RegistrationForm, LoginForm, UpdateAccountForm
from game_recommender.models import User, Rating
from game_recommender.recommend import recommend_games
from flask_login import login_user, logout_user, login_required, current_user
from game_recommender.utils import save_picture


@app.route("/", methods=["GET", "POST"])
def home():
    form = RecommenderFrom()
    if form.validate_on_submit():
        user_ratings = {}
        for i in range(5): 
            game_name = form.games[i].data.strip()  # OR: request.form.get(f"games-{i}").strip()
            user_ratings[game_name] = FAVOURITE_RATING # JavaScript is used to validate valid names and avoid duplicates.

        recommendations = recommend_games(ubyi_norm_0, user_ratings, als)
        return render_template("recommendations.html", title="Recommendations", recommendations=recommendations)
    
    return render_template("recommender.html", title="Recommender", form=form)


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
        flash("Your account has been created! You are now able to log in", "success") # Store list of flash messages in session at key: "_flashes"
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
    

@app.route("/profile/new", methods=["GET", "POST"])
@login_required
def new_profile():
    pass