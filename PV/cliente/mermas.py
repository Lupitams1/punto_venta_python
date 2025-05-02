import tkinter as tk
from tkinter import messagebox
import requests

libros = []

def cargar_libros():
    global libros
    response = requests.get("http://localhost:8000/libros")
    if response.status_code == 200:
        libros = response.json()
        lista_libros.delete(0, tk.END)
        for l in libros:
            lista_libros.insert(tk.END, f"{l['id']}. {l['titulo']} - Stock: {l['stock']}")
    else:
        messagebox.showerror("Error", "No se pudo cargar libros.")

def registrar_merma():
    seleccion = lista_libros.curselection()
    if not seleccion:
        messagebox.showwarning("Selecciona un libro", "Debes seleccionar un libro.")
        return

    libro = libros[seleccion[0]]
    try:
        cantidad = int(entry_cantidad.get())
        if cantidad <= 0:
            raise ValueError
        if cantidad > libro["stock"]:
            messagebox.showwarning("Error", "La cantidad excede el stock.")
            return
    except ValueError:
        messagebox.showerror("Error", "Cantidad inválida.")
        return

    motivo = entry_motivo.get()
    data = {
        "id_libro": libro["id"],
        "cantidad": cantidad,
        "motivo": motivo
    }

    response = requests.post("http://localhost:8000/mermas", json=data)
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Merma registrada.")
        entry_cantidad.delete(0, tk.END)
        entry_motivo.delete(0, tk.END)
        cargar_libros()
    else:
        messagebox.showerror("Error", response.text)

# Interfaz
root = tk.Tk()
root.title("Registrar Merma")

tk.Label(root, text="Libros en inventario").pack()
lista_libros = tk.Listbox(root, width=50, height=15)
lista_libros.pack()

tk.Label(root, text="Cantidad de merma:").pack()
entry_cantidad = tk.Entry(root)
entry_cantidad.pack()

tk.Label(root, text="Motivo de la merma:").pack()
entry_motivo = tk.Entry(root, width=50)
entry_motivo.pack()

tk.Button(root, text="Registrar Merma", command=registrar_merma).pack(pady=10)

cargar_libros()
root.mainloop()
def exportar_mermas_excel_cmd():
    try:
        archivo = exportar_mermas_excel()
        messagebox.showinfo("Exportado", f"Exportado a {archivo}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def exportar_mermas_pdf_cmd():
    try:
        archivo = exportar_mermas_pdf()
        messagebox.showinfo("Exportado", f"Exportado a {archivo}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(frame_mermas, text="Exportar a Excel", command=exportar_mermas_excel_cmd).pack(pady=5)
tk.Button(frame_mermas, text="Exportar a PDF", command=exportar_mermas_pdf_cmd).pack(pady=5)



