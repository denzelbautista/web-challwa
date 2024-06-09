# views.py
from flask import Blueprint, render_template, request
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

@views_bp.route('/comprar')
def sell():
    return render_template('comprar.html')

@views_bp.route('/carrito')
def carrito():
    return render_template('carrito.html')

@views_bp.route('/register')
def register():
    return render_template('register.html')

@views_bp.route('/login')
def login():
    return render_template('login.html')

@views_bp.route('/detallesproducto')
def detallesproducto():
    product_id = request.args.get('id')
    return render_template('detallesproducto.html', product_id=product_id)

@views_bp.route('/registroproducto')
@login_required
def registroproducto():
    return render_template('registroproducto.html')

@views_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
