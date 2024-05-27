# main.py
from flask import Flask, request, jsonify, abort
import sys
from database import init_app, db
from flask import Flask, send_file, render_template

from models import Usuario, Comentario, Pedido, LineaPedido, Producto
from views import views_bp
from users_controller import users_bp

app = Flask(__name__)
init_app(app)

# Para la web

app.register_blueprint(views_bp)
app.register_blueprint(users_bp)

# Para la API


@app.route('/usuarios/<string:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    try:
        # Busca el usuario en la base de datos por su ID
        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

        # Serializa los datos del usuario
        usuario_serializado = usuario.serialize()

        return jsonify({'success': True, 'usuario': usuario_serializado}), 200
    except Exception as e:
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error al obtener el usuario'}), 500


@app.route('/productos', methods=['POST'])
def create_producto():
    try:
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        categoria = data.get('categoria')
        stock = data.get('stock')
        # Asegúrate de que este campo esté presente en el JSON
        vendedor_id = data.get('vendedor_id')

        # Verifica que los campos obligatorios estén presentes
        if not (nombre and descripcion and precio and categoria and stock and vendedor_id):
            return jsonify({'success': False, 'message': 'Campos obligatorios faltantes'}), 400

        # Crea un nuevo producto
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio,
                                  categoria=categoria, stock=stock, vendedor_id=vendedor_id)
        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pedido creado correctamente', 'id': nuevo_producto.id}), 201
    except Exception as e:
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error creando producto'}), 500
    finally:
        db.session.close()


@app.route('/productos/<producto_id>', methods=['GET'])
def get_producto(producto_id):
    try:
        # Verifica que el ID sea positivo
        if producto_id <= 0:
            return jsonify({'success': False, 'message': 'ID de producto no válido'}), 400

        # Busca el producto por ID
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404

        # Devuelve los detalles del producto
        return jsonify({'success': True, 'producto': producto.serialize()}), 200
    except Exception as e:
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error al obtener el producto'}), 500


@app.route('/pedidos', methods=['POST'])
def create_pedido():
    try:
        data = request.json
        # Extrae los campos necesarios del JSON

        # Crea un nuevo pedido
        nuevo_pedido = Pedido(...)  # Completa con los campos adecuados
        db.session.add(nuevo_pedido)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pedido creado correctamente'}), 201
    except Exception as e:
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error creando pedido'}), 500
    finally:
        db.session.close()


@app.route('/pedidos/<string:pedido_id>/lineas_pedido', methods=['POST'])
def create_linea_pedido(pedido_id):
    try:
        data = request.json
        # Extrae los campos necesarios del JSON

        # Verifica si el pedido existe
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            return jsonify({'success': False, 'message': 'Pedido no encontrado'}), 404

        # Crea una nueva línea de pedido
        # Completa con los campos adecuados
        nueva_linea_pedido = LineaPedido(...)
        db.session.add(nueva_linea_pedido)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Línea de pedido creada correctamente'}), 201
    except Exception as e:
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error creando línea de pedido'}), 500
    finally:
        db.session.close()


if __name__ == '__main__':
    app.run(debug=True)


"""
def fibo(n):
    if n == 0 or n == 1:
        return n
    else: 
        return fibo(n-1) + fibo(n-2)

@app.route('/fibonacci/<number>',methods=['GET'])
def get_nth_fibonacci(number):

    num = int(number)

    def fibo(n):
        if n == 0 or n == 1:
            return n
        else: 
            return fibo(n-1) + fibo(n-2)
         
    result = fibo(num)
        
    return jsonify({f'fibo for {num} is :':result})
"""
