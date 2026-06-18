from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase
from bson.objectid import ObjectId

products_bp = Blueprint('products', __name__)

# --- REGISTRAR PRODUCTOS (HU02) ---
@products_bp.route('/products/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        db = dbase.dbConnection()
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio_raw = request.form.get('precio')
        stock_raw = request.form.get('stock')
        categoria = request.form.get('categoria')
        imagen = request.form.get('imagen', '').strip()

        if not nombre or not precio_raw or not stock_raw or not categoria:
            flash("Error: Los campos con asterisco son obligatorios.", "danger")
            return redirect(url_for('products.create_product'))

        if not imagen:
            imagen = "https://via.placeholder.com/150?text=Sin+Imagen"

        precio = float(precio_raw)
        stock = int(stock_raw)

        if db is not None:
            db['productos'].insert_one({
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria": categoria,
                "imagen": imagen
            })
            flash("Producto guardado correctamente.", "success")
        else:
            flash("Error: Base de datos no disponible.", "danger")

        return redirect(url_for('products.create_product'))

    return render_template('create_product.html')


# --- BUSCAR Y LISTAR PRODUCTOS (HU05) ---
@products_bp.route('/products/search', methods=['GET'])
def search_products():
    db = dbase.dbConnection()
    query_nombre = request.args.get('nombre', '').strip()
    query_categoria = request.args.get('categoria', '').strip()
    productos_encontrados = []
    
    if db is not None:
        filtro = {}
        if query_nombre:
            filtro['nombre'] = {'$regex': query_nombre, '$options': 'i'}
        if query_categoria:
            filtro['categoria'] = query_categoria
            
        productos_encontrados = list(db['productos'].find(filtro))
        
    return render_template('search_product.html', productos=productos_encontrados, q_nombre=query_nombre, q_categoria=query_categoria)


# --- CONFIRMAR Y ELIMINAR PRODUCTO (HU06) ---
@products_bp.route('/products/<string:id>/delete', methods=['GET', 'POST'])
def delete_product(id):
    db = dbase.dbConnection()
    if db is None:
        flash("Error: Base de datos no disponible.", "danger")
        return redirect(url_for('products.search_products'))

    # Buscar el producto específico en MongoDB para mostrar sus datos en la confirmación
    producto = db['productos'].find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        # Eliminar definitivamente al presionar el botón del formulario
        db['productos'].delete_one({"_id": ObjectId(id)})
        flash("Producto eliminado correctamente.", "success")
        return redirect(url_for('products.search_products'))

    return render_template('delete_confirm.html', producto=producto)


# --- APLICAR DESCUENTOS (HU09) ---
@products_bp.route('/products/<string:id>/discount', methods=['POST'])
def apply_discount(id):
    db = dbase.dbConnection()
    porcentaje_raw = request.form.get('porcentaje')

    if db is not None and porcentaje_raw:
        porcentaje = float(porcentaje_raw)
        if porcentaje <= 0 or porcentaje > 100:
            flash("Error: El porcentaje de descuento no es válido.", "danger")
            return redirect(url_for('products.search_products'))

        producto = db['productos'].find_one({"_id": ObjectId(id)})
        if producto:
            # Calcular el nuevo precio rebajado
            precio_actual = producto['precio']
            nuevo_precio = round(precio_actual * (1 - (porcentaje / 100)), 2)

            # Actualizar en la base de datos
            db['productos'].update_one(
                {"_id": ObjectId(id)},
                {"$set": {"precio": nuevo_precio}}
            )
            flash(f"Descuento del {int(porcentaje)}% aplicado con éxito.", "success")

    return redirect(url_for('products.search_products'))