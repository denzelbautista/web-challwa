# main.py
from flask import Flask, request, jsonify, abort
import sys
from database import init_app, db
from config.local import config
from flask import Flask, send_file, render_template
import requests
# flask-login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# end flask-login
from models import Usuario, Comentario, Pedido, LineaPedido, Producto
from views import views_bp
from users_controller import users_bp

from authorize import authorize

app = Flask(__name__)
init_app(app)

app.config['SECRET_KEY'] = config['SECRET_KEY']

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

# Para la web

app.register_blueprint(views_bp)
app.register_blueprint(users_bp)

# Para la API

@app.route('/productos', methods=['POST'])
@login_required
def create_producto():
    usuario = current_user
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        categoria = request.form.get('categoria')
        stock = request.form.get('stock')

        # Verifica que los campos obligatorios estén presentes
        if not (nombre and descripcion and precio and categoria and stock):
            return jsonify({'success': False, 'message': 'Campos obligatorios faltantes'}), 400

        # Verifica que se haya subido una imagen
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'Imagen es obligatoria'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se ha seleccionado ninguna imagen'}), 400

        # Subimos la imagen al servicio de imgBB y obtenemos el nombre del archivo
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            data={'key': '2adc25aee373fb46c2d721f17defe3d4'},  # Reemplaza con tu clave de API de imgBB
            files={'image': file}
        )

        if response.status_code != 200:
            return jsonify({'success': False, 'message': 'Error subiendo la imagen'}), 500

        image_url = response.json()['data']['display_url']

        # Crea un nuevo producto con el user_created_id del token
        nuevo_producto = Producto(
            nombre=nombre, descripcion=descripcion, precio=precio,
            categoria=categoria, stock=stock, vendedor_id=usuario.id, imagen_producto=image_url
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Producto creado correctamente', 'id': nuevo_producto.id}), 201
    except Exception as e:
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error creando producto'}), 500
    finally:
        db.session.close()

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        productos = Producto.query.all()
        productos_list = []
        for producto in productos:
            productos_list.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'categoria': producto.categoria,
                'stock': producto.stock,
                'imagen_producto': producto.imagen_producto  # Asegúrate de que el campo imagen exista y contenga la URL
            })
        return jsonify({'success': True, 'productos': productos_list}), 200
    except Exception as e:
        print(sys.exc_info())
        return jsonify({'success': False, 'message': 'Error obteniendo productos'}), 500



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
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

"""
