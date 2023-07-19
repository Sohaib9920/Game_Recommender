from game_recommender import app
from flask import request, render_template, url_for, flash, redirect
from game_recommender.forms import RegistrationForm, LoginForm
from game_recommender import ubyi_norm_0, als, game_names, FAVOURITE_RATING
from game_recommender.recommend import recommend_games


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_ratings = {}
        for i in range(1, 6): 
            game_name = request.form.get(f"game{i}_name")
            if game_name in game_names:
                user_ratings[game_name] = FAVOURITE_RATING
        
        recommendations = recommend_games(ubyi_norm_0, user_ratings, als)

        return render_template("recommendations.html",title="Recommendations", recommendations=recommendations)
    
    return render_template("index.html", title="Recommender")


@app.route("/get_recommended_names", methods=["GET"])
def get_recommended_names():
    game_names = ubyi_norm_0.columns.values
    return {"recommended_names": game_names.tolist()}  


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # shortcut for `from.is_submitted() and form.validate()`. Check if it is a POST request and if form is valid. So you dont need to pass request.form
        flash(f"Account created for {form.username.data}!", "success") # Store list of flash messages in session at key: "_flashes"
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)