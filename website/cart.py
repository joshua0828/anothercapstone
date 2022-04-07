
from re import sub
from flask import Blueprint, render_template, flash, url_for, redirect, request, abort, jsonify
from flask_login import current_user

from website.views import successful
from website.store import create_order
from .models import Cart
from . import db
import stripe
from .getters import get_cart_items, total_price_items, getItemsInCart, get_discounts

cart = Blueprint('cart', __name__)
stripe.api_key = 'sk_test_51KOEoTEAaICJ0GdRPRiVmPSZIQQ9DVtzWqeNtuevHa01p74QcR5wCNOrPdisWya0OheTal3B6kIy7Tuk987Cuk3l00n89yrf6y'

@cart.route('/website-cart', methods=['GET', 'POST'])
def website_cart():
  tip = request.form.get('tipp') # get user tip input
  discount = request.form.get('discountt') # get user discount input
  
  total = 0
  subtotal = total_price_items()
  discountTotal = discountPrice(subtotal, get_discounts(), discount)

  
  #This if statement will check if the user input is an empty string or a none value. so that way the website doesn't crash.
  if tip == '' or tip == None:
    tip = 0
    total = subtotal
  else:
    total += subtotal + float(tip)

  #This if statement will check if the subtotal of the cart is more than $20 to apply the discount,
  # and also to check if the user input is an empty string or a none value.
  if subtotal >= 20:
    total -= discountTotal
  elif discount == '' or discount == None:
    total = subtotal
    discountTotal = 0


  return render_template('cart.html', user=current_user, item=get_cart_items(), rows=getItemsInCart(), total='{:,.2f}'.format(total), subtotal='{:,.2f}'.format(subtotal),
    tip='{:,.2f}'.format(float(tip)), discount = '{:,.2f}'.format(discountTotal))


@cart.route('/delete/<int:id>')
def delete(id):
  item_to_delete = Cart.query.get_or_404(id)
  try:
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Item removed from cart')
    return redirect(url_for('cart.website_cart'))
  except:
    flash('Problem removing item from cart')
    return redirect(url_for('cart.website_cart'))


@cart.route('/clearcart')
def clearcart():
  num_of_items_in_cart = [id[0] for id in Cart.query.with_entities(Cart.id).all()]
  for item in num_of_items_in_cart:
    item_to_delete = Cart.query.get_or_404(item)
    try:
      db.session.delete(item_to_delete)
      db.session.commit()
    except:
      flash('Problem removing ', item_to_delete.name, ' from cart.' )
  flash('All items removed from cart!')
  return redirect(url_for('cart.website_cart'))


@cart.route('/create-checkout-session', methods=['POST'])
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
    cancel_url='http://127.0.0.1:5000/website-cart',
  )
    create_order(get_cart_items(), current_user)
    return redirect(session.url, code=303)

def discountPrice(total, discounts, getDiscount):
  
  price_discounted = 0
  discountArray = []
  discountStr = []
  dis = 0

# This for loop will go through the discounts values inside the dict from getDiscount and save it
# to the discountArray[]
  for i in discounts:
    discountArray.append(i['discount_info'] )
# This for loop will create a new dict to store the discount and the string that the next
# for loop will use to compare the user input discount with the ones that this loop created.
  for num in discountArray:
    grabber = {'discount': 0, 'string': ''}
    grabber['discount'] = num
    grabber['string'] = str(num) + '%OFF'
    discountStr.append(grabber)
# This loop will go through the string of the discountStr array to compare the strings with the user input
  for j in discountStr:
    if j['string'] == getDiscount:
      dis = int(j['discount']) / 100
      price_discounted = total * dis


  return price_discounted