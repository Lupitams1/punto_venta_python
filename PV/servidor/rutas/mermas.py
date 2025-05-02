from fastapi import APIRouter, HTTPException
from servidor.db_mysql import get_connection
from servidor.modelos import MermaEntrada
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import requests

router = APIRouter()

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
