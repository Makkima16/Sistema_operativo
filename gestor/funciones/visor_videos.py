import os
import time
import tkinter as tk

import cv2
import customtkinter as ctk
import pygame
from tkinter import messagebox

from kernel import config, procesos

try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip


def abrir_video(archivo_video, usuario):
    if not archivo_video:
        messagebox.showerror("Error", "No se seleccionó un archivo de video válido.")
        return

    carpeta_videos = str(config.get_user_dir(usuario) / "Videos")
    os.makedirs(carpeta_videos, exist_ok=True)

    procesos.register("Visor de videos")

    ventana_video = ctk.CTkToplevel()
    ventana_video.title("Visualizador de Video")
    ventana_video.resizable(False, False)

    cap = cv2.VideoCapture(archivo_video)
    if not cap.isOpened():
        procesos.unregister("Visor de videos")
        ventana_video.destroy()
        messagebox.showerror("Error", "No se pudo abrir el archivo de video.")
        return

    ancho_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 800
    alto_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 600

    lienzo = tk.Canvas(ventana_video, width=ancho_video, height=alto_video)
    lienzo.pack(fill="both", expand=True)

    archivo_audio = os.path.join(
        carpeta_videos, os.path.splitext(os.path.basename(archivo_video))[0] + ".wav"
    )

    audio_available = False
    video_clip = None
    try:
        video_clip = VideoFileClip(archivo_video)
        audio_clip = video_clip.audio
        if audio_clip is not None:
            try:
                audio_clip.write_audiofile(archivo_audio, logger=None)
            except AttributeError:
                audio_clip.to_audiofile(archivo_audio, logger=None)
            audio_available = os.path.exists(archivo_audio)
    except Exception:
        audio_available = False

    if audio_available:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(archivo_audio)
            pygame.mixer.music.play()
        except Exception:
            audio_available = False

    inicio = time.time()

    def cerrar_video():
        cap.release()
        if video_clip is not None:
            try:
                video_clip.close()
            except Exception:
                pass
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        procesos.unregister("Visor de videos")
        ventana_video.destroy()

    def actualizar_video():
        if not ventana_video.winfo_exists():
            return

        if audio_available and pygame.mixer.music.get_busy():
            tiempo_actual = pygame.mixer.music.get_pos() / 1000.0
            if tiempo_actual < 0:
                tiempo_actual = 0
        else:
            tiempo_actual = time.time() - inicio

        cap.set(cv2.CAP_PROP_POS_MSEC, tiempo_actual * 1000)
        ret, frame = cap.read()

        if ret:
            frame_resized = cv2.resize(frame, (ancho_video, alto_video))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            data = cv2.imencode(".png", frame_rgb)[1].tobytes()
            foto = tk.PhotoImage(
                master=lienzo,
                width=frame_rgb.shape[1],
                height=frame_rgb.shape[0],
                data=data,
            )
            lienzo.create_image(0, 0, anchor=tk.NW, image=foto)
            lienzo.image = foto
            lienzo.after(30, actualizar_video)
        else:
            cerrar_video()

    ventana_video.protocol("WM_DELETE_WINDOW", cerrar_video)
    actualizar_video()
