import os

import customtkinter as ctk
import pygame
from tkinter import messagebox

from kernel import procesos


def abrir_reproductor_audio(ruta_audio):
    procesos.register("Reproductor de audio")

    ventana = ctk.CTkToplevel()
    ventana.title(f"Reproductor de Audio - {os.path.basename(ruta_audio)}")
    ventana.geometry("400x280")

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(ruta_audio)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el audio: {e}")
        procesos.unregister("Reproductor de audio")
        ventana.destroy()
        return

    estado = {"pausado": False}

    etiqueta = ctk.CTkLabel(ventana, text=os.path.basename(ruta_audio), font=("Arial", 14))
    etiqueta.pack(pady=10)

    label_estado = ctk.CTkLabel(ventana, text="Detenido", font=("Arial", 12))
    label_estado.pack(pady=10)

    def reproducir():
        pygame.mixer.music.play()
        estado["pausado"] = False
        actualizar_estado()

    def pausar_reanudar():
        if estado["pausado"]:
            pygame.mixer.music.unpause()
            estado["pausado"] = False
        else:
            pygame.mixer.music.pause()
            estado["pausado"] = True
        actualizar_estado()

    def detener():
        pygame.mixer.music.stop()
        actualizar_estado()

    def on_close():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        procesos.unregister("Reproductor de audio")
        ventana.destroy()

    fila_botones = ctk.CTkFrame(ventana)
    fila_botones.pack(pady=10)

    ctk.CTkButton(fila_botones, text="Reproducir", command=reproducir).pack(side="left", padx=5)
    ctk.CTkButton(fila_botones, text="Pausar/Reanudar", command=pausar_reanudar).pack(side="left", padx=5)
    ctk.CTkButton(fila_botones, text="Detener", command=detener).pack(side="left", padx=5)
    ctk.CTkButton(ventana, text="Cerrar", command=on_close).pack(pady=10)

    def actualizar_estado():
        if not ventana.winfo_exists():
            return

        if pygame.mixer.music.get_busy():
            pos = pygame.mixer.music.get_pos() / 1000
            if pos < 0:
                pos = 0
            texto = "Pausado" if estado["pausado"] else "Reproduciendo"
            label_estado.configure(text=f"{texto} - {int(pos)}s")
        else:
            label_estado.configure(text="Detenido")

        ventana.after(500, actualizar_estado)

    ventana.protocol("WM_DELETE_WINDOW", on_close)
    actualizar_estado()
