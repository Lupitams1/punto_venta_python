from cliente.usuarios import interfaz_usuarios
tab_usuarios = ttk.Frame(notebook)
notebook.add(tab_usuarios, text="Usuarios")
interfaz_usuarios(tab_usuarios)

def iniciar_interfaz(usuario, rol):
    root = tk.Tk()
    root.title(f"Punto de Venta - Usuario: {usuario} (Rol: {rol})")
    
    # Ejemplo: desactivar pestaña de reportes para vendedores
    if rol == "vendedor":
        # Ocultar pestaña de reportes
        notebook = ttk.Notebook(root)
        # Agrega solo pestañas de venta, no reportes ni exportaciones
    else:
        # Agrega todas las pestañas
        from cliente.reportes import cargar_reportes
        cargar_reportes(notebook)

    root.mainloop()
