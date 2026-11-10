_procesos = []
_suscriptores = []


def register(nombre):
    if nombre not in _procesos:
        _procesos.append(nombre)
        _notify()


def unregister(nombre):
    if nombre in _procesos:
        _procesos.remove(nombre)
        _notify()


def listar():
    return list(_procesos)


def suscribir(callback):
    _suscriptores.append(callback)


def _notify():
    for callback in list(_suscriptores):
        try:
            callback()
        except Exception:
            pass
