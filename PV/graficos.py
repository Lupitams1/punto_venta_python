frame_graficos = ttk.Frame(notebook)
notebook.add(frame_graficos, text="Gráficos")
def graficar_top_libros():
    resp = requests.get("http://localhost:8000/reportes/libros_mas_vendidos")
    if resp.status_code != 200:
        messagebox.showerror("Error", resp.text)
        return

    datos = resp.json()
    titulos = [libro["titulo"] for libro in datos]
    cantidades = [libro["total_vendidos"] for libro in datos]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(titulos, cantidades, color="skyblue")
    ax.set_title("Libros más vendidos")
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Título")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    tk.Button(frame_graficos, text="Mostrar libros más vendidos", command=graficar_top_libros).pack(pady=10)

