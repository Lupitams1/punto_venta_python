from servidor.modelos import Libro


db = []
ventas_realizadas = []

def crear_tabla():
    # Simulación inicial de libros
    db.extend([
        Libro(id=1, titulo="Cien Años de Soledad", autor="Gabriel García Márquez",
              categoria="Novela", precio=150.00, stock=10, stock_min=3, stock_max=20),
        Libro(id=2, titulo="El Principito", autor="Antoine de Saint-Exupéry",
              categoria="Infantil", precio=90.00, stock=5, stock_min=2, stock_max=15),
    ])
