import tkinter as tk
from tkinter import messagebox
import requests

carrito = []
libros_disponibles = []

def cargar_libros():
    global libros_disponibles
    response = requests.get("http://localhost:8000/libros")
    if response.status_code == 200:
        libros_disponibles = response.json()
        lista_libros.delete(0, tk.END)
        for l in libros_disponibles:
            lista_libros.insert(tk.END, f"{l['id']}. {l['titulo']} - {l['categoria']} - ${l['precio']:.2f} - Stock: {l['stock']}")
    else:
        messagebox.showerror("Error", "No se pudo cargar libros.")

def agregar_al_carrito():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona un libro.")
        return

    libro = libros_disponibles[seleccion[0]]
    try:
        cantidad = int(entry_cantidad.get())
        if cantidad <= 0:
            raise ValueError
        if cantidad > libro["stock"]:
            messagebox.showwarning("Stock insuficiente", "La cantidad excede el stock.")
            return
    except ValueError:
        messagebox.showerror("Error", "Cantidad inválida.")
        return

    carrito.append({"id_libro": libro["id"], "cantidad": cantidad})
    lista_carrito.insert(tk.END, f"{libro['titulo']} x {cantidad}")
    entry_cantidad.delete(0, tk.END)

def procesar_venta():
    if not carrito:
        messagebox.showwarning("Carrito vacío", "Agrega libros al carrito.")
        return

    email_cliente = entry_email.get().strip()
    data = {"items": carrito}
    if email_cliente:
        data["email"] = email_cliente

    response = requests.post("http://localhost:8000/ventas", json=data)
    if response.status_code == 200:
        remision = response.json()
        mostrar_remision(remision)
        carrito.clear()
        lista_carrito.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        cargar_libros()
    else:
        messagebox.showerror("Error", response.text)


def mostrar_remision(rem):
    ventana = tk.Toplevel()
    ventana.title("Nota de Remisión")
    msg = f"Fecha: {rem['fecha']}\n\n"
    for item in rem['items']:
        msg += f"{item}\n"
    msg += f"\nSubtotal: ${rem['subtotal']:.2f}"
    msg += f"\nIVA (16%): ${rem['iva']:.2f}"
    msg += f"\nTotal: ${rem['total']:.2f}"
    tk.Label(ventana, text=msg, justify="left").pack(padx=10, pady=10)

# Interfaz
root = tk.Tk()
root.title("Ventas - Punto de Venta de Libros")

frame_libros = tk.Frame(root)
frame_libros.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(frame_libros, text="Libros disponibles").pack()
lista_libros = tk.Listbox(frame_libros, width=50, height=15)
lista_libros.pack()

tk.Label(frame_libros, text="Cantidad:").pack()
entry_cantidad = tk.Entry(frame_libros)
entry_cantidad.pack()

tk.Button(frame_libros, text="Agregar al carrito", command=agregar_al_carrito).pack(pady=5)

frame_carrito = tk.Frame(root)
frame_carrito.pack(side=tk.RIGHT, padx=10, pady=10)

tk.Label(frame_carrito, text="Carrito de compras").pack()
lista_carrito = tk.Listbox(frame_carrito, width=40, height=15)
lista_carrito.pack()

tk.Button(frame_carrito, text="Procesar venta", command=procesar_venta).pack(pady=10)
tk.Label(frame_carrito, text="Correo electrónico (opcional):").pack()
entry_email = tk.Entry(frame_carrito, width=40)
entry_email.pack(pady=5)

cargar_libros()
root.mainloop()
