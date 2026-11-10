# gemOS

Sistema operativo de escritorio simulado en Python con interfaz gráfica (CustomTkinter).

## Funcionalidades

- Inicio de sesión y creación de usuarios con contraseñas cifradas (SHA-256).
- Escritorio con reloj, clima y accesos directos.
- Gestor de archivos por usuario (navegar, crear, abrir, editar y borrar archivos).
- Visor de PDF, imágenes, video y un reproductor de audio dedicado.
- Calculadora científica.
- Monitor de recursos (CPU, memoria y procesos activos).
- Descarga de videos y navegador integrado.
- Juego de la culebrita.

## Requisitos

Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

Los datos se guardan localmente en `usuarios.db` y `users/` (ignorados por git).

## Estructura

- `main.py` — punto de entrada.
- `Inicio/` — interfaz de inicio de sesión.
- `Escritorio/` — escritorio y calculadora.
- `Recursos/` — monitor de recursos y procesos.
- `Usuarios/` — autenticación y gestión de usuarios.
- `gestor/` — gestor de archivos y visores.
- `juegos/` — juego de la culebrita.
- `kernel/` — configuración, base de datos y registro de procesos.
- `imagenes/` — iconos de la interfaz.
