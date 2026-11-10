import customtkinter as ctk
from PIL import Image, ImageTk


def abrir_visor_imagenes(ruta_imagen):
    visor = ctk.CTkToplevel()
    visor.title("Visor de Imágenes")
    visor.geometry("800x600")
    visor.resizable(False, False)

    etiqueta_imagen = ctk.CTkLabel(visor, text="")
    etiqueta_imagen.pack(expand=True)

    imagen_ref = {"imagen": None}

    def cargar_imagen(ruta):
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((800, 600), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen.configure(image=imagen_tk, text="")
            imagen_ref["imagen"] = imagen_tk
        except Exception as e:
            etiqueta_imagen.configure(image=None, text=f"Error al abrir la imagen: {e}")

    cargar_imagen(ruta_imagen)

    boton_cerrar = ctk.CTkButton(visor, text="Cerrar", command=visor.destroy)
    boton_cerrar.pack(pady=10)
