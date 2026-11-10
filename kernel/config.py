from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "usuarios.db"
USERS_DIR = PROJECT_ROOT / "users"
IMAGES_DIR = PROJECT_ROOT / "imagenes"

SUB_DIRS = ["Documentos", "Musica", "Descargas", "Imagenes", "Videos"]

API_KEY = "663e66b760396f9d2f0198dd1483e3e0"
CIUDAD = "Ibague"
URL_CLIMA = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"


def get_user_dir(usuario):
    return USERS_DIR / usuario


def ensure_user_dirs(usuario):
    base = get_user_dir(usuario)
    base.mkdir(parents=True, exist_ok=True)
    for carpeta in SUB_DIRS:
        (base / carpeta).mkdir(parents=True, exist_ok=True)
    return base


def image_path(nombre):
    return IMAGES_DIR / nombre
