import os

import customtkinter as ctk
from tkinter import Text, messagebox


def abrir_txt(ruta_txt):
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title(f"Editor de Texto - {os.path.basename(ruta_txt)}")
    ventana_editor.geometry("600x500")

    text_area = Text(ventana_editor, wrap="word", font=("Arial", 12))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    try:
        with open(ruta_txt, "r", encoding="utf-8") as file:
            text_area.insert("1.0", file.read())
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
        ventana_editor.destroy()
        return

    def guardar_cambios():
        try:
            with open(ruta_txt, "w", encoding="utf-8") as file:
                file.write(text_area.get("1.0", "end-1c"))
            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.")
            ventana_editor.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar_cambios)
    boton_guardar.pack(padx=10, pady=10)

    boton_cancelar = ctk.CTkButton(ventana_editor, text="Cancelar", command=ventana_editor.destroy)
    boton_cancelar.pack(padx=10, pady=10)
