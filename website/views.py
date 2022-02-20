# create standard routes

# from crypt import methods
from crypt import methods
from distutils.command.config import config
from flask import Blueprint, render_template, flash, request, request_started, session, url_for, redirect
from flask_login import login_required, current_user
import stripe
# added import for 'Items' table
from .models import Items


views = Blueprint('views', __name__)
stripe.api_key = 'sk_test_51KOEoTEAaICJ0GdRPRiVmPSZIQQ9DVtzWqeNtuevHa01p74QcR5wCNOrPdisWya0OheTal3B6kIy7Tuk987Cuk3l00n89yrf6y'


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html', user=current_user, items=get_items())

@views.route('/item/<int:id>', methods=['GET', 'POST'])
def item(id):
    return render_template('item.html', user=current_user, current_item=get_items()[id - 1])

# @views.route('/addcart', methods=['POST'])
# def addcart():
    
#     try:
#         item_id = request.form.get('item_id')
#         item = item.query.filter_by(id=item_id).first()
#         if item_id and request.method == "POST":
#             DictItems = {item_id: {}}
#             if 'Shoppingcart' in session:
#                 print(session['Shoppingcart'])
#                 if item_id in session['Shoppingcart']:
#                     flash("This product is in your cart already :)", 'info')
#                 else:
#                     session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
#                     return redirect(request.referrer) 
#             else:
#                 session['Shoppingcart'] = DictItems
#                 return redirect(request.referrer)
#     except Exception as e:
#         print(e)
#     finally:
#         return redirect(request.referrer)

@views.route('/cart', methods=['GET', 'POST'])
def getcart():
    if 'Shoppingcart' not in session:
        return render_template('cart.html', user=current_user)
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        grandtotal = subtotal
    return render_template('cart.html', user=current_user, grandtotal=grandtotal)

@views.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'Pizza',
        },
        'unit_amount': 1999,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='http://127.0.0.1:5000/successful', 
    cancel_url='http://127.0.0.1:5000/menu',
  )
    return redirect(session.url, code=303)


@views.route('/successful', methods=['GET', 'POST'])
def successful():
    return render_template('successful.html', user=current_user)


def get_items():
    ids = [1,2,3] # need a way to find how many items belong to table
    test_items = []
    for id in ids:
        item = Items.query.filter_by(id=id).first()
        grabber = {'id': 0, 'name': '', 'price': 0, 'desc': '', 'img': '', 'toppings': ['']}
        grabber['id'] = id
        grabber['name'] = item.name
        grabber['price'] = item.price
        grabber['desc'] = item.description
        grabber['img'] = item.item_image
        test_items.append(grabber)
    return test_items

# def MergeDicts(dict1, dict2):
#     if isinstance(dict1, list) and isinstance(dict2, list):
#         return dict1 + dict2
#     elif isinstance(dict1, dict) and isinstance(dict2,dict):
#         return dict(list(dict1.items()) + list(dict2.items()) )    
#     return False
