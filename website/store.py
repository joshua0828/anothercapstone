from multiprocessing.sharedctypes import Value
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Store, Employee, Cart
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
# this is why user mixin needed to be added to user model
from flask_login import login_user, login_required, logout_user, current_user
from .menu import get_items, get_options, get_stores, get_employees

store = Blueprint('store', __name__)

@store.route('/edit-employees', methods=['POST', 'GET'])
def edit_employees():
  # if store adds a new employee
  if request.method == 'POST':
    email = request.form.get('email')
    phone = request.form.get('phone')
    first_name = request.form.get('first_name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    # search table by email entered
    employee = Employee.query.filter_by(email=email).first()
    # check if email is already inside of table and all info meets requirements below
    if employee:
      # if it is flask this message
      flash('Email already exists.', category='error')
    elif len(email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(first_name) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
      flash('Password must be at least 7 characters.', category='error')
    else:
      # create new user by passing data into variable called 'new_employee'
      new_employee = Employee(email=email,
      first_name=first_name,
      phone=phone,
      password=generate_password_hash(password1, method='sha256'))
      # pass new_employee into database
      db.session.add(new_employee)
      # save database with new_employee passed
      db.session.commit()
      flash('Employee created!', category='success')
      return redirect(url_for('store.edit_employees'))
      # end of post request
  # rows to track cart quantity
  rows = Cart.query.filter(Cart.id).count()
  return render_template('editemployees.html', user=current_user, account=get_employees(), rows=rows)

@store.route('/remove_employee/<int:id>')
def remove_employee(id):
  option_to_delete = Employee.query.get_or_404(id)
  try:
    db.session.delete(option_to_delete)
    db.session.commit()
    
    # reassign ids so there in a good order
    ids = [id[0] for id in Employee.query.with_entities(Employee.id).all()] # fixed
    new_id = 1
    for i in ids:
      _id = Employee.query.get(i)
      _id.id = new_id
      new_id += 1
      db.session.commit()

    flash('Employee removed')
    return redirect(url_for('store.edit_employees'))
  except:
    flash('Problem removing Employee')
    return redirect(url_for('store.edit_employees'))

@store.route('/current-orders', methods=['POST', 'GET'])
def current_orders():
  return render_template('currentorders.html', user=current_user)