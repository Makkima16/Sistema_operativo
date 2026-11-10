import psutil
import customtkinter as ctk

from kernel import procesos


def monitorear_recursos():
    ventana_recursos = ctk.CTkToplevel()
    ventana_recursos.geometry("600x400")
    ventana_recursos.title("Monitoreo de Recursos y Procesos")

    label_recursos = ctk.CTkLabel(ventana_recursos, text="Monitoreo de Recursos", font=("Arial", 16))
    label_recursos.pack(pady=10)

    label_recursos_text = ctk.CTkLabel(ventana_recursos, text="", font=("Arial", 14))
    label_recursos_text.pack(pady=10)

    label_procesos_text = ctk.CTkLabel(ventana_recursos, text="Procesos Activos:", font=("Arial", 14))
    label_procesos_text.pack(pady=10)

    def actualizar_vista():
        lista = procesos.listar()
        texto = "\n".join(lista) if lista else "No hay procesos activos."
        label_procesos_text.configure(text=f"Procesos Activos:\n{texto}")

    procesos.suscribir(actualizar_vista)

    def actualizar_recursos():
        if not ventana_recursos.winfo_exists():
            return

        uso_cpu = psutil.cpu_percent(interval=None)
        memoria = psutil.virtual_memory()
        label_recursos_text.configure(
            text=(
                f"Uso de CPU: {uso_cpu}%\n"
                f"Uso de Memoria: {memoria.percent}% ({memoria.used // (1024 * 1024)} MB)"
            )
        )
        actualizar_vista()
        ventana_recursos.after(1000, actualizar_recursos)

    actualizar_vista()
    actualizar_recursos()
