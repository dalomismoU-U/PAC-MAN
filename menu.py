import tkinter as tk
from tkinter import Canvas
import sys
import os
import mine

# Intentar usar Pillow localmente para cargar JPG/PNG mejor que tk.PhotoImage
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def dibujar_texto(canvas, texto, size, color, x, y):
    canvas.create_text(x, y, text=texto, font=("Arial", size), fill=color)


def menu():
    ventana = tk.Tk()
    ventana.title("PAC-MAN - Menú")
    ventana.geometry(f"{mine.ANCHO}x{mine.ALTO}")
    ventana.resizable(False, False)
    
    # Cargar imágenes del juego para la vista previa (opcional)
    try:
        mine.cargar_imagenes()
    except Exception:
        pass

    # Intentar cargar imagen de fondo 'donde-de-pantalla.jpg' en el directorio del proyecto
    ventana.bg_image = None
    ventana.bg_load_error = False
    posible_ruta = os.path.join(os.path.dirname(__file__), "donde-de-pantalla.jpg")
    if os.path.exists(posible_ruta):
        try:
            # Preferir Pillow local si está disponible
            if PIL_AVAILABLE:
                img = Image.open(posible_ruta).convert("RGBA")
                size = (mine.ANCHO, mine.ALTO)
                if hasattr(Image, 'Resampling'):
                    img = img.resize(size, Image.Resampling.LANCZOS)
                else:
                    img = img.resize(size, Image.ANTIALIAS)
                ventana.bg_image = ImageTk.PhotoImage(img)
            else:
                # Intentar con tk.PhotoImage para formatos compatibles (PNG/GIF/PPM)
                ext = os.path.splitext(posible_ruta)[1].lower()
                if ext in ['.png', '.gif', '.ppm', '.pgm']:
                    ventana.bg_image = tk.PhotoImage(file=posible_ruta)
                else:
                    ventana.bg_image = None
                    ventana.bg_load_error = True
        except Exception:
            ventana.bg_image = None
            ventana.bg_load_error = True

    canvas = Canvas(ventana, width=mine.ANCHO, height=mine.ALTO, bg="#000000", highlightthickness=0)
    canvas.pack()
    
    opciones = ["Iniciar juego", "Instrucciones", "Salir"]
    seleccionado = [0]
    
    def dibujar_menu():
        canvas.delete("all")
        # Dibujar fondo: imagen si existe, si no color negro
        if getattr(ventana, 'bg_image', None):
            canvas.create_image(0, 0, image=ventana.bg_image, anchor='nw')
        else:
            canvas.create_rectangle(0, 0, mine.ANCHO, mine.ALTO, fill="#000000", outline="#000000")
            # Mostrar mensaje discreto si la imagen existe pero no pudo cargarse
            if getattr(ventana, 'bg_load_error', False):
                mensaje = "Fondo no cargado: instala Pillow o usa PNG/GIF"
                canvas.create_text(mine.ANCHO // 2, mine.ALTO - 20, text=mensaje, font=("Arial", 12), fill="#BBBBBB")

        # --- Vista previa de imágenes (fallback a formas si faltan) ---
        IMAGES = getattr(mine, 'IMAGES', {})

        # Pac-Man -- centro arriba
        pac_x = mine.ANCHO // 2
        pac_y = 110
        if IMAGES.get('pacman'):
            canvas.create_image(pac_x, pac_y, image=IMAGES['pacman'])
        else:
            canvas.create_oval(pac_x - 18, pac_y - 18, pac_x + 18, pac_y + 18, fill="#FFFF00", outline="#FFFF00")

        # Fantasmas -- fila centrada
        ghosts = [('ghost_rojo', '#FF0000'), ('ghost_rosa', '#FF6496'), ('ghost_azul', '#00FFFF'), ('ghost_naranja', '#FF9600')]
        gap = 70
        total_width = gap * (len(ghosts) - 1)
        start_x = mine.ANCHO // 2 - total_width // 2
        gy = 170
        for i, (key, color) in enumerate(ghosts):
            gx = start_x + i * gap
            if IMAGES.get(key):
                canvas.create_image(gx, gy, image=IMAGES[key])
            else:
                canvas.create_oval(gx - 16, gy - 16, gx + 16, gy + 16, fill=color, outline=color)

        # Pellets junto a las opciones (a la izquierda)
        pellet_x = mine.ANCHO // 2 - 140
        for i in range(len(opciones)):
            py = 150 + i * 50
            if IMAGES.get('pellet'):
                canvas.create_image(pellet_x, py, image=IMAGES['pellet'])
            else:
                canvas.create_oval(pellet_x - 4, py - 4, pellet_x + 4, py + 4, fill="#FFFFFF", outline="#FFFFFF")
        
        dibujar_texto(canvas, "PAC-MAN", 50, "#FFFF00", mine.ANCHO // 2, 50)
        
        for i, op in enumerate(opciones):
            color = "#FFFFFF" if i != seleccionado[0] else "#FFC800"
            dibujar_texto(canvas, op, 30, color, mine.ANCHO // 2, 150 + i * 50)
    
    def manejar_tecla(event):
        if event.keysym == "Up":
            seleccionado[0] = (seleccionado[0] - 1) % len(opciones)
            dibujar_menu()
        elif event.keysym == "Down":
            seleccionado[0] = (seleccionado[0] + 1) % len(opciones)
            dibujar_menu()
        elif event.keysym == "Return" or event.keysym == "space":
            if opciones[seleccionado[0]] == "Iniciar juego":
                ventana.destroy()
                mine.main()
            elif opciones[seleccionado[0]] == "Instrucciones":
                mostrar_instrucciones(ventana, canvas)
            elif opciones[seleccionado[0]] == "Salir":
                ventana.destroy()
        # Cargar imagen del fantasma rojo con la tecla R
        elif event.keysym.lower() == 'r':
            try:
                # usar la función de selección de imagen en mine.py
                cargada = mine.seleccionar_imagen_y_cargar('ghost_rojo')
                if cargada:
                    # Si se cargó, redibujar el menú para mostrar la nueva imagen
                    dibujar_menu()
            except Exception:
                pass
    
    ventana.bind("<KeyPress>", manejar_tecla)
    dibujar_menu()
    ventana.mainloop()


def mostrar_instrucciones(ventana_padre, canvas_padre):
    ventana_inst = tk.Toplevel(ventana_padre)
    ventana_inst.title("Instrucciones")
    ventana_inst.geometry(f"{mine.ANCHO}x{mine.ALTO}")
    ventana_inst.resizable(False, False)
    
    canvas_inst = Canvas(ventana_inst, width=mine.ANCHO, height=mine.ALTO, bg="#000000", highlightthickness=0)
    canvas_inst.pack()
    
    instrucciones = [
        "WASD - Mover Pac-Man",
        "Q - Salir del juego",
        "Comer O activa power pellet (come fantasmas)",
        "Pulsa cualquier tecla para volver al menú",
    ]
    
    def dibujar_instrucciones():
        canvas_inst.delete("all")
        canvas_inst.create_rectangle(0, 0, mine.ANCHO, mine.ALTO, fill="#000000", outline="#000000")
        for i, linea in enumerate(instrucciones):
            dibujar_texto(canvas_inst, linea, 20, "#C8C8C8", 50, 120 + i * 40)
    
    def volver_menu(event):
        ventana_inst.destroy()
    
    ventana_inst.bind("<KeyPress>", volver_menu)
    dibujar_instrucciones()


if __name__ == "__main__":
    menu()
