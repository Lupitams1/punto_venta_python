import tkinter as tk
import requests
from cliente.login import mostrar_login


def iniciar_app(usuario, rol):
    from cliente.app import iniciar_interfaz
    iniciar_interfaz(usuario, rol)

if __name__ == "__main__":
    mostrar_login(iniciar_app)

def cargar_libros():
    response = requests.get("http://localhost:8000/libros")
    if response.status_code == 200:
        libros = response.json()
        lista.delete(0, tk.END)
        for l in libros:
            estado = ""
            if l['stock'] <= l['stock_min']:
                estado = "⚠ Bajo stock"
            elif l['stock'] > l['stock_max']:
                estado = "❗ Sobre stock"
            lista.insert(tk.END, f"{l['titulo']} - {l['categoria']} - Stock: {l['stock']} {estado}")

root = tk.Tk()
root.title("Catálogo de Libros")
root.geometry("500x400")

tk.Button(root, text="Cargar Libros", command=cargar_libros).pack(pady=10)

lista = tk.Listbox(root, width=60)
lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

cargar_libros()
root.mainloop()
