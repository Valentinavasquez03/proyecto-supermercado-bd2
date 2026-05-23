from flask import Flask, render_template
import database as dbase

app = Flask(__name__)
# Clave obligatoria en Flask para habilitar sesiones y mensajes flash informativos
app.secret_key = "clave_secreta_compartida_supermercado"

# Inicialización de la Base de Datos global para el grupo
db = dbase.dbConnection()


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