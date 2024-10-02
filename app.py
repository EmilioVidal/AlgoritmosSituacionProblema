import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Crear la aplicación Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Asegúrate de que la carpeta de subidas exista
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Definir rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No se ha seleccionado ningún archivo', 400

    file = request.files['file']

    if file.filename == '':
        return 'No hay archivo seleccionado', 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Obtener el botón seleccionado para aplicar el algoritmo
        algorithm = request.form.get('algorithm')

        # Dependiendo del algoritmo seleccionado
        if algorithm == 'algoritmo1':
            resultado = algoritmo1(filepath)
        elif algorithm == 'algoritmo2':
            resultado = algoritmo2(filepath)
        else:
            return 'Algoritmo no válido', 400

        return f"Resultado del {algorithm}: {resultado}"

# Algoritmos de ejemplo
def algoritmo1(filepath):
    # Leer el archivo y procesarlo
    with open(filepath, 'r') as file:
        contenido = file.read()
        # Ejemplo de procesamiento: contar líneas
        return f"Número de líneas: {len(contenido.splitlines())}"

def algoritmo2(filepath):
    # Leer el archivo y procesarlo
    with open(filepath, 'r') as file:
        contenido = file.read()
        # Ejemplo de procesamiento: contar palabras
        return f"Número de palabras: {len(contenido.split())}"

if __name__ == '__main__':
    app.run(debug=True)
