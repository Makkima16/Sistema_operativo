import hashlib
import sqlite3

import customtkinter as ctk

from kernel.config import ensure_user_dirs
from kernel.db import get_connection


def encriptar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()


def guardar_credenciales(usuario, contrasena, rol):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios VALUES (?, ?, ?)",
            (usuario, encriptar_contrasena(contrasena), rol),
        )
        conn.commit()
    finally:
        conn.close()

    ensure_user_dirs(usuario)


def cargar_credenciales():
    credenciales = {}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    for usuario, contrasena_hash, rol in cursor.fetchall():
        credenciales[usuario] = (contrasena_hash, rol)
    conn.close()
    return credenciales


def verificar_credenciales(usuario, contrasena):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    return bool(resultado and resultado[0] == encriptar_contrasena(contrasena))


def obtener_rol(usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def abrir_ventana_crear_usuario(parent):
    ventana_crear_usuario = ctk.CTkToplevel(parent)
    ventana_crear_usuario.title("Crear Nuevo Usuario")
    ventana_crear_usuario.geometry("400x400")
    ventana_crear_usuario.attributes("-topmost", True)

    etiqueta_usuario = ctk.CTkLabel(ventana_crear_usuario, text="Nombre de Usuario", font=("Arial", 16))
    etiqueta_usuario.pack(pady=10)

    entry_nuevo_usuario = ctk.CTkEntry(ventana_crear_usuario, placeholder_text="Nuevo Usuario")
    entry_nuevo_usuario.pack(pady=10)

    etiqueta_contrasena = ctk.CTkLabel(ventana_crear_usuario, text="Contraseña", font=("Arial", 16))
    etiqueta_contrasena.pack(pady=10)

    entry_nueva_contrasena = ctk.CTkEntry(ventana_crear_usuario, placeholder_text="Nueva Contraseña", show="*")
    entry_nueva_contrasena.pack(pady=10)

    etiqueta_rol = ctk.CTkLabel(ventana_crear_usuario, text="Rol", font=("Arial", 16))
    etiqueta_rol.pack(pady=10)

    combo_rol = ctk.CTkComboBox(ventana_crear_usuario, values=["Administrador", "Usuario"])
    combo_rol.pack(pady=10)

    etiqueta_resultado = ctk.CTkLabel(ventana_crear_usuario, text="")
    etiqueta_resultado.pack(pady=10)

    def guardar_usuario():
        usuario = entry_nuevo_usuario.get().strip()
        contrasena = entry_nueva_contrasena.get()
        rol = combo_rol.get()

        if not (usuario and contrasena and rol):
            etiqueta_resultado.configure(text="Ingrese usuario, contraseña y rol.")
            return

        try:
            guardar_credenciales(usuario, contrasena, rol)
        except sqlite3.IntegrityError:
            etiqueta_resultado.configure(text="Ese usuario ya existe.")
            return

        etiqueta_resultado.configure(text="Usuario creado exitosamente.")
        ventana_crear_usuario.destroy()

    boton_guardar = ctk.CTkButton(
        ventana_crear_usuario,
        text="Guardar Usuario",
        command=guardar_usuario,
    )
    boton_guardar.pack(pady=10)
