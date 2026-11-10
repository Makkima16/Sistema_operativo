import os

import customtkinter as ctk
import yt_dlp as youtube_dl
from tkinter import messagebox

from kernel import config


def descargar_video(url, calidad, usuario):
    if not url:
        messagebox.showerror("Error", "Por favor ingresa una URL válida.")
        return

    carpeta_videos = str(config.get_user_dir(usuario) / "Videos")
    os.makedirs(carpeta_videos, exist_ok=True)

    if calidad == "best":
        fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
        fmt = f"bestvideo[height<={calidad}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

    ydl_opts = {
        "format": fmt,
        "outtmpl": os.path.join(carpeta_videos, "%(title)s.%(ext)s"),
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Video descargado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def ventana_descarga_video(usuario):
    ventana_video = ctk.CTkToplevel()
    ventana_video.title("Descargar Video")

    url_label = ctk.CTkLabel(ventana_video, text="Ingresa la URL del video:")
    url_label.pack(padx=10, pady=10)

    url_entry = ctk.CTkEntry(ventana_video, width=300)
    url_entry.pack(padx=10, pady=10)

    calidad_label = ctk.CTkLabel(ventana_video, text="Elige la calidad (1080, 720, 480):")
    calidad_label.pack(padx=10, pady=10)

    calidad_var = ctk.StringVar(value="1080")
    calidad_menu = ctk.CTkOptionMenu(ventana_video, variable=calidad_var, values=["1080", "720", "480", "best"])
    calidad_menu.pack(padx=10, pady=10)

    def descargar_video_action():
        descargar_video(url_entry.get(), calidad_var.get(), usuario)
        ventana_video.destroy()

    boton_descargar_video = ctk.CTkButton(
        ventana_video, text="Descargar Video", command=descargar_video_action
    )
    boton_descargar_video.pack(padx=10, pady=10)
