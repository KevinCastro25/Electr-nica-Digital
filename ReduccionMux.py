"""
Proyecto reduccion de MUX
"""
import math
import numpy as np
import tkinter as tk
from tkinter import messagebox

#------------------------------------------------------------------------------------------------------------------------
# Función para calcular el número de variables necesarias a partir de los minterms
def calcular_num_vars(minterms):
    """
    Calcula el número de variables necesarias para representar los minterms.
    Args:
        minterms (list): Lista de minterms.

    Returns:
        int: Número de variables necesarias.
    """
    if (max(minterms) == 0):
        return 1
    else:
        return math.ceil(math.log2(max(minterms) + 1))
#------------------------------------------------------------------------------------------------------------------------
# Función para seleccionar el MUX correcto basado en el número de variables
def seleccionar_mux(num_vars):
    """
    Selecciona el tamaño del MUX (2^n) basado en el número de variables.
    Args:
        num_vars (int): Número de variables.

    Returns:
        int: Número de entradas del MUX.
    """
    s = num_vars - 1
    mux = 2 ** s
    return mux
#------------------------------------------------------------------------------------------------------------------------
def EsPotencia(Numero):
    """
    Verifica si un número es potencia de dos.
    Args:
        Numero (int): Número a verificar.

    Returns:
        bool: True si es potencia de dos, False en caso contrario.
    """
    return (Numero & (Numero - 1)) == 0 and Numero != 0
#------------------------------------------------------------------------------------------------------------------------
def AnalizarTabla(Fila1, Fila2):
    """
    Analiza dos filas de minterms y genera una lista de resultados.

    Args:
        Fila1 (list): Primera fila de minterms.
        Fila2 (list): Segunda fila de minterms.

    Returns:
        list: Lista de resultados analizados.
    """
    Resultado = []
    for i in range(len(Fila1)):
        if (Fila1[i] == -1 and Fila2[i] == -1):
            Resultado.append("1")
        elif (Fila1[i] == -1):
            Resultado.append("A'")
        elif (Fila2[i] == -1):
            Resultado.append("A")
        else:
            Resultado.append("0")
    return Resultado
