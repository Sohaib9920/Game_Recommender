from flask import request, render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from game_recommender import app, db, bcrypt
from game_recommender.user_authentication.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm
from game_recommender.models import User
from game_recommender.user_authentication.utils import send_reset_message
import threading


user_authentication = Blueprint("user_authentication", __name__)

@user_authentication.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: # where is_authenticated is property from inherited UserMixin class in User class 
        return redirect(url_for("recommend_games.home"))
    form = RegistrationForm()
    if form.validate_on_submit(): # shortcut for `from.is_submitted() and form.validate()`. Check if it is a POST request and if form is valid. So you dont need to pass request.form
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success") # Store list of flash messages in custom session by flask
        return redirect(url_for("user_authentication.login"))
        
    return render_template("user_authentication/register.html", title="Register", form=form)


@user_authentication.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("recommend_games.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged In", "success")
            next = request.args.get("next")
            return redirect(next if next else url_for("recommend_games.home"))           
        else:
            flash("Login Unsuccessful. Please check your email and password.", "danger")
        
    return render_template("user_authentication/login.html", title="Login", form=form)


@user_authentication.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("recommend_games.home"))


@user_authentication.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("recommend_games.home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        url = url_for("user_authentication.reset_token", token=token, _external=True)
        # Using threading to send email asynchronously and avoid timeout error
        email_thread = threading.Thread(target=send_reset_message, args=(user, url, app))
        email_thread.start()
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("user_authentication.login"))
    
    return render_template("user_authentication/reset_request.html", title="Reset Password", form=form)

@user_authentication.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = User.verify_reset_token(token)
    if current_user.is_authenticated:
        return redirect(url_for("recommend_games.home"))
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('user_authentication.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success") 
        return redirect(url_for("user_authentication.login"))
    return render_template("user_authentication/reset_token.html", title="Reset Password", form = form)