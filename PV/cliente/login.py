import tkinter as tk
from tkinter import messagebox
import requests

def mostrar_login(app_callback):
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("300x180")

    tk.Label(login_win, text="Usuario").pack(pady=5)
    entry_usuario = tk.Entry(login_win)
    entry_usuario.pack()

    tk.Label(login_win, text="Contraseña").pack(pady=5)
    entry_contrasena = tk.Entry(login_win, show="*")
    entry_contrasena.pack()

    def autenticar():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        datos = {"usuario": usuario, "contrasena": contrasena}
        resp = requests.post("http://localhost:8000/login", json=datos)

        if resp.status_code == 200 and resp.json().get("login"):
            rol = resp.json()["rol"]
            login_win.destroy()
            app_callback(usuario, rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(login_win, text="Iniciar sesión", command=autenticar).pack(pady=10)
    login_win.mainloop()
