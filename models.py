# models.py
from database import db
import uuid
from datetime import datetime

def current_time():
    return datetime.now().isoformat()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

"""
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('comprador', 'vendedor', name='user_roles'), nullable=False)
    nombre_empresa = db.Column(db.String, nullable=True)
    telefono = db.Column(db.String, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    nombre = db.Column(db.String, nullable=True)
    apellido = db.Column(db.String, nullable=True)
    direccion_envio = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    productos = db.relationship('Producto', back_populates='vendedor')
    pedidos = db.relationship('Pedido', back_populates='comprador')
    comentarios = db.relationship('Comentario', back_populates='usuario')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            # ... otros campos relevantes ...
        }

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.Enum('pescado', 'marisco', 'accesorios_nauticos', 'equipos_de_pesca', 'ropa_accesorios', name='product_categories'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    vendedor = db.relationship('Usuario', back_populates='productos')
    lineas_pedido = db.relationship('LineaPedido', back_populates='producto')
    comentarios = db.relationship('Comentario', back_populates='producto')

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),  # Convertir a float si es necesario
            # ... otros campos relevantes ...
        }

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'en_proceso', 'completado', 'cancelado', name='order_status'), nullable=False)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    comprador = db.relationship('Usuario', back_populates='pedidos')
    lineas_pedido = db.relationship('LineaPedido', back_populates='pedido')

    def serialize(self):
        return {
            'id': self.id,
            'comprador_id': self.comprador_id,
            'total': float(self.total),  # Convertir a float si es necesario
            'estado': self.estado,
            # ... otros campos relevantes ...
        }

class LineaPedido(db.Model):
    __tablename__ = 'lineas_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    pedido = db.relationship('Pedido', back_populates='lineas_pedido')
    producto = db.relationship('Producto', back_populates='lineas_pedido')

    def serialize(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),  # Convertir a float si es necesario
            # ... otros campos relevantes ...
        }

class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.String, default=current_time)
    updated_at = db.Column(db.String, default=current_time, onupdate=current_time)

    producto = db.relationship('Producto', back_populates='comentarios')
    usuario = db.relationship('Usuario', back_populates='comentarios')

    def serialize(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'usuario_id': self.usuario_id,
            'contenido': self.contenido,
            # ... otros campos relevantes ...
        }

"""