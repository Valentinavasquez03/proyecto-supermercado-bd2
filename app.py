from flask import Flask, render_template, redirect, url_for
import database as dbase

app = Flask(__name__)

app.secret_key = "clave_secreta_compartida_supermercado"

db = dbase.dbConnection()


# =================================================================
# SECCIÓN DE REGISTRO DE BLUEPRINTS (Espacio para el equipo)
# Cada integrante importará y registrará sus rutas aquí abajo:
# =================================================================
from routes.products import products_bp
app.register_blueprint(products_bp)


@app.route('/')
def home():
  
    return redirect(url_for('products.create_product'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)