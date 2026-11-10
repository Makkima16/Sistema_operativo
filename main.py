from Inicio.inicioSesion import iniciar_interfaz
from kernel.config import DB_PATH
from kernel.db import create_database

if __name__ == "__main__":
    create_database(DB_PATH)
    iniciar_interfaz()
