from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase

# Crear el modulo independiente para los productos
products_bp = Blueprint('products', __name__)

@products_bp.route('/products/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        # Conectamos a la DB justo aqui
        db = dbase.dbConnection()

        # Recibir unicamente los datos esenciales sin imagen ni descripcion
        nombre = request.form.get('nombre', '').strip()
        precio_raw = request.form.get('precio')
        stock_raw = request.form.get('stock')
        categoria = request.form.get('categoria')

        # Validar campos obligatorios de la HU02
        if not nombre or not precio_raw or not stock_raw or not categoria:
            flash("Error: Los campos con asterisco son obligatorios.", "danger")
            return redirect(url_for('products.create_product'))

        precio = float(precio_raw)
        stock = int(stock_raw)

        # Guardar el documento en MongoDB de forma directa y limpia
        if db is not None:
            db['productos'].insert_one({
                "nombre": nombre,
                "precio": precio,
                "stock": stock,
                "categoria": categoria
            })
            flash("Producto guardado correctamente.", "success")
        else:
            flash("Error: Base de datos no disponible.", "danger")

        return redirect(url_for('products.create_product'))

    return render_template('create_product.html')