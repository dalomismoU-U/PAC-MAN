import tkinter as tk

# --- CONFIGURACIÓN ---
TAM_CELDA = 24
ANCHO, ALTO = 28 * TAM_CELDA, 31 * TAM_CELDA

# --- COLORES ---
AZUL = "#2121FF"
NEGRO = "#000000"
BLANCO = "#FFFFFF"
AMARILLO = "#FFFF00"
GRIS = "#323232"

# --- MAPA CLÁSICO ORIGINAL (28x31) ---
# Basado en la disposición auténtica del arcade original
mapa_numerico = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0],
[0,2,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,2,0],
[0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0],
[0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0],
[0,1,1,1,1,1,1,1,0,0,0,0,3,3,3,3,0,0,0,0,1,1,1,1,1,1,1,0],
[0,0,0,0,0,1,0,0,0,0,0,1,3,3,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
[0,0,0,0,0,1,0,0,0,0,0,1,3,3,0,0,1,0,0,0,0,0,0,1,0,0,0,0],
[0,0,0,0,0,1,0,0,3,3,3,0,0,0,3,3,3,3,0,0,3,3,0,1,0,0,0,0],
[0,0,0,0,0,1,0,0,3,3,3,0,0,0,3,3,3,3,0,0,3,3,0,1,0,0,0,0],
[0,0,0,0,0,1,0,0,3,3,3,0,0,0,3,3,3,3,0,0,3,3,0,1,0,0,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0],
[0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0],
[0,2,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,2,0],
[0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0],
[0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0],
[0,1,1,1,1,1,1,1,0,0,0,0,3,3,3,3,0,0,0,0,1,1,1,1,1,1,1,0],
[0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,0],
[0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]


# Convertir el mapa numérico a un mapa de caracteres que usa el resto del código
# 0 -> muro (#), 1 -> pellet (.), 2 -> power pellet (O), 3 -> espacio vacío ( )
NUM_TO_CHAR = {0: "#", 1: ".", 2: "O", 3: " "}

# `mapa` es la representación usada por el resto del proyecto (lista de listas de caracteres)
mapa = [[NUM_TO_CHAR.get(c, " ") for c in fila] for fila in mapa_numerico]

# --- FUNCIÓN PARA DIBUJAR EL MAPA ---
def dibujar_mapa(canvas):
    """Dibuja el mapa sobre el canvas.

    Esta función es importable y no asume la existencia de una ventana global.
    """
    canvas.delete("all")
    for fila_idx, fila in enumerate(mapa):
        for col_idx, celda in enumerate(fila):
            x = col_idx * TAM_CELDA
            y = fila_idx * TAM_CELDA
            if celda == "#":
                canvas.create_rectangle(x, y, x + TAM_CELDA, y + TAM_CELDA, fill=AZUL, outline=AZUL)
            elif celda == ".":
                cx, cy = x + TAM_CELDA // 2, y + TAM_CELDA // 2
                canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=BLANCO, outline=BLANCO)
            elif celda == "O":
                cx, cy = x + TAM_CELDA // 2, y + TAM_CELDA // 2
                canvas.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill=BLANCO, outline=BLANCO)
            elif celda == " ":
                pass  # espacio libre
            # Posición inicial de Pac-Man (centro inferior)
            if fila_idx == 17 and col_idx == 13:
                cx, cy = x + TAM_CELDA // 2, y + TAM_CELDA // 2
                canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8, fill=AMARILLO, outline=AMARILLO)

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Pac-Man - Mapa clásico original")
    ventana.geometry(f"{ANCHO}x{ALTO}")
    ventana.resizable(False, False)
    
    canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg=NEGRO, highlightthickness=0)
    canvas.pack()
    
    def actualizar():
        dibujar_mapa(canvas)
        ventana.after(33, actualizar)
    
    actualizar()
    ventana.mainloop()

