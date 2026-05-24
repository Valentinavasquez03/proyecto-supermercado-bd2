from flask import Flask, render_template
import database as dbase
from routes.productos import productos
from routes.ventas import ventas
from routes.login import login
# Clave obligatoria en Flask para habilitar sesiones y mensajes flash informativos
app = Flask(__name__)


# Inicialización de la Base de Datos global para el grupo
db = dbase.dbConnection()

app.secret_key = "clave_secreta_compartida_supermercado"

app.register_blueprint(productos, url_prefix='/productos')
app.register_blueprint(ventas, url_prefix='/ventas')
app.register_blueprint(login, url_prefix='/login')
# =================================================================
# SECCIÓN DE REGISTRO DE BLUEPRINTS
# Cada integrante importará y registrará sus rutas aquí abajo:
# Ejemplo de HU02:
# from routes.products import products_bp
# app.register_blueprint(products_bp)
# =================================================================


# Ruta raíz neutra para dar la bienvenida al sistema
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)