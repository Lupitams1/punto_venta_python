from cliente.exportar import exportar_ventas_excel, exportar_ventas_pdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox
import requests

ventana = tk.Tk()
ventana.title("Reportes del Punto de Venta")
ventana.geometry("800x600")

notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

def exportar_excel():
    try:
        archivo = exportar_ventas_excel(entry_inicio.get(), entry_fin.get())
        messagebox.showinfo("Exportado", f"Exportado a {archivo}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def exportar_pdf():
    try:
        archivo = exportar_ventas_pdf(entry_inicio.get(), entry_fin.get())
        messagebox.showinfo("Exportado", f"Exportado a {archivo}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(frame_ventas, text="Exportar a Excel", command=exportar_excel).pack(pady=5)
tk.Button(frame_ventas, text="Exportar a PDF", command=exportar_pdf).pack(pady=5)

def graficar_ventas_por_fecha():
    fecha_inicio = entry_inicio.get()
    fecha_fin = entry_fin.get()
    
    try:
        url = f"http://localhost:8000/reportes/ventas?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}"
        resp = requests.get(url)
        if resp.status_code != 200:
            messagebox.showerror("Error", "No se pudo obtener las ventas.")
            return

        ventas = resp.json()["ventas"]

        fechas = [datetime.strptime(v["fecha"], "%Y-%m-%d").date() for v in ventas]
        totales = [v["total"] for v in ventas]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(fechas, totales, marker='o', linestyle='-', color='green')
        ax.set_title("Ventas por Fecha")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Total Vendido")
        ax.grid(True)
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Error", str(e))
        tk.Button(frame_graficos, text="Mostrar ventas por fecha", command=graficar_ventas_por_fecha).pack(pady=10)

