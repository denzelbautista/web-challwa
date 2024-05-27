# models.py
from database import db
import uuid
import sys
from datetime import datetime

def current_time():
    return datetime.now().isoformat()

"""
# modelo de ejemplo 
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True) # para uuid
    email = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

"""

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), primary_key=True, default=lambda:str(uuid.uuid4()), unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('comprador', 'vendedor', name='user_roles'), nullable=False)
    # opcionales al momento de envio o editables en otro momento
    nombre_empresa = db.Column(db.String, nullable=True)
    telefono = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    nombre = db.Column(db.String, nullable=True)
    apellido = db.Column(db.String, nullable=True)
    direccion_envio = db.Column(db.String, nullable=True)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con otras tablas
    productos = db.relationship('Producto', back_populates='vendedor')
    pedidos = db.relationship('Pedido', back_populates='comprador')
    comentarios = db.relationship('Comentario', back_populates='usuario')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido' : self.apellido,
            'email': self.email,
            'role' : self.role
        }
    
    def __init__(self, email, password, nombre, apellido, role):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
    
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

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.Enum('pescado', 'marisco', 'accesorios_nauticos', 'equipos_de_pesca', 'ropa_accesorios', name='product_categories'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con las otras tablas
    vendedor = db.relationship('Usuario', back_populates='productos')
    lineas_pedido = db.relationship('LineaPedido', back_populates='producto')
    comentarios = db.relationship('Comentario', back_populates='producto')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),  # Convertir a float si es necesario
            'categoria' : self.categoria.value,
            'stock' : self.stock,
            'vendedor_id' : self.vendedor_id
        }

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'en_proceso', 'completado', 'cancelado', name='order_status'), nullable=False)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con las otras tablas
    comprador = db.relationship('Usuario', back_populates='pedidos')
    lineas_pedido = db.relationship('LineaPedido', back_populates='pedido')

    def serialize(self):
        return {
            'id': self.id,
            'comprador_id': self.comprador_id,
            'total': float(self.total),  # Convertir a float si es necesario
            'estado': self.estado.value
        }

class LineaPedido(db.Model):
    __tablename__ = 'lineas_pedido'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    # fechas
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)
    # relaciones con las otras tablas
    pedido = db.relationship('Pedido', back_populates='lineas_pedido')
    producto = db.relationship('Producto', back_populates='lineas_pedido')

    def serialize(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),  # Convertir a float si es necesario
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
