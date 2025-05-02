import tkinter as tk
from tkinter import ttk
import requests
from .ventas import agregar_al_carrito, procesar_venta

class VentanaVentas:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de Venta - Libros")
        self.carrito = []

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("Autor", "Categoría", "Precio", "Stock"), show="headings")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack()

        self.cantidad_label = tk.Label(self.frame, text="Cantidad:")
        self.cantidad_label.pack(pady=(10, 0))

        self.cantidad_entry = tk.Entry(self.frame)
        self.cantidad_entry.pack()

        self.btn_agregar = tk.Button(self.frame, text="Agregar al carrito", command=self.agregar_item)
        self.btn_agregar.pack(pady=5)

        self.btn_comprar = tk.Button(self.frame, text="Procesar venta", command=self.vender)
        self.btn_comprar.pack(pady=10)

        self.status = tk.Label(self.frame, text="", fg="green")
        self.status.pack()

        self.cargar_libros()

    def cargar_libros(self):
        response = requests.get("http://localhost:8000/libros")
        if response.status_code == 200:
            self.libros = response.json()
            for libro in self.libros:
                self.tree.insert("", tk.END, iid=libro["id"], values=(libro["autor"], libro["categoria"], libro["precio"], libro["stock"]))

    def agregar_item(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            self.status.config(text="Selecciona un libro.")
            return
        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            self.status.config(text="Cantidad inválida.")
            return

        libro_id = int(seleccionado)
        agregar_al_carrito(libro_id, cantidad)
        self.status.config(text=f"Agregado al carrito.")

    def vender(self):
        procesar_venta()
        self.status.config(text="Venta procesada.")
        self.root.destroy()

# Para probarlo individualmente
if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana
