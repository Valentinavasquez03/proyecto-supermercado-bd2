from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase

products_bp = Blueprint('products', __name__)

# --- REGISTRAR PRODUCTOS (HU02 ampliada según enunciado) ---
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

        # Validación de campos obligatorios mínimos
        if not nombre or not precio_raw or not stock_raw or not categoria:
            flash("Error: Los campos con asterisco son obligatorios.", "danger")
            return redirect(url_for('products.create_product'))

        # Si no pone imagen, usamos una silueta por defecto como exige el enunciado
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
            flash("Producto guardado correctamente en el inventario.", "success")
        else:
            flash("Error: Base de datos no disponible.", "danger")

        return redirect(url_for('products.create_product'))

    return render_template('create_product.html')


# --- BUSCAR Y LISTAR PRODUCTOS (HU05 ampliada) ---
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