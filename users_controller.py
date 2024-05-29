# views.py
from flask import Blueprint, abort, request, jsonify, session
from models import Usuario
from config.local import config
from utilities import verificar_contrasena
from authorize import authorize
import jwt
import datetime

# Crea un Blueprint llamado 'users'
users_bp = Blueprint('users', __name__)


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
            if not verificar_contrasena(password):
                list_errors.append('contraseña no cumple con los requisitos')

        if len(list_errors) > 0:
            returned_code = 400
        else:
            nuevo_usuario = Usuario(
                email=email, password=password, role=role, nombre=nombre, apellido=apellido)
            user_created_id = nuevo_usuario.insert()

            token = jwt.encode({
                'user_created_id': user_created_id,
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], config['ALGORYTHM'])

            response = jsonify({
                'success': True,
                'token': token,
                'user_created_id': user_created_id,
            })
            response.set_cookie('token', token)
            return response

    except Exception as e:
        print('e: ', e)
        returned_code = 500

    if returned_code == 400:
        return jsonify({
            'success': False,
            'errors': list_errors,
            'message': 'Error creando un nuevo usuario'
        })
    elif returned_code != 201:
        abort(returned_code)



@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email y contraseña son requeridos'}), 400

        user = Usuario.query.filter_by(email=email).first()

        if user and user.password == password:
            token = jwt.encode({
                'user_created_id': user.id,
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
            }, config['SECRET_KEY'], algorithm=config['ALGORYTHM'])

            response = jsonify({'success': True, 'token': token})
            response.set_cookie('token', token)
            return response
        else:
            return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

    except Exception as e:
        print('e: ', e)
        return jsonify({'success': False, 'message': 'Error en el servidor'}), 500



@users_bp.route('/protected')
@authorize
def protected_route(user_created_id):
    return jsonify({'message': f'Hello user {user_created_id}!'}), 200


@users_bp.route('/logout', methods=['GET'])
@authorize
def logout(user_created_id):
    # Limpiar la sesión del servidor (opcional)
    session.clear()

    # Crear una respuesta JSON para enviar al cliente
    response = jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'})

    # Eliminar la cookie del token
    response.delete_cookie('token')

    return response