#------------------------------------------------------------------------------------------------------------------------
# Función para simular el circuito MUX
def simular_circuito(equivalencias, NumeroMux):
    """
    Crea una ventana para simular el circuito MUX.

    Args:
        equivalencias (list): Lista de equivalencias de salida.
        NumeroMux (int): Número de entradas del MUX.
    """
    sim_ventana = tk.Toplevel()
    sim_ventana.title("Simulación de Circuito MUX")
    sim_ventana.geometry("700x500")
    sim_ventana.configure(bg="#E6E6FA")

    # Crear un canvas con scrollbar vertical
    canvas = tk.Canvas(sim_ventana, bg="#F4F6F7")
    scrollbar = tk.Scrollbar(sim_ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Añadir funcionalidad para desplazar con la rueda del ratón
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    sim_ventana.bind_all("<MouseWheel>", on_mouse_wheel)

    # Ajustar el tamaño del MUX basado en el número de entradas
    rect_width = 100  # Ancho del MUX
    rect_height = 50 + (len(equivalencias) * 30)  # Altura ajustada según las entradas
    rect_x_start = 300
    rect_x_end = rect_x_start + rect_width
    rect_y_start = 100
    rect_y_end = rect_y_start + rect_height

    # Dibujar el MUX
    canvas.create_rectangle(rect_x_start, rect_y_start, rect_x_end, rect_y_end, fill="#FF6347", outline="#1C2833", width=2)
    canvas.create_text((rect_x_start + rect_x_end) / 2, rect_y_start - 20, text=f"{NumeroMux}x1 MUX", font=("Helvetica", 14, "bold"), fill="black")

    # Dibujar las entradas conectadas al MUX
    for i in range(NumeroMux):
        entrada_y = rect_y_start + (i + 1) * (rect_height / (NumeroMux + 1))
        canvas.create_line(rect_x_start - 50, entrada_y, rect_x_start, entrada_y, fill="black", width=2)

        # Dibujar el símbolo correspondiente a la entrada
        if equivalencias[i] == '1':
            canvas.create_line(rect_x_start - 70, entrada_y - 10, rect_x_start - 50, entrada_y, fill="red", width=2)  # Línea para "V+"
            canvas.create_text(rect_x_start - 80, entrada_y - 10, text="V+", font=("Helvetica", 12), anchor=tk.E)
        elif equivalencias[i] == '0':
            canvas.create_line(rect_x_start - 70, entrada_y - 10, rect_x_start - 50, entrada_y - 10, fill="blue", width=2)
            canvas.create_line(rect_x_start - 65, entrada_y - 5, rect_x_start - 50, entrada_y - 5, fill="blue", width=2)
            canvas.create_line(rect_x_start - 60, entrada_y, rect_x_start - 50, entrada_y, fill="blue", width=2)
            canvas.create_text(rect_x_start - 80, entrada_y - 10, text="GND", font=("Helvetica", 12), anchor=tk.E)
        else:
            canvas.create_text(rect_x_start - 60, entrada_y, text=equivalencias[i], font=("Helvetica", 12), anchor=tk.E)

    # Dibujar las variables de control debajo del MUX, organizadas horizontalmente
    num_variables = math.ceil(math.log2(NumeroMux))
    var_y_start = rect_y_end + 50
    var_spacing = (rect_x_end - rect_x_start) / (num_variables + 1)

    for i in range(num_variables):
        var_x = rect_x_start + (i + 1) * var_spacing
        var_y = var_y_start
        canvas.create_line(var_x, var_y + 10, var_x, rect_y_end, fill="black", width=2)  # Línea para la variable
        canvas.create_text(var_x, var_y + 30, text=f"S{i}", font=("Helvetica", 12), fill="black")  # Texto debajo de la línea

    # Dibujar la salida
    salida_y = (rect_y_start + rect_y_end) / 2
    canvas.create_line(rect_x_end, salida_y, rect_x_end + 50, salida_y, fill="red", width=2)
    canvas.create_text(rect_x_end + 70, salida_y, text="Q", font=("Helvetica", 12), anchor=tk.W)
    sim_ventana.mainloop()
#------------------------------------------------------------------------------------------------------------------------
# Interfaz gráfica principal
def principal():
    """
    Crea la interfaz gráfica principal para el reductor de MUX.
    """
    def calcular():
        """
        Función que se ejecuta al presionar el botón "Calcular". 
        Toma los minterms de entrada y calcula el MUX reducido.
        """
        try:
            Elementos = entrada_minterms.get()
            Minterms = Elementos.strip().split()
            MintermsCopy = [int(minterm) for minterm in Minterms]
            if (len(Minterms)== 1 and Minterms[0] == "0"):
                NumVars=1
            else:
                NumVars = calcular_num_vars(MintermsCopy)
            Variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            # Generar cadena con el número de variables
            variables_str = f"La función contiene {NumVars} variables: "
            for i in range(NumVars):
                variables_str += f"{Variables[i]} "
            NumeroMux = seleccionar_mux(NumVars)  # Seleccionar el MUX adecuado
            mux_str = f"El MUX reducido será de {NumeroMux}x1\n"
            # Cabecera de la tabla
            headers = "\t".join([f"I{i}" for i in range(NumeroMux)])
            resultado = f"{variables_str}\n{mux_str}\n\t{headers}\n"
            controlador = max(MintermsCopy)
            while not EsPotencia(controlador + 1):
                controlador += 1
            array = np.arange(0, controlador + 1)  # Crear el rango de minterms
            Fila1, Fila2 = [], []
            if (len(Minterms)== 1 and Minterms[0] == "0"):
                Fila1.append(-1)
                resultado += "A'\t"
                resultado += f"0\t"
                Fila2.append(1)
                resultado += "\nA\t"
                resultado += f"1\t"
            else:
                resultado += "A'\t"
                for i in range(NumeroMux):
                    resultado += f"{array[i]}\t"
                    if array[i] in MintermsCopy:
                        Fila1.append(-1)
                    else:
                        Fila1.append(int(array[i]))
                resultado += "\nA\t"
                for i in range(NumeroMux):
                    resultado += f"{array[i + NumeroMux]}\t"
                    if array[i + NumeroMux] in MintermsCopy:
                        Fila2.append(-1)
                    else:
                        Fila2.append(int(array[i + NumeroMux]))
            Resultado = AnalizarTabla(Fila1, Fila2)  # Analizar la tabla
            resultado += "\nQ:\t" + "\t".join(Resultado)
            equivalencias = Resultado[:NumeroMux]
            label_resultado.config(text=resultado, justify="left")
            simular_circuito(equivalencias, NumeroMux)  # Simular el circuito
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese minterms válidos.")
#------------------------------------------------------------------------------------------------------------------------    
    def limpiar():
        """
        Limpia el campo de entrada y el resultado.
        """
        entrada_minterms.delete(0, tk.END)
        label_resultado.config(text="")
#------------------------------------------------------------------------------------------------------------------------    
    def salir():
        """
        Cierra la ventana principal.
        """
        ventana.destroy()
#------------------------------------------------------------------------------------------------------------------------
    ventana = tk.Tk()
    ventana.title("Reductor de MUX")
    ventana.geometry("700x400")
    ventana.configure(bg="#ADD8E6")
    # Elementos de la interfaz
    label_titulo = tk.Label(ventana, text="Reductor de MUX", font=("Helvetica", 18, "bold"), bg="#ADD8E6")
    label_titulo.pack(pady=10)
    frame_entrada = tk.Frame(ventana, bg="#ADD8E6")
    frame_entrada.pack(pady=5)
    label_minterms = tk.Label(frame_entrada, text="Ingrese los minterms separados por espacio:", bg="#ADD8E6")
    label_minterms.grid(row=0, column=0, padx=5)
    entrada_minterms = tk.Entry(frame_entrada, width=40)
    entrada_minterms.grid(row=0, column=1, padx=5)
    frame_botones = tk.Frame(ventana, bg="#ADD8E6")
    frame_botones.pack(pady=10)
    # Botones de acción
    boton_calcular = tk.Button(frame_botones, text="Calcular", command=calcular, bg="#90EE90", font=("Helvetica", 12), width=10)
    boton_calcular.grid(row=0, column=0, padx=10)
    boton_limpiar = tk.Button(frame_botones, text="Limpiar", command=limpiar, bg="#FFD700", font=("Helvetica", 12), width=10)
    boton_limpiar.grid(row=0, column=1, padx=10)
    boton_salir = tk.Button(frame_botones, text="Salir", command=salir, bg="#FF6347", font=("Helvetica", 12), width=10)
    boton_salir.grid(row=0, column=2, padx=10)
    # Frame para mostrar resultados con scroll horizontal
    frame_resultado = tk.Frame(ventana, bg="#ADD8E6")
    frame_resultado.pack(fill=tk.X, padx=10, pady=10)
    canvas_resultado = tk.Canvas(frame_resultado, bg="#F4F6F7")
    scrollbar_horizontal = tk.Scrollbar(frame_resultado, orient="horizontal", command=canvas_resultado.xview)
    scrollable_frame_resultado = tk.Frame(canvas_resultado)
    # Configurar el scrollable_frame para que se ajuste al canvas
    scrollable_frame_resultado.bind(
        "<Configure>",
        lambda e: canvas_resultado.configure(scrollregion=canvas_resultado.bbox("all"))
    )
    canvas_resultado.create_window((0, 0), window=scrollable_frame_resultado, anchor="nw")
    canvas_resultado.configure(xscrollcommand=scrollbar_horizontal.set)
    scrollbar_horizontal.pack(side="bottom", fill="x")
    canvas_resultado.pack(side="top", fill="both", expand=True)
    # Label para mostrar el resultado
    label_resultado = tk.Label(scrollable_frame_resultado, text="", bg="#F4F6F7", justify="left")
    label_resultado.pack()
    ventana.mainloop()
#------------------------------------------------------------------------------------------------------------------------
# Inicia la aplicación
principal()