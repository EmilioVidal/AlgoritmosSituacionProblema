from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variables globales para almacenar el contenido de los archivos
file1_content = None
file2_content = None

@app.route('/')
def index():
    # Renderizar la plantilla con el contenido de ambos archivos
    return render_template('index.html', content1=file1_content, content2=file2_content)

# Ruta para subir el primer archivo
@app.route('/upload_file1', methods=['POST'])
def upload_file1():
    global file1_content
    if 'file1' in request.files:
        file = request.files['file1']
        if file.filename != '':
            file1_content = file.read().decode('utf-8')
    return redirect(url_for('index'))

# Ruta para subir el segundo archivo
@app.route('/upload_file2', methods=['POST'])
def upload_file2():
    global file2_content
    if 'file2' in request.files:
        file = request.files['file2']
        if file.filename != '':
            file2_content = file.read().decode('utf-8')
    return redirect(url_for('index'))

# Ruta para aplicar un algoritmo al primer archivo
@app.route('/apply_algorithm_file1', methods=['POST'])
def apply_algorithm_file1():
    global file1_content, resultado
    if 'file1_content' in request.form:
        file1_content = request.form.get('file1_content')
        algorithm = request.form.get('algorithm')
        palindromo = request.form.get('palindromo')  # Recibir el patrón del palíndromo
        if algorithm == 'algoritmo1':
            file1_content = algoritmo_z_resaltar(file1_content, palindromo)
        elif algorithm == 'algoritmo2':
            file1_content = algoritmo_z_resaltar(file1_content)
    return redirect(url_for('index'))

# Ruta para aplicar un algoritmo al segundo archivo
@app.route('/apply_algorithm_file2', methods=['POST'])
def apply_algorithm_file2():
    global file2_content, resultado
    if 'file2_content' in request.form:
        file2_content = request.form.get('file2_content')
        algorithm = request.form.get('algorithm')
        palindromo = request.form.get('palindromo')  # Recibir el patrón del palíndromo
        if algorithm == 'algoritmo1':
            file2_content = algoritmo_z_resaltar(file2_content, palindromo)
        elif algorithm == 'algoritmo2':
            file2_content = algoritmo_z_resaltar(file2_content)
    return redirect(url_for('index'))

# Algoritmo Z para buscar y resaltar el patrón
def algoritmo_z_resaltar(texto, palindromo):
    # Función Z para encontrar posiciones de un patrón en el texto
    def Z(texto, palindromo):
        cadena_concatenada = palindromo + "$" + texto
        n = len(cadena_concatenada)
        Z = [0] * n
        L, R, K = 0, 0, 0
        for i in range(1, n):
            if i > R:
                L, R = i, i
                while R < n and cadena_concatenada[R] == cadena_concatenada[R - L]:
                    R += 1
                Z[i] = R - L
                R -= 1
            else:
                K = i - L
                if Z[K] < R - i + 1:
                    Z[i] = Z[K]
                else:
                    L = i
                    while R < n and cadena_concatenada[R] == cadena_concatenada[R - L]:
                        R += 1
                    Z[i] = R - L
                    R -= 1
        
        # Recoger las posiciones donde se encontró el patrón
        posiciones = []
        for i in range(len(palindromo) + 1, n):
            if Z[i] == len(palindromo):
                posiciones.append(i - len(palindromo) - 1)
        
        return posiciones

    # Encontrar todas las posiciones donde ocurre el palíndromo
    posiciones = Z(texto, palindromo)

    # Resaltar las ocurrencias del palíndromo con <span>
    texto_resaltado = ""
    ultimo_index = 0

    for pos in posiciones:
        texto_resaltado += texto[ultimo_index:pos]  # Añadir la parte antes de la coincidencia
        texto_resaltado += f"<span style='background-color: yellow;'>{texto[pos:pos + len(palindromo)]}</span>"  # Resaltar
        ultimo_index = pos + len(palindromo)

    # Añadir el resto del texto
    texto_resaltado += texto[ultimo_index:]
    
    return texto_resaltado

if __name__ == '__main__':
    app.run(debug=True)
