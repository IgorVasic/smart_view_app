from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from . import db
from .models import *


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile_show():
    return render_template('profile.html', name=current_user.name, lastname=current_user.lastname, email=current_user.email)
   

@main.route('/mycars')
@login_required
def user_cars():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    cars = user.cars
    return render_template('my_cars.html', cars=cars)

@main.route("/car/<int:car_id>/update", methods=['GET', 'POST'])
@login_required
def update_cars(car_id):
    cars = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        cars.car_make = request.form['car_make']
        cars.car_model = request.form['car_model']
        cars.car_year = request.form['car_year']
        cars.color = request.form['color']
        cars.reg_plate = request.form['reg_plate']
        flash('Podaci o vozilu su uspješno promjenjeni')
        return redirect(url_for('main.user_cars'))
    return render_template('updateMyCars.html', cars=cars)    
    