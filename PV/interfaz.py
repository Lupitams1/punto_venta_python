import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog
from tkinter import ttk

class PuntoDeVentaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de Venta - Administración")
        self.root.geometry("600x400")

        # Títulos de las secciones
        self.label = tk.Label(self.root, text="Sistema de Administración de Inventario", font=("Arial", 16))
        self.label.pack(pady=10)

        # Crear botones
        self.boton_agregar_producto = tk.Button(self.root, text="Agregar Producto al Inventario", command=self.agregar_producto)
        self.boton_agregar_producto.pack(pady=10)

        self.boton_registrar_compra = tk.Button(self.root, text="Registrar Compra", command=self.registrar_compra)
        self.boton_registrar_compra.pack(pady=10)

        self.boton_generar_reporte_inventario = tk.Button(self.root, text="Generar Reporte de Inventario", command=self.generar_reporte_inventario)
        self.boton_generar_reporte_inventario.pack(pady=10)

        self.boton_generar_reporte_ventas = tk.Button(self.root, text="Generar Reporte de Ventas", command=self.generar_reporte_ventas)
        self.boton_generar_reporte_ventas.pack(pady=10)

    def agregar_producto(self):
        """Función para agregar productos al inventario"""
        def agregar():
            nombre_producto = entry_nombre_producto.get()
            cantidad_minima = entry_cantidad_minima.get()
            precio = entry_precio.get()

            if not nombre_producto or not cantidad_minima or not precio:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
                return

            # Insertar el producto en la base de datos
            # Aquí debe ir el código para insertar el producto en la base de datos
            messagebox.showinfo("Producto agregado", f"Producto {nombre_producto} agregado exitosamente.")
            ventana_agregar.destroy()

        # Crear ventana para ingresar los detalles del producto
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Producto")

        tk.Label(ventana_agregar, text="Nombre del Producto:").pack()
        entry_nombre_producto = tk.Entry(ventana_agregar)
        entry_nombre_producto.pack()

        tk.Label(ventana_agregar, text="Cantidad Mínima:").pack()
        entry_cantidad_minima = tk.Entry(ventana_agregar)
        entry_cantidad_minima.pack()

        tk.Label(ventana_agregar, text="Precio:").pack()
        entry_precio = tk.Entry(ventana_agregar)
        entry_precio.pack()

        boton_agregar = tk.Button(ventana_agregar, text="Agregar Producto", command=agregar)
        boton_agregar.pack(pady=10)

    def registrar_compra(self):
        """Función para registrar una compra en el inventario"""
        def registrar():
            proveedor_id = entry_proveedor_id.get()
            producto_id = entry_producto_id.get()
            cantidad = entry_cantidad.get()
            precio_unitario = entry_precio_unitario.get()

            if not proveedor_id or not producto_id or not cantidad or not precio_unitario:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
                return

            # Registrar la compra y actualizar el inventario
            # Aquí debe ir el código para registrar la compra en la base de datos
            messagebox.showinfo("Compra registrada", "Compra registrada exitosamente.")
            ventana_compra.destroy()

        # Crear ventana para ingresar los detalles de la compra
        ventana_compra = tk.Toplevel(self.root)
        ventana_compra.title("Registrar Compra")

        tk.Label(ventana_compra, text="Proveedor ID:").pack()
        entry_proveedor_id = tk.Entry(ventana_compra)
        entry_proveedor_id.pack()

        tk.Label(ventana_compra, text="Producto ID:").pack()
        entry_producto_id = tk.Entry(ventana_compra)
        entry_producto_id.pack()

        tk.Label(ventana_compra, text="Cantidad:").pack()
        entry_cantidad = tk.Entry(ventana_compra)
        entry_cantidad.pack()

        tk.Label(ventana_compra, text="Precio Unitario:").pack()
        entry_precio_unitario = tk.Entry(ventana_compra)
        entry_precio_unitario.pack()

        boton_registrar = tk.Button(ventana_compra, text="Registrar Compra", command=registrar)
        boton_registrar.pack(pady=10)

    def generar_reporte_inventario(self):
        """Generar reporte de inventario en Excel"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.nombre, i.cantidad_disponible, i.cantidad_minima
            FROM inventario i
            JOIN productos p ON i.producto_id = p.producto_id
        """)
        inventario = cursor.fetchall()
        cursor.close()

        df = pd.DataFrame(inventario, columns=["Producto", "Stock Disponible", "Stock Mínimo"])
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if filename:
            df.to_excel(filename, index=False)
            messagebox.showinfo("Reporte generado", f"Reporte de inventario guardado en {filename}")

    def generar_reporte_ventas(self):
        """Generar reporte de ventas en Excel"""
        fecha_inicio = filedialog.askstring("Fecha Inicio", "Ingrese la fecha de inicio (YYYY-MM-DD):")
        fecha_fin = filedialog.askstring("Fecha Fin", "Ingrese la fecha de fin (YYYY-MM-DD):")

        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.venta_id, v.fecha_venta, c.nombre AS cliente, v.total
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.cliente_id
            WHERE v.fecha_venta BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        cursor.close()

        df = pd.DataFrame(ventas, columns=["Venta ID", "Fecha de Venta", "Cliente", "Total"])
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

        if filename:
            df.to_excel(filename, index=False)
            messagebox.showinfo("Reporte generado", f"Reporte de ventas guardado en {filename}")

# Crear la ventana principal
root = tk.Tk()
app = PuntoDeVentaApp(root)
root.mainloop()
