import tkinter as tk
from tkinter import ttk
import requests

def cargar_historial():
    response = requests.get("http://localhost:8000/ventas/historial")
    if response.status_code == 200:
        ventas = response.json()
        for venta in ventas:
            tree.insert("", tk.END, values=(
                venta["fecha"],
                "\n".join(venta["items"]),
                f"${venta['subtotal']:.2f}",
                f"${venta['iva']:.2f}",
                f"${venta['total']:.2f}",
                venta.get("email", ""),
                venta.get("telefono", "")
            ))
    else:
        print("Error al obtener historial")

root = tk.Tk()
root.title("Historial de Ventas")

cols = ("Fecha", "Libros", "Subtotal", "IVA", "Total", "Email", "Teléfono")
tree = ttk.Treeview(root, columns=cols, show="headings")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100 if col != "Libros" else 300)

tree.pack(fill=tk.BOTH, expand=True)

cargar_historial()
root.mainloop()
