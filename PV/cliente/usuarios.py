import tkinter as tk
from tkinter import ttk, messagebox
import requests

def interfaz_usuarios(master):
    frame = ttk.Frame(master)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("id", "nombre", "rol"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Usuario")
    tree.heading("rol", text="Rol")
    tree.pack(fill="both", expand=True)

    def cargar_usuarios():
        tree.delete(*tree.get_children())
        resp = requests.get("http://localhost:8000/usuarios")
        for u in resp.json()["usuarios"]:
            tree.insert("", "end", values=(u["id"], u["nombre_usuario"], u["rol"]))

    def agregar_usuario():
        nombre = entry_nombre.get()
        contra = entry_contra.get()
        rol = combo_rol.get()
        if not nombre or not contra:
            messagebox.showerror("Error", "Completa todos los campos.")
            return
        datos = {"nombre_usuario": nombre, "contrasena": contra, "rol": rol}
        resp = requests.post("http://localhost:8000/usuarios", json=datos)
        if resp.status_code == 200:
            cargar_usuarios()
            entry_nombre.delete(0, tk.END)
            entry_contra.delete(0, tk.END)

    def eliminar_usuario():
        selected = tree.selection()
        if not selected:
            return
        id_usuario = tree.item(selected[0])["values"][0]
        requests.delete(f"http://localhost:8000/usuarios/{id_usuario}")
        cargar_usuarios()

    def cambiar_rol():
        selected = tree.selection()
        if not selected:
            return
        id_usuario = tree.item(selected[0])["values"][0]
        nuevo_rol = combo_rol.get()
        requests.put(f"http://localhost:8000/usuarios/{id_usuario}", json={"rol": nuevo_rol})
        cargar_usuarios()

    frame_form = ttk.Frame(frame)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Usuario").grid(row=0, column=0)
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Contraseña").grid(row=1, column=0)
    entry_contra = tk.Entry(frame_form, show="*")
    entry_contra.grid(row=1, column=1)

    tk.Label(frame_form, text="Rol").grid(row=2, column=0)
    combo_rol = ttk.Combobox(frame_form, values=["admin", "vendedor"])
    combo_rol.grid(row=2, column=1)
    combo_rol.current(0)

    ttk.Button(frame_form, text="Agregar", command=agregar_usuario).grid(row=3, column=0, pady=5)
    ttk.Button(frame_form, text="Eliminar", command=eliminar_usuario).grid(row=3, column=1)
    ttk.Button(frame_form, text="Cambiar rol", command=cambiar_rol).grid(row=3, column=2)

    cargar_usuarios()
