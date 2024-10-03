from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variables globales para almacenar el contenido de los archivos
file1_content = None
file2_content = None
highlighted_content = None

@app.route('/')
def index():
    # Renderizar la plantilla con el contenido de ambos archivos
    return render_template('index.html', content1=file1_content, content2=file2_content, highlighted_content=highlighted_content)

# Ruta para subir el primer archivo
@app.route('/upload_file1', methods=['POST'])
def upload_file1():
    global file1_content, highlighted_content
    if 'file1' in request.files:
        file = request.files['file1']
        if file.filename != '':
            file1_content = file.read().decode('utf-8')
            highlighted_content = file1_content  # Mostrar inmediatamente el contenido al cargar
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
    global file1_content, highlighted_content
    if 'file1_content' in request.form:
        file1_content = request.form.get('file1_content')
        algorithm = request.form.get('algorithm')
        
        # Limpiar resaltado previo antes de aplicar nuevo algoritmo
        highlighted_content = file1_content
        
        if algorithm == 'buscar':
            # Algoritmo Z o KMP para buscar y resaltar el patrón
            palindromo = request.form.get('palindromo')  # Recibir el patrón del usuario
            highlighted_content = algoritmo_z_resaltar(highlighted_content, palindromo)
        elif algorithm == 'palindromo':
            # Algoritmo de Manacher para encontrar el palíndromo más largo
            palindromo_encontrado = manacher(file1_content)
            highlighted_content = file1_content.replace(palindromo_encontrado, f"<span style='background-color: green'>{palindromo_encontrado}</span>")
    
    return redirect(url_for('index'))

# Algoritmo Z para buscar y resaltar el patrón
def algoritmo_z_resaltar(texto, palindromo):
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
        
        posiciones = []
        for i in range(len(palindromo) + 1, n):
            if Z[i] == len(palindromo):
                posiciones.append(i - len(palindromo) - 1)
        
        return posiciones

    posiciones = Z(texto, palindromo)
    texto_resaltado = ""
    ultimo_index = 0

    for pos in posiciones:
        texto_resaltado += texto[ultimo_index:pos]
        texto_resaltado += f"<span style='background-color: yellow;'>{texto[pos:pos + len(palindromo)]}</span>"
        ultimo_index = pos + len(palindromo)

    texto_resaltado += texto[ultimo_index:]
    return texto_resaltado

# Algoritmo de Manacher para buscar el palíndromo más largo
def manacher(s):
    t = '#'.join(f'^{s}$')
    n = len(t)
    P = [0] * n
    C = R = 0  # Centro y borde derecho del palíndromo actual

    for i in range(1, n - 1):
        mirror = 2 * C - i
        if i < R:
            P[i] = min(R - i, P[mirror])
        # Expande el palíndromo centrado en i
        while t[i + 1 + P[i]] == t[i - 1 - P[i]]:
            P[i] += 1
        # Actualiza el centro y el borde derecho
        if i + P[i] > R:
            C = i
            R = i + P[i]

    # Encuentra el palíndromo más largo
    maxLen = max(P)
    centerIndex = P.index(maxLen)
    start = (centerIndex - maxLen) // 2
    return s[start:start + maxLen]

if __name__ == '__main__':
    app.run(debug=True)