import pandas as pd
import requests

def exportar_ventas_excel(fecha_inicio, fecha_fin, archivo_salida="reporte_ventas.xlsx"):
    url = f"http://localhost:8000/reportes/ventas?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}"
    resp = requests.get(url)
    
    if resp.status_code != 200:
        raise Exception("Error al consultar ventas")

    datos = resp.json()
    df = pd.DataFrame(datos["ventas"])
    resumen = datos["resumen"]

    with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Ventas", index=False)
        resumen_df = pd.DataFrame([resumen])
        resumen_df.to_excel(writer, sheet_name="Resumen", index=False)
def exportar_top_excel(archivo_salida="libros_mas_vendidos.xlsx"):
    resp = requests.get("http://localhost:8000/reportes/libros_mas_vendidos")
    if resp.status_code != 200:
        raise Exception("Error al consultar libros más vendidos")

    datos = resp.json()
    df = pd.DataFrame(datos)
    df.to_excel(archivo_salida, index=False)
  

    return archivo_salida
