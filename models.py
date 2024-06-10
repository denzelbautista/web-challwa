# models.py
from database import db
import uuid
import sys
from datetime import datetime
from flask_login import UserMixin

def current_time():
    return datetime.now().isoformat()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('comprador', 'vendedor', name='user_roles'), nullable=False)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    # opcionales al momento de envio o editables en otro momento
    nombre_empresa = db.Column(db.String, nullable=True)
    telefono = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    direccion_envio = db.Column(db.String, nullable=True)
    imagen_usuario = db.Column(db.String(500), nullable=True)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con otras tablas
    productos = db.relationship('Producto', back_populates='vendedor')
    comentarios = db.relationship('Comentario', back_populates='usuario')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'role': self.role,
            'imagen_usuario': self.imagen_usuario,
            'telefono' : self.telefono,
            'descripcion' : self.descripcion ,
            'direccion_envio' :  self.direccion_envio,
            'nombre_empresa' : self.nombre_empresa
        }

    def __init__(self, email, password, nombre, apellido, role,telefono):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.role = role
        self.telefono = telefono

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            user_created_id = self.id
        except Exception as e:
            print(sys.exc_info())
            print('e: ', e)
            db.session.rollback()
        finally:
            db.session.close()
        return user_created_id
    

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.Enum('pescado', 'marisco', 'accesorios_nauticos', 'equipos_de_pesca', 'ropa_accesorios', name='product_categories'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    imagen_producto = db.Column(db.String(500), nullable=False)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con las otras tablas
    vendedor = db.relationship('Usuario', back_populates='productos')
    comentarios = db.relationship('Comentario', back_populates='producto')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),  # Convertir a float si es necesario
            'categoria' : self.categoria,
            'stock' : self.stock,
            'vendedor_id' : self.vendedor_id,
            'imagen_producto' : self.imagen_producto
        }

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con las otras tablas
    producto = db.relationship('Producto', back_populates='comentarios')
    usuario = db.relationship('Usuario', back_populates='comentarios')

    def serialize(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'usuario_id': self.usuario_id,
            'contenido': self.contenido
        }

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni_usuario = db.Column(db.String(50), nullable=False)
    productos = db.Column(db.Text, nullable=False)  # Almacena los ids de los productos comprados como una cadena separada por comas
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)