# users_controller.py
from flask import Blueprint, abort, request, jsonify, render_template
from models import Usuario
from config.local import config
from utilities import verificar_contrasena
from authorize import authorize
import datetime

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Crea un Blueprint llamado 'users'
users_bp = Blueprint('users', __name__)

# Crear usuario
@users_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    list_errors = []
    returned_code = 201
    try:
        data = request.json

        if 'email' not in data:
            list_errors.append('email requerido')
        else:
            email = data.get('email')
            if Usuario.query.filter_by(email=email).first():
                list_errors.append('email ya está registrado')

        if 'nombre' not in data:
            list_errors.append('nombre requerido')
        else:
            nombre = data.get('nombre')

        if 'apellido' not in data:
            list_errors.append('apellido requerido')
        else:
            apellido = data.get('apellido')

        if 'role' not in data:
            list_errors.append('rol requerido')
        else:
            role = data.get('role')
            if role not in ('comprador', 'vendedor'):
                list_errors.append('rol no valido')

        if 'password' not in data:
            list_errors.append('contraseña requerida')
        else:
            password = data.get('password')
            password_hashed = generate_password_hash(password)

        if len(list_errors) > 0:
            returned_code = 400
        else:
            nuevo_usuario = Usuario(
                email=email, password=password_hashed, role=role, nombre=nombre, apellido=apellido)
            user_created_id = nuevo_usuario.insert()

            response = jsonify({
                'success': True,
                'user_created_id': user_created_id
            })

            login_user(nuevo_usuario)  # Loguear usuario automáticamente tras el registro

            return response, 201

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': list_errors,
            'message': 'Error creando un nuevo usuario'
        }), 400
    elif returned_code != 201:
        abort(returned_code)

# Iniciar sesión
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email y contraseña son requeridos'}), 400

        user = Usuario.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

    except Exception as e:
        print('e: ', e)
        return jsonify({'success': False, 'message': 'Error en el servidor'}), 500

# Cerrar sesión
@users_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'}), 200

# Obtener el perfil del usuario actual
@users_bp.route('/usuarios', methods=['GET'])
@login_required
def get_current_user():
    usuario = current_user
 
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'success': True, 'usuario': usuario.serialize()}), 200

# Actualizar el perfil del usuario
@users_bp.route('/usuarios', methods=['PATCH'])
@login_required
def update_user():
    usuario = current_user
    if not usuario:
        return jsonify({'error': 'Usuario no autorizado para editar este perfil'}), 403

    nombre_empresa = request.form.get('nombre_empresa')
    nombre_empresa = request.form.get('telefono')
    nombre_empresa = request.form.get('nombre_empresa')

    usuario_update_id = usuario.insert()  # Guardar los cambios en la base de datos

    return jsonify({'message': 'Perfil de usuario actualizado exitosamente', 'id': usuario_update_id}), 200


# Ruta protegida de ejemplo
@users_bp.route('/protected')
@login_required
def protected_route():
    return jsonify({'message': f'Hello user {current_user.id}!'}), 200



"""
@users_bp.route('/usuarios', methods=['PATCH'])
@login_required
def update_user():
    usuario = current_user
    if not usuario:
        return jsonify({'error': 'Usuario no autorizado para editar este perfil'}), 403

    data = request.json
    for key, value in data.items():
        # Verificar si el campo es editable (evitar modificar nombre y apellido)
        if key != 'nombre' and key != 'apellido':
            setattr(usuario, key, value)

    usuario_update_id = usuario.insert()  # Guardar los cambios en la base de datos

    return jsonify({'message': 'Perfil de usuario actualizado exitosamente', 'id': usuario_update_id}), 200


"""