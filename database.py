# database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///challwa.db'
    db.init_app(app)

    with app.app_context():
            db.create_all()  # Crea las tablas si no existen