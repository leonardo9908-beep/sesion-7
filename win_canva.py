import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_open_meteo():
    """Conecta con la API de Open-Meteo (Clima actual - últimas 24h)."""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=21.12&longitude=-101.68"
            "&hourly=temperature_2m&past_days=1&timezone=auto"
        )
        resp = requests.get(url, timeout=15, headers={"User-Agent": "CursoPC/1.0"})
        resp.raise_for_status()
        data = resp.json()
        horas = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]
        return horas, temps
    except Exception as e:
        messagebox.showerror("Error Open-Meteo", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def fetch_nasa_power():
    """Conecta con la API de NASA POWER (Datos históricos / T2M)."""
    try:
        url = (
            "https://power.larc.nasa.gov/api/temporal/hourly/point"
            "?parameters=T2M&community=RE&latitude=21.12&longitude=-101.68"
            "&start=20240901&end=20240902&format=JSON"
        )
        r = requests.get(url, timeout=20, headers={"User-Agent": "CursoPC/1.0"})
        r.raise_for_status()
        data = r.json()
        series = data["properties"]["parameter"]["T2M"]
        horas = list(series.keys())
        valores = list(series.values())
        return horas, valores
    except Exception as e:
        messagebox.showerror("Error NASA POWER", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def create_line_chart(horas, temps):
    """Gráfica de línea para Open-Meteo con fondo azul personalizado."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    
    # Fondo azul personalizado para la gráfica
    ax.set_facecolor("#e8f4f8")
    
    ax.plot(horas, temps, marker="o", linewidth=1.5, color="#1f77b4")
    ax.set_title("Temperatura Open-Meteo (Últimas 24h)")
    ax.set_xlabel("Hora")
    ax.set_ylabel("°C")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, linestyle="--", alpha=0.5, color="white")
    
    fig.tight_layout()
    return fig


def create_bar_chart(horas, valores):
    """Gráfica de barras para NASA POWER con fondo azul personalizado."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    
    # Fondo azul personalizado para la gráfica
    ax.set_facecolor("#e8f4f8")
    
    ax.bar(horas, valores, color="#ff7f0e")
    ax.set_title("NASA POWER — T2M (°C) Histórico")
    ax.set_xlabel("Hora (UTC)")
    ax.set_ylabel("°C")
    ax.tick_params(axis="x", rotation=60)
    ax.grid(True, axis="y", linestyle="--", alpha=0.5, color="white")
    
    fig.tight_layout()
    return fig


def mostrar_graficas(frm):
    """Consulta ambas APIs e inserta las gráficas en el frame de Tkinter."""
    # Limpiar widgets previos si se vuelve a presionar el botón
    for widget in frm.winfo_children():
        if isinstance(widget, tk.Widget) and not isinstance(widget, ttk.Button):
            widget.destroy()

    # 1. Obtener y graficar Open-Meteo
    h_om, t_om = fetch_open_meteo()
    if h_om and t_om:
        fig1 = create_line_chart(h_om, t_om)
        canvas1 = FigureCanvasTkAgg(fig1, master=frm)
        canvas1.draw()
        canvas1.get_tk_widget().pack(pady=10, fill="x")

    # 2. Obtener y graficar NASA POWER
    h_nasa, v_nasa = fetch_nasa_power()
    if h_nasa and v_nasa:
        fig2 = create_bar_chart(h_nasa, v_nasa)
        canvas2 = FigureCanvasTkAgg(fig2, master=frm)
        canvas2.draw()
        canvas2.get_tk_widget().pack(pady=10, fill="x")


def open_win_canvas(parent: tk.Tk):
    """
    Crea la ventana secundaria con gráficas de múltiples APIs.
    """
    win = tk.Toplevel(parent)
    win.title("Canvas con Open-Meteo y NASA POWER")
    win.geometry("960x1050")

    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)

    # Botón para cargar datos de ambas APIs y graficar
    ttk.Button(frm, text="Cargar y mostrar gráficas (APIs Múltiples)", command=lambda: mostrar_graficas(frm)).pack(pady=10)


# Para pruebas independientes (opcional)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba win_canvas")
    ttk.Button(root, text="Abrir ventana Canvas", command=lambda: open_win_canvas(root)).pack(pady=20)
    root.mainloop()