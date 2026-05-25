from flask import Flask, render_template, redirect, url_for
import database as dbase

app = Flask(__name__)
# Clave obligatoria para sesiones y mensajes informativos
app.secret_key = "clave_secreta_compartida_supermercado"

# Conexion global a la base de datos
db = dbase.dbConnection()


# =================================================================
# SECCIÓN DE REGISTRO DE BLUEPRINTS (Aquí integramos tus rutas)
# =================================================================
from routes.products import products_bp
app.register_blueprint(products_bp)

from routes.suppliers import suppliers_bp
app.register_blueprint(suppliers_bp)



# Ruta raíz: Al entrar a http://127.0.0.1:5000 te mandará directo al registro
@app.route('/')
def home():
    return redirect(url_for('products.create_product'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)