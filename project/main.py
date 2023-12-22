from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Reservation, Guest, Room
from datetime import date
from . import db
from .logic import convert_sql_to_kb, taste_combines, art_combines

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    reservations = Reservation.query.all()
    records = [{'id': r.id,
                'name': Guest.query.filter_by(id = r.guest_id).first().name, 
                'room': Room.query.filter_by(id = r.room_id).first().id, 
                'in': r.check_in, 
                'out': r.check_out, 
                'pay': r.payment
                } for r in reservations]
    
    guests = Guest.query.all()
    
    return render_template('profile.html', name=current_user.name, records=records, guests=guests)

@main.route('/create', methods=['POST'])
@login_required
def create_post():
    name = request.form.get('name')
    second_name = request.form.get('surname')
    room = int(request.form.get('room'))
    check_in = date.fromisoformat(request.form.get('in'))
    check_out = date.fromisoformat(request.form.get('out'))
    payment = int(request.form.get('payment'))

    room_map = [11, 12, 13, 14, 15,
                21, 22, 23, 24, 25,
                31, 32, 33, 34, 35]

    guest = Guest.query.filter_by(name = name, second_name = second_name).first()
    if ((not guest) 
        or (not check_in) 
        or (not check_out) 
        or (check_in > check_out) 
        or (room not in room_map)):
        flash('Please check your input data! There is error!')
        return redirect(url_for('main.profile'))
    
    new_reservation = Reservation(guest_id=guest.id, 
                                  room_id=room, 
                                  check_in=check_in, 
                                  check_out=check_out, 
                                  payment=payment)
    db.session.add(new_reservation)
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route('/add_guest', methods=['POST'])
@login_required
def add_guest_post():
    name = request.form.get('name')
    second_name = request.form.get('surname')
    alcohol = request.form.get('alcohol')
    spice = request.form.get('spice')
    color = request.form.get('color')
    music = request.form.get('music')

    if ((not name) or (not second_name)):
        flash('Please check your input data! Name is required!')
        return redirect(url_for('main.profile'))

    guest = Guest.query.filter_by(name = name, second_name = second_name).first()
    if (guest):
        flash('This guest already exists!')
        return redirect(url_for('main.profile'))
    
    guests = Guest.query.all()
    if ((not alcohol) or (not spice)):
        dataset = ((i.name, i.second_name, i.alcohol, i.spice, i.color, i.music) 
                   for i in guests)
        kb = convert_sql_to_kb(dataset)

        if ((not alcohol) and spice):
            alcohol = taste_combines(kb, spice)
            if alcohol[0] != 'No':
                alcohol = alcohol[0]['What'].capitalize()

        elif (alcohol and (not spice)):
            spice = taste_combines(kb, alcohol)
            if spice[0] != 'No':
                spice = spice[0]['What'].capitalize()
        else:
            flash('Not enough data to predict!')
            return redirect(url_for('main.profile'))
        
    if ((not color) or (not music)):
        dataset = ((i.name, i.second_name, i.alcohol, i.spice, i.color, i.music) 
                   for i in guests)
        kb = convert_sql_to_kb(dataset)

        if ((not color) and music):
            color = taste_combines(kb, music)
            if color[0] != 'No':
                color = color[0]['What'].capitalize()

        elif (color and (not music)):
            music = art_combines(kb, color)
            if music[0] != 'No':
                music = music[0]['What'].capitalize()
        else:
            flash('Not enough data to predict!')
            return redirect(url_for('main.profile'))
    
    new_guest = Guest(name=name, 
                      second_name=second_name,
                      alcohol=alcohol,
                      spice=spice,
                      color=color,
                      music=music)
    db.session.add(new_guest)
    db.session.commit()
    return redirect(url_for('main.profile'))