from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Car
from flask_login import login_user, logout_user, login_required, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    lastname = request.form.get('lastname')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: #if a user is found, we want to redirect back to signup page so user can try again
        flash('E-mail adresa već postoji,')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, lastname=lastname,  password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    


    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Provjerite svoje korisničke podatke i pokušajte ponovo.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile_show'))

@auth.route('/profile', methods=["POST"])
@login_required
def cars_post():
    car_make = request.form.get('car_make')
    car_model = request.form.get('car_model')
    car_year = request.form.get('car_year')
    color = request.form.get('color')
    reg_plate = request.form.get('reg_plate')
   
    
    



    cars = Car.query.filter_by(reg_plate=reg_plate).first()
    db.session.query(Car.id).all()



    new_car = Car(car_make=car_make, car_model=car_model, car_year=car_year, color=color, reg_plate=reg_plate, user=current_user)

    if cars: #if a user is found, we want to redirect back to signup page so user can try again
        flash('Automobil s istom registracijom postoji u bazi.')
        return redirect(url_for('main.user_cars'))

    flash('Novi automovil je dodan u bazu podataka.')
    db.session.add(new_car)
    db.session.commit()

    return redirect(url_for('main.user_cars'))
