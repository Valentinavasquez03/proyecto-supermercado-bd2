from flask import request
import database as dbase

db = dbase.dbConnection()

def crear_venta_service():

    data = request.get_json()

    producto = data.get('producto')
    cantidad = data.get('cantidad')
    total = data.get('total')

    if producto and cantidad and total:

        venta = {
            'producto': producto,
            'cantidad': cantidad,
            'total': total
        }

        response = db.ventas.insert_one(venta)

        return {
            'id': str(response.inserted_id),
            'producto': producto,
            'cantidad': cantidad,
            'total': total
        }

    return {
        'mensaje': 'Datos inválidos'
    }, 400