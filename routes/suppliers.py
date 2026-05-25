from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson import ObjectId
import database as dbase

suppliers_bp = Blueprint('suppliers', __name__)

# --- HU07: REGISTRAR PROVEEDORES ---
@suppliers_bp.route('/suppliers/new', methods=['GET', 'POST'])
def create_supplier():
    if request.method == 'POST':
        db = dbase.dbConnection()

        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        email = request.form.get('email', '').strip()
        direccion = request.form.get('direccion', '').strip()
        categoria = request.form.get('categoria', '').strip()

        if not nombre or not telefono or not email or not categoria:
            flash("Error: Los campos con asterisco son obligatorios.", "danger")
            return redirect(url_for('suppliers.create_supplier'))

        if db is not None:
            db['proveedores'].insert_one({
                "nombre": nombre,
                "telefono": telefono,
                "email": email,
                "direccion": direccion,
                "categoria": categoria
            })
            flash("Proveedor registrado correctamente.", "success")
        else:
            flash("Error: Base de datos no disponible.", "danger")

        return redirect(url_for('suppliers.create_supplier'))

    return render_template('create_supplier.html')


# --- LISTAR PROVEEDORES ---
@suppliers_bp.route('/suppliers', methods=['GET'])
def list_suppliers():
    db = dbase.dbConnection()
    proveedores = []
    if db is not None:
        proveedores = list(db['proveedores'].find())
    return render_template('list_suppliers.html', proveedores=proveedores)