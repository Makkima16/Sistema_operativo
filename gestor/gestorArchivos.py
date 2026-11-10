import csv
import os
import shutil

import customtkinter as ctk
import fitz
from docx import Document
from fpdf import FPDF
from openpyxl import Workbook
from PIL import Image, ImageTk
from tkinter import ACTIVE, END, Canvas, Listbox, Scrollbar, messagebox, ttk

from Usuarios.usuarios import obtener_rol
from gestor.funciones.descarga_videos import ventana_descarga_video
from gestor.funciones.edicion import abrir_txt
from gestor.funciones.reproductor_audio import abrir_reproductor_audio
from gestor.funciones.visor_imagenes import abrir_visor_imagenes
from gestor.funciones.visor_videos import abrir_video
from kernel import config, procesos

gestor_abierto = False


def dentro_de(ruta, base):
    try:
        return os.path.commonpath([os.path.abspath(ruta), os.path.abspath(base)]) == os.path.abspath(base)
    except ValueError:
        return False


def mostrar_gestor_archivos(usuario):
    global gestor_abierto

    if gestor_abierto:
        return

    gestor_abierto = True
    config.ensure_user_dirs(usuario)
    ruta_base_usuario = str(config.get_user_dir(usuario))
    raiz = str(config.USERS_DIR)
    rol = obtener_rol(usuario)
    limite = raiz if rol == "Administrador" else ruta_base_usuario

    ventana = ctk.CTkToplevel()
    ventana.geometry("800x600")
    ventana.title(f"Gestor de Archivos - {usuario}")
    ventana.resizable(False, False)

    procesos.register("Gestor de Archivos")

    frame = ctk.CTkFrame(ventana, fg_color="#282c34")
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def listar_archivos(ruta):
        if not dentro_de(ruta, limite):
            messagebox.showerror("Error", "No tienes permiso para acceder a esta carpeta.")
            return

        lista_archivos.delete(0, END)
        try:
            for archivo in os.listdir(ruta):
                lista_archivos.insert(END, archivo)
        except (PermissionError, FileNotFoundError):
            messagebox.showerror("Error", "No se pudo acceder a este directorio")

    def abrir_pdf(ruta_pdf):
        doc = fitz.open(ruta_pdf)
        ventana_pdf = ctk.CTkToplevel()
        ventana_pdf.title("Visor de PDF")
        ventana_pdf.geometry("800x600")

        canvas = Canvas(ventana_pdf)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(ventana_pdf, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        def mostrar_pagina(numero_pagina):
            if 0 <= numero_pagina < len(doc):
                page = doc[numero_pagina]
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                imagen_tk = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
                canvas.image = imagen_tk
                canvas.config(scrollregion=canvas.bbox("all"))

        pagina_actual = [0]

        def siguiente_pagina():
            if pagina_actual[0] + 1 < len(doc):
                pagina_actual[0] += 1
                mostrar_pagina(pagina_actual[0])

        def pagina_anterior():
            if pagina_actual[0] > 0:
                pagina_actual[0] -= 1
                mostrar_pagina(pagina_actual[0])

        boton_atras = ctk.CTkButton(ventana_pdf, text="Anterior", command=pagina_anterior)
        boton_atras.pack(side="left", padx=5, pady=5)

        boton_siguiente = ctk.CTkButton(ventana_pdf, text="Siguiente", command=siguiente_pagina)
        boton_siguiente.pack(side="left", padx=5, pady=5)

        mostrar_pagina(pagina_actual[0])

    def abrir_item():
        seleccionado = lista_archivos.get(ACTIVE)
        if not seleccionado:
            return

        nueva_ruta = os.path.join(entry_ruta.get(), seleccionado)

        if os.path.isdir(nueva_ruta):
            entry_ruta.delete(0, END)
            entry_ruta.insert(0, nueva_ruta)
            listar_archivos(nueva_ruta)
        elif seleccionado.endswith(".txt"):
            abrir_txt(nueva_ruta)
        elif seleccionado.endswith(".pdf"):
            abrir_pdf(nueva_ruta)
        elif seleccionado.endswith((".mp4", ".webm")):
            abrir_video(nueva_ruta, usuario)
        elif seleccionado.endswith((".png", ".jpg", ".jpeg")):
            abrir_visor_imagenes(nueva_ruta)
        elif seleccionado.endswith((".mp3", ".wav", ".ogg")):
            abrir_reproductor_audio(nueva_ruta)
        else:
            messagebox.showinfo("Información", f"No se puede abrir el archivo '{seleccionado}'.")

    def volver_atras():
        ruta_actual = os.path.abspath(entry_ruta.get())
        if ruta_actual == os.path.abspath(raiz):
            messagebox.showerror("Error", "No puede acceder más atrás.")
            return

        ruta_padre = os.path.dirname(ruta_actual)
        if not dentro_de(ruta_padre, limite):
            messagebox.showerror("Error", "No puedes salir de tu carpeta principal.")
            return

        entry_ruta.delete(0, END)
        entry_ruta.insert(0, ruta_padre)
        listar_archivos(ruta_padre)

    def borrar_item():
        seleccionado = lista_archivos.get(ACTIVE)
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un archivo o carpeta para eliminar.")
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación", f"¿Estás seguro de que deseas eliminar '{seleccionado}'?"
        )
        if not respuesta:
            return

        ruta_a_borrar = os.path.join(entry_ruta.get(), seleccionado)
        try:
            if os.path.isfile(ruta_a_borrar):
                os.remove(ruta_a_borrar)
            elif os.path.isdir(ruta_a_borrar):
                shutil.rmtree(ruta_a_borrar)
            listar_archivos(entry_ruta.get())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar '{seleccionado}': {e}")

    entry_ruta = ctk.CTkEntry(frame, width=600)
    entry_ruta.grid(row=0, column=0, pady=10, padx=10)
    entry_ruta.insert(0, ruta_base_usuario)

    boton_atras = ctk.CTkButton(frame, text="Atrás", command=volver_atras)
    boton_atras.grid(row=0, column=1, pady=10, padx=10)

    lista_archivos = Listbox(frame, height=20, width=80)
    lista_archivos.grid(row=1, column=0, pady=10, padx=10, columnspan=2)
    listar_archivos(ruta_base_usuario)

    boton_abrir = ctk.CTkButton(frame, text="Abrir", command=abrir_item)
    boton_abrir.grid(row=2, column=0, pady=10, padx=10)

    boton_borrar = ctk.CTkButton(frame, text="Borrar", command=borrar_item)
    boton_borrar.grid(row=2, column=1, pady=10, padx=10)

    def crear_archivo():
        ventana_archivo = ctk.CTkToplevel()
        ventana_archivo.title("Crear archivo")

        etiqueta = ctk.CTkLabel(ventana_archivo, text="Ingrese el nombre del archivo:")
        etiqueta.pack(padx=10, pady=10)

        entry_nombre_archivo = ctk.CTkEntry(ventana_archivo, width=300)
        entry_nombre_archivo.pack(padx=10, pady=10)

        tipos_archivos = ["txt", "docx", "pdf", "csv", "xlsx", "jpg", "png", "video"]

        etiqueta_tipo = ctk.CTkLabel(ventana_archivo, text="Seleccione el tipo de archivo:")
        etiqueta_tipo.pack(padx=10, pady=10)

        combo_tipo_archivo = ttk.Combobox(ventana_archivo, values=tipos_archivos, state="readonly")
        combo_tipo_archivo.pack(padx=10, pady=10)
        combo_tipo_archivo.current(0)

        def confirmar_creacion():
            nombre_archivo = entry_nombre_archivo.get()
            tipo_archivo = combo_tipo_archivo.get()

            if tipo_archivo == "video":
                ventana_descarga_video(usuario)
                ventana_archivo.destroy()
                return

            if not nombre_archivo:
                return

            nueva_ruta_archivo = os.path.join(entry_ruta.get(), f"{nombre_archivo}.{tipo_archivo}")

            if tipo_archivo == "txt":
                with open(nueva_ruta_archivo, "w", encoding="utf-8") as f:
                    f.write("Nuevo archivo creado")
            elif tipo_archivo == "docx":
                doc = Document()
                doc.add_paragraph("Nuevo documento creado")
                doc.save(nueva_ruta_archivo)
            elif tipo_archivo == "pdf":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Nuevo PDF creado", ln=True)
                pdf.output(nueva_ruta_archivo)
            elif tipo_archivo == "csv":
                with open(nueva_ruta_archivo, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Nuevo", "archivo", "CSV", "creado"])
            elif tipo_archivo == "xlsx":
                wb = Workbook()
                ws = wb.active
                ws.append(["Nuevo archivo", "Excel", "creado"])
                wb.save(nueva_ruta_archivo)
            elif tipo_archivo in ["jpg", "png"]:
                with open(nueva_ruta_archivo, "wb") as f:
                    f.write(b"")

            listar_archivos(entry_ruta.get())
            ventana_archivo.destroy()

        boton_confirmar = ctk.CTkButton(ventana_archivo, text="Crear", command=confirmar_creacion)
        boton_confirmar.pack(padx=10, pady=10)

    boton_crear_archivo = ctk.CTkButton(frame, text="Crear Archivo", command=crear_archivo)
    boton_crear_archivo.grid(row=3, column=0, pady=10, padx=10)

    def on_close():
        global gestor_abierto
        procesos.unregister("Gestor de Archivos")
        gestor_abierto = False
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", on_close)
