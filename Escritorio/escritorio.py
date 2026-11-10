import time
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from Escritorio.calculadora import abrir_calculadora
from Recursos.recursos import monitorear_recursos
from gestor.gestorArchivos import mostrar_gestor_archivos
from juegos.culebrita import iniciar_culebrita
from kernel import config


def load_icon(name, size):
    path = config.image_path(name)
    if path.exists():
        return ctk.CTkImage(Image.open(path), size=size)
    return None


def obtener_clima():
    try:
        import requests
        respuesta = requests.get(config.URL_CLIMA, timeout=5)
        datos = respuesta.json()
        if respuesta.status_code == 200:
            temperatura = datos["main"]["temp"]
            descripcion = datos["weather"][0]["description"].capitalize()
            return f"{temperatura}°C, {descripcion}"
        return "Error al obtener el clima"
    except Exception:
        return "Sin conexión"


def mostrar_escritorio(usuario):
    escritorio = ctk.CTk()
    escritorio.geometry("1000x700")
    escritorio.title("Escritorio")
    escritorio.configure(fg_color="#56637e")
    escritorio.resizable(False, False)

    frame = ctk.CTkFrame(escritorio, fg_color="#18252a")
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    escritorio.grid_columnconfigure(0, weight=1)
    escritorio.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)

    def iniciar_webview():
        try:
            import webview
            webview.create_window("Mi Navegador Integrado", "https://www.google.com")
            webview.start()
        except ImportError:
            messagebox.showerror("Error", "El navegador no está disponible. Instala pywebview.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")

    etiqueta_bienvenida = ctk.CTkLabel(frame, text=f"Bienvenido, {usuario}", font=("Arial", 24))
    etiqueta_bienvenida.grid(row=2, column=0, pady=10, padx=10)

    imagen_estrella = ctk.CTkImage(Image.open(config.image_path("estrella.png")), size=(100, 100))
    boton_cerrar = ctk.CTkButton(
        frame, image=imagen_estrella, text="", fg_color="transparent", command=escritorio.destroy
    )
    boton_cerrar.grid(row=1, column=0, pady=10, padx=10)

    imagen_omnitrix = ctk.CTkImage(Image.open(config.image_path("omnitrix.png")), size=(100, 100))
    boton_omnitrix = ctk.CTkButton(
        frame, image=imagen_omnitrix, text="", fg_color="transparent", command=escritorio.destroy
    )
    boton_omnitrix.grid(row=4, column=0, padx=10, pady=10, sticky="sw")

    imagen_calculadora = ctk.CTkImage(Image.open(config.image_path("calculadora.png")), size=(100, 100))
    boton_calculadora = ctk.CTkButton(
        frame, image=imagen_calculadora, text="", fg_color="transparent", command=abrir_calculadora
    )
    boton_calculadora.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

    imagen_recursos = ctk.CTkImage(Image.open(config.image_path("recursos.png")), size=(100, 100))
    boton_recursos = ctk.CTkButton(
        frame, image=imagen_recursos, text="", fg_color="transparent", command=monitorear_recursos
    )
    boton_recursos.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    imagen_gestor = ctk.CTkImage(Image.open(config.image_path("gestor.png")), size=(100, 100))
    boton_gestor = ctk.CTkButton(
        frame, image=imagen_gestor, text="", fg_color="transparent",
        command=lambda: mostrar_gestor_archivos(usuario)
    )
    boton_gestor.grid(row=0, column=0, padx=10, pady=10, sticky="sw")

    icon_culebrita = load_icon("culebrita.png", (100, 100))
    boton_culebrita = ctk.CTkButton(
        frame,
        image=icon_culebrita,
        text="" if icon_culebrita else "Culebrita",
        fg_color="transparent",
        command=iniciar_culebrita,
    )
    boton_culebrita.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    etiqueta_reloj = ctk.CTkLabel(frame, text="", font=("Arial", 14), fg_color="#18252a")
    etiqueta_reloj.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

    etiqueta_clima = ctk.CTkLabel(frame, text="Cargando clima...", font=("Arial", 14), fg_color="#18252a")
    etiqueta_clima.grid(row=4, column=0, padx=10, pady=10, sticky="se")

    icon_edge = load_icon("edge.png", (100, 100))
    boton_edge = ctk.CTkButton(
        frame,
        image=icon_edge,
        text="" if icon_edge else "Navegador",
        fg_color="transparent",
        command=iniciar_webview,
    )
    boton_edge.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

    ultimo_clima = {"ts": 0}

    def actualizar_reloj_y_clima():
        hora_actual = time.strftime("%H:%M:%S")
        fecha_actual = time.strftime("%Y-%m-%d")
        etiqueta_reloj.configure(text=f"{fecha_actual} {hora_actual}")

        ahora = time.time()
        if ahora - ultimo_clima["ts"] >= 60:
            etiqueta_clima.configure(text=obtener_clima())
            ultimo_clima["ts"] = ahora

        etiqueta_reloj.after(1000, actualizar_reloj_y_clima)

    etiqueta_clima.configure(text=obtener_clima())
    actualizar_reloj_y_clima()

    escritorio.mainloop()
