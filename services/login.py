from flask import request
import database as dbase

db = dbase.dbConnection()

def login_service():

    data = request.get_json()

    usuario = data.get('usuario')
    password = data.get('password')

    usuario_encontrado = db.usuarios.find_one({
        'usuario': usuario,
        'password': password
    })

    if usuario_encontrado:

        return {
            'mensaje': 'Inicio de sesión exitoso'
        }, 200

    return {
        'mensaje': 'Usuario o contraseña incorrectos'
    }, 401