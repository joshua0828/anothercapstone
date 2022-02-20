from cgi import test
from flask import Blueprint, render_template, flash, session, url_for, redirect
from flask_login import login_required, current_user

def get_items():
    test_items = [
        {id: 1, 'name': 'Pepperoni', 'price': 9.99},
        {id: 2, 'name': 'Veggie', 'price': 10.99}
    ]

    return test_items