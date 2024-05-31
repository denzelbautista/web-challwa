# views.py
from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required, current_user
# Crea un Blueprint llamado 'views'
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/shop')
def shop():
    return render_template('shop.html')

@views_bp.route('/contact')
def contact():
    return render_template('contact.html')

@views_bp.route('/sell')
def sell():
    return render_template('sell.html')

@views_bp.route('/fishes')
def fishes():
    return render_template('fishes.html')

@views_bp.route('/register')
def register():
    return render_template('register.html')

@views_bp.route('/login')
def login():
    return render_template('login.html')

@views_bp.route('/productos')
def productos():
    return render_template('productos.html')

