import math

import customtkinter as ctk

from kernel import procesos


def abrir_calculadora():
    procesos.register("Calculadora")

    calculadora = ctk.CTkToplevel()
    calculadora.geometry("400x600")
    calculadora.title("Calculadora Científica")
    calculadora.attributes("-topmost", True)
    calculadora.resizable(False, False)

    entrada = ctk.CTkEntry(calculadora, width=350)
    entrada.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

    def agregar_a_entrada(simbolo):
        entrada.insert("end", simbolo)

    def calcular():
        try:
            expresion = entrada.get().replace("^", "**")
            resultado = eval(expresion, {"__builtins__": None}, {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e,
                "cub": math.cbrt,
            })
            entrada.delete(0, "end")
            entrada.insert("end", resultado)
        except Exception:
            entrada.delete(0, "end")
            entrada.insert("end", "Error")

    def limpiar():
        entrada.delete(0, "end")

    botones = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('(', 2, 4),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), (')', 3, 4),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 3), ('^', 4, 4),
        ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3), ('sqrt', 5, 4),
        ('pi', 6, 0), ('e', 6, 1), ('=', 4, 2), ('cub', 6, 2),
    ]

    for texto, fila, columna in botones:
        if texto == '=':
            boton = ctk.CTkButton(calculadora, text=texto, width=60, height=50, command=calcular)
        elif texto == 'C':
            boton = ctk.CTkButton(calculadora, text=texto, width=60, height=50, command=limpiar)
        else:
            boton = ctk.CTkButton(
                calculadora, text=texto, width=60, height=50,
                command=lambda t=texto: agregar_a_entrada(t),
            )
        boton.grid(row=fila, column=columna, padx=10, pady=10)

    def on_close():
        procesos.unregister("Calculadora")
        calculadora.destroy()

    calculadora.protocol("WM_DELETE_WINDOW", on_close)
