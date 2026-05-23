from flask import Blueprint
from services.ventas import crear_venta_service

ventas = Blueprint('ventas', __name__)

@ventas.route('/', methods=['POST'])
def crear_venta():
    return crear_venta_service()