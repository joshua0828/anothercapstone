# create standard routes
# contains:
# 1. home function (home.html)
# 2. successful function (successful.html)

from flask import Blueprint, render_template
from flask_login import current_user
from .models import Cart


# this is our blueprint for views. this also needs to be declared in init
views = Blueprint('views', __name__)

# this is our function for home.html it holds all python code needed in order to properly display the page
@views.route('/')
def home():
  # find the number of items in cart
  rows = Cart.query.filter(Cart.id).count()
  return render_template("home.html", user=current_user, rows=rows)

# this is our function for successful.html it holds all python code needed in order to properly display the page
# this function needs a lot of work as this page will contain much more information.
@views.route('/successful')
def successful():
  # find the number of items in cart
  rows = Cart.query.filter(Cart.id).count()
  return render_template('successful.html', user=current_user, rows=rows)

