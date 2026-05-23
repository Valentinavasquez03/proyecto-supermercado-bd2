from flask import request
import database as dbase

db = dbase.dbConnection()

def crear_producto_service():

    data = request.get_json()

    nombre = data.get('nombre')
    precio = data.get('precio')
    stock = data.get('stock')

    if nombre and precio and stock:

        producto = {
            'nombre': nombre,
            'precio': precio,
            'stock': stock
        }

        response = db.productos.insert_one(producto)

        return {
            'id': str(response.inserted_id),
            'nombre': nombre,
            'precio': precio,
            'stock': stock
        }

    return {
        'mensaje': 'Datos inválidos'
    }, 400