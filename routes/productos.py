from flask import Blueprint
from services.productos import crear_producto_service

productos = Blueprint('productos', __name__)

@productos.route('/', methods=['POST'])
def crear_producto():
    return crear_producto_service()