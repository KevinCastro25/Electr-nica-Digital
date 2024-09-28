#Librerias necesarias
import math
import tkinter as tk
"""
Algoritmo que simula el metodo de McCluskey 
"""
# Función para contar el número de 1's en la representación binaria
def count_ones(term):
    """
    Convierte un número entero a su representación binaria y cuenta el número de bits en 1's.
    
    Parámetros:
    - term: número entero para convertir y contar
    
    Retorna:
    - Número de bits en 1's
    """
    return bin(term).count('1')

# Función para obtener la representación binaria de un número con longitud fija
def to_binary_string(term, length):
    """
    Convierte un número entero a una cadena binaria de longitud fija.
    
    Parámetros:
    - term: número entero para convertir
    - length: longitud deseada de la cadena binaria
    
    Retorna:
    - Cadena binaria de longitud fija
    """
    return bin(term)[2:].zfill(length)

# Función para combinar dos términos si difieren en exactamente un bit
def combine_terms(term1, term2):
    """
    Combina dos términos binarios si difieren en exactamente un bit.
    Retorna el término combinado si la diferencia es exactamente un bit, de lo contrario, None.
    
    Parámetros:
    - term1: primer término binario
    - term2: segundo término binario
    
    Retorna:
    - Término combinado con un guion '-' en la posición del bit diferente, o None si no es combinable
    """
    combined = ""  # Inicializa la cadena combinada
    differences = 0  # Contador de diferencias entre los términos
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            combined += "-"  # Usa "-" para indicar el bit diferente
            differences += 1
        else:
            combined += term1[i]  # Mantiene el bit igual
    return combined if differences == 1 else None  # Retorna el término combinado si solo hay una diferencia

# Función para traducir los implicantes a variables A, B, C...
def implicant_to_variables(implicant, num_vars):
    """
    Traduce un implicante binario a una expresión booleana con variables A, B, C...
    
    Parámetros:
    - implicant: término binario combinado
    - num_vars: número de variables necesarias
    
    Retorna:
    - Expresión booleana en formato de variables
    """
    variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:num_vars]  # Variables necesarias
    expression = []  # Lista para construir la expresión booleana
    for i, bit in enumerate(implicant):
        if bit == '1':
            expression.append(variables[i])  # Añade la variable si el bit es 1
        elif bit == '0':
            expression.append(variables[i] + "'")  # Añade la variable negada si el bit es 0
    return ''.join(expression)  # Une los elementos en una cadena

# Función principal para minimizar con el metodo de McCluskey
def quine_mccluskey(minterms):
    """
    Minimiza una función booleana utilizando el método de Quine-McCluskey.
    
    Parámetros:
    - minterms: lista de minterms para simplificar
    
    Retorna:
    - Tuple con la lista de expresiones booleanas simplificadas y el número de variables
    """
    num_vars = math.ceil(math.log2(max(minterms) + 1))  # Determina el número de variables necesarias
    groups = {}  # Diccionario para agrupar términos por número de 1's
    for minterm in minterms:
        bin_term = to_binary_string(minterm, num_vars)  # Convierte minterm a binario
        ones_count = count_ones(minterm)  # Cuenta el número de 1's
        if ones_count not in groups:
            groups[ones_count] = []  # Crea el grupo si no existe
        groups[ones_count].append(bin_term)  # Agrega el minterm al grupo correspondiente
    prime_implicants = set()  # Conjunto para almacenar implicantes primos
    checked = set()  # Conjunto para almacenar términos combinados
    while True:
        new_groups = {}  # Diccionario para los nuevos grupos de términos combinados
        combined = False  # Indica si se han realizado combinaciones
        for i in range(len(groups) - 1):
            if i in groups and i + 1 in groups:
                for term1 in groups[i]:
                    for term2 in groups[i + 1]:
                        combined_term = combine_terms(term1, term2)  # Intenta combinar términos
                        if combined_term:
                            combined = True  # Se realizó una combinación
                            checked.add(term1)  # Marca los términos como combinados
                            checked.add(term2)
                            ones_count = combined_term.count('1')  # Cuenta los 1's en el término combinado
                            if ones_count not in new_groups:
                                new_groups[ones_count] = []  # Crea el grupo si no existe
                            if combined_term not in new_groups[ones_count]:
                                new_groups[ones_count].append(combined_term)  # Agrega el término combinado al grupo

        # Agrega términos no combinados a los implicantes primos
        for group in groups.values():
            for term in group:
                if term not in checked:
                    prime_implicants.add(term)
        
        if not combined:
            break  # Sale del bucle si no hay más combinaciones
        groups = new_groups  # Actualiza los grupos para la siguiente iteración

    # Paso 2: Determinar los implicantes primos esenciales
    essential_prime_implicants = []  # Lista para los implicantes primos esenciales
    uncovered_minterms = set(minterms)  # Conjunto de minterms no cubiertos
    table = {implicant: set() for implicant in prime_implicants}  # Tabla de implicantes y minterms cubiertos

    # Llenar la tabla de implicantes
    for minterm in minterms:
        bin_term = to_binary_string(minterm, num_vars)
        for implicant in prime_implicants:
            if all(x == y or x == '-' for x, y in zip(implicant, bin_term)):
                table[implicant].add(minterm)

    # Selección de implicantes primos esenciales
    while uncovered_minterms:
        if not table:  # Si la tabla está vacía y aún hay minterms no cubiertos, se debe usar la solución más simple
            return None
        best_choice = max(table, key=lambda imp: len(table[imp] & uncovered_minterms))
        essential_prime_implicants.append(best_choice)  # Añadir implicante esencial
        covered = table[best_choice]  # Minterms cubiertos por este implicante
        uncovered_minterms -= covered  # Elimina los minterms cubiertos

    result_in_vars = [implicant_to_variables(imp, num_vars) for imp in essential_prime_implicants]  # Convierte implicantes primos a variables
    return result_in_vars, num_vars

# Función que se ejecuta cuando el usuario presiona el botón de calcular
def calcular():
    """
    Procesa la entrada del usuario, llama a la función de minimización y actualiza la interfaz gráfica con el resultado.
    """
    try:
        minterms = list(map(int, entry_minterms.get().split()))  # Convierte la entrada a una lista de enteros
        result, num_vars = quine_mccluskey(minterms)  # Llama a la función para simplificar
        #Verificacion para los casos (0---7) , (0 ---- 15) ,etc.
        if (result[0] != ""):
            result_str = ' + '.join(result)  # Formatea el resultado como una suma de términos
        else:
            result_str = None
        if (result_str == None):
            result_label.config(text=f"Número de variables: {num_vars}\nImplicantes esenciales:\n 1", fg="white")
        else:
            result_label.config(text=f"Número de variables: {num_vars}\nImplicantes esenciales:\n{result_str}", fg="white")
    except ValueError:
        result_label.config(text="Error: Entrada inválida. Por favor, ingrese minterms separados por espacio.", fg="red")

# Función para limpiar los campos de entrada y el resultado
def limpiar():
    """
    Limpia el campo de entrada y el texto del resultado.
    """
    entry_minterms.delete(0, tk.END)  # Limpia la entrada de minterms
    result_label.config(text="")  # Borra el texto del resultado

# Función para salir de la aplicación
def salir():
    """
    Cierra la ventana principal de la aplicación.
    """
    root.destroy()  # Cierra la ventana principal

# Crear la ventana principal de la interfaz gráfica
root = tk.Tk()
root.title("Simplificación de McCluskey")  # Establece el título de la ventana
root.geometry("550x450")  # Define las dimensiones de la ventana
root.config(bg="#1E1E1E")  # Establece un color de fondo oscuro

# Estilo de fuente
font_style = ("Arial", 14, "bold")
font_style_result = ("Arial", 12)

# Encabezado
header_label = tk.Label(root, text="Método de McCluskey", font=("Arial", 20, "bold"), bg="#1E1E1E", fg="#FFFFFF")
header_label.pack(pady=20)

# Etiqueta para el campo de entrada
label_minterms = tk.Label(root, text="Introduce los minterminos separados por espacio:", font=font_style, bg="#1E1E1E", fg="#FFFFFF")
label_minterms.pack(pady=10)

# Campo de entrada
entry_minterms = tk.Entry(root, width=50, font=("Arial", 12))  # Entrada para los minterms
entry_minterms.pack(pady=10)

# Frame para los botones
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=20)

# Botón para calcular
btn_calcular = tk.Button(button_frame, text="Calcular", command=calcular, width=15, bg="#4CAF50", fg="white", font=font_style)
btn_calcular.pack(side=tk.LEFT, padx=10)

# Botón para limpiar
btn_limpiar = tk.Button(button_frame, text="Limpiar", command=limpiar, width=15, bg="#FFC107", fg="black", font=font_style)
btn_limpiar.pack(side=tk.LEFT, padx=10)

# Botón para salir
btn_salir = tk.Button(button_frame, text="Salir", command=salir, width=15, bg="#F44336", fg="white", font=font_style)
btn_salir.pack(side=tk.LEFT, padx=10)

# Etiqueta para mostrar resultados
result_label = tk.Label(root, text="", font=font_style_result, bg="#1E1E1E", fg="#FFFFFF")
result_label.pack(pady=20)

# Ejecutar la interfaz gráfica
root.mainloop()
