from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Variables globales para almacenar el contenido de los archivos y la opción seleccionada
file1_content = None
file2_content = None
highlighted_content = None
selected_option = None

@app.route('/')
def index():
    # Renderizar la plantilla con el contenido de ambos archivos y la opción seleccionada
    return render_template('index.html', content1=file1_content, content2=file2_content, highlighted_content=highlighted_content, selected_option=selected_option)

# Ruta para seleccionar opción de algoritmo
@app.route('/select_option', methods=['POST'])
def select_option():
    global selected_option, highlighted_content, file1_content, file2_content
    selected_option = request.form.get('algorithm')
    
    # Limpiar los contenidos al cambiar de algoritmo
    highlighted_content = None
    file1_content = None
    file2_content = None
    
    return redirect(url_for('index'))

@app.route('/upload_file1', methods=['POST'])
def upload_file1():
    global file1_content, highlighted_content
    if 'file1' in request.files:
        file = request.files['file1']
        if file.filename != '':
            file1_content = file.read().decode('utf-8')
            # Si estamos en el modo de Similitud, iniciar el diccionario para el contenido resaltado, sino cargar texto plano
            if selected_option == 'similitud':
                highlighted_content = {'file1': file1_content}  # Mostrar solo el primer archivo si el segundo no está listo
            else:
                highlighted_content = file1_content  # Mostrar en texto plano para las opciones de Buscar y Palíndromo
    return redirect(url_for('index'))

@app.route('/upload_file2', methods=['POST'])
def upload_file2():
    global file2_content, highlighted_content
    if 'file2' in request.files:
        file = request.files['file2']
        if file.filename != '':
            file2_content = file.read().decode('utf-8')
            if highlighted_content and isinstance(highlighted_content, dict):
                highlighted_content['file2'] = file2_content  # Almacenar el contenido del segundo archivo en el diccionario
            else:
                highlighted_content = {'file1': file1_content, 'file2': file2_content}  # Crear el diccionario si ambos archivos están presentes
    return redirect(url_for('index'))


# Ruta para aplicar un algoritmo al primer archivo (Buscar Patrón o Palíndromo)
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
            patron = request.form.get('patron')  # Recibir el patrón del usuario
            highlighted_content = algoritmo_z_resaltar(highlighted_content, patron)
        elif algorithm == 'palindromo':
            # Algoritmo de Manacher para encontrar el palíndromo más largo
            palindromo_encontrado = manacher(file1_content)
            highlighted_content = file1_content.replace(palindromo_encontrado, f"<span style='background-color: green'>{palindromo_encontrado}</span>")
    
    return redirect(url_for('index'))

# Ruta para aplicar el algoritmo LCS (Similitud entre dos textos)
@app.route('/apply_algorithm_lcs', methods=['POST'])
def apply_algorithm_lcs():
    global file1_content, file2_content, highlighted_content
    if 'file1_content' in request.form and 'file2_content' in request.form:
        file1_content = request.form.get('file1_content')
        file2_content = request.form.get('file2_content')
        
        # Aplicar el algoritmo LCS
        lcs_result = lcs(file1_content, file2_content)
        
        # Resaltar la subcadena común más larga en azul claro en ambos archivos
        highlighted_file1 = file1_content.replace(lcs_result, f"<span style='background-color: #add8e6'>{lcs_result}</span>")
        highlighted_file2 = file2_content.replace(lcs_result, f"<span style='background-color: #add8e6'>{lcs_result}</span>")
        
        # Almacenar los resultados por separado para cada archivo
        highlighted_content = {'file1': highlighted_file1, 'file2': highlighted_file2}
    
    return redirect(url_for('index'))

# Algoritmo Z para buscar y resaltar el patrón
def algoritmo_z_resaltar(texto, patron):
    def Z(texto, patron):
        cadena_concatenada = patron + "$" + texto
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
        for i in range(len(patron) + 1, n):
            if Z[i] == len(patron):
                posiciones.append(i - len(patron) - 1)
        
        return posiciones

    posiciones = Z(texto, patron)
    texto_resaltado = ""
    ultimo_index = 0

    for pos in posiciones:
        texto_resaltado += texto[ultimo_index:pos]
        texto_resaltado += f"<span style='background-color: yellow;'>{texto[pos:pos + len(patron)]}</span>"
        ultimo_index = pos + len(patron)

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

# Algoritmo LCS para encontrar la subcadena común más larga
def lcs(T1, T2):
    n = len(T1)
    m = len(T2)
    
    # Crear matriz de ceros de tamaño (n+1) x (m+1)
    M = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    end_idx = 0
    
    # Llenar la matriz según el algoritmo de LCS
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if T1[i - 1] == T2[j - 1]:
                M[i][j] = M[i - 1][j - 1] + 1
                if M[i][j] > max_len:
                    max_len = M[i][j]
                    end_idx = i
            else:
                M[i][j] = 0
    
    # La subcadena más larga estará en el rango [end_idx - max_len : end_idx]
    lcs_string = T1[end_idx - max_len:end_idx]
    return lcs_string

if __name__ == '__main__':
    app.run(debug=True)