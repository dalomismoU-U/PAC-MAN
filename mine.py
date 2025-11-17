import tkinter as tk
from tkinter import Canvas, filedialog
import sys
import random
import os
import mapa

# Intentar usar Pillow (PIL) para escalado de imágenes si está disponible
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# Contenedor de imágenes cargadas (PhotoImage o ImageTk.PhotoImage)
IMAGES = {}
# Factor de escala para sprites de personaje (relativo a TAM_CELDA)
CHARACTER_SCALE = 1.5

def cargar_imagenes():
    """Carga imágenes desde la carpeta `assets/` si existen.

    Archivos soportados (nombres sugeridos):
    - pacman.png
    - pellet.png
    - power_pellet.png
    - wall.png
    - ghost_red.png
    - ghost_pink.png
    - ghost_blue.png
    - ghost_orange.png
    """
    global IMAGES
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    names = {
        "pacman": "pacman.png",
        "pellet": "pellet.png",
        "power": "power_pellet.png",
        "wall": "wall.png",
        "ghost_rojo": "ghost_red.png",
        "ghost_rosa": "ghost_pink.png",
        "ghost_azul": "ghost_blue.png",
        "ghost_naranja": "ghost_orange.png",
    }
    # tamaños por clave: por defecto tile = TAM_CELDA, characters = TAM_CELDA * CHARACTER_SCALE
    sizes = {}
    for k in names.keys():
        if k in ("pacman", "ghost_rojo", "ghost_rosa", "ghost_azul", "ghost_naranja"):
            sizes[k] = (int(TAM_CELDA * CHARACTER_SCALE), int(TAM_CELDA * CHARACTER_SCALE))
        else:
            sizes[k] = (TAM_CELDA, TAM_CELDA)

    for key, fname in names.items():
        path = os.path.join(assets_dir, fname)
        if os.path.exists(path):
            try:
                if PIL_AVAILABLE:
                    img = Image.open(path).convert("RGBA")
                    # Escalar conservando la relación de aspecto dentro del cuadro 'size'
                    size = sizes.get(key, (TAM_CELDA, TAM_CELDA))
                    # thumbnail mantiene aspecto y modifica img in-place
                    try:
                        resample = Image.Resampling.LANCZOS
                    except AttributeError:
                        resample = Image.ANTIALIAS
                    img.thumbnail(size, resample)
                    # Crear un fondo transparente del tamaño objetivo y centrar la imagen
                    bg = Image.new("RGBA", size, (0, 0, 0, 0))
                    ox = (size[0] - img.width) // 2
                    oy = (size[1] - img.height) // 2
                    bg.paste(img, (ox, oy), img)
                    IMAGES[key] = ImageTk.PhotoImage(bg)
                else:
                    IMAGES[key] = tk.PhotoImage(file=path)
            except Exception:
                # si falla la carga, ignorar y seguir con el fallback gráfico
                pass


def cargar_imagen_desde_ruta(path, key):
    """Carga una imagen desde `path` y la asigna a IMAGES[key].

    Retorna True si la carga tuvo éxito, False en caso contrario.
    """
    if not path or not os.path.exists(path):
        return False
    try:
        # Determinar tamaño objetivo según la clave
        if key in ("pacman", "ghost_rojo", "ghost_rosa", "ghost_azul", "ghost_naranja"):
            size = (int(TAM_CELDA * CHARACTER_SCALE), int(TAM_CELDA * CHARACTER_SCALE))
        else:
            size = (TAM_CELDA, TAM_CELDA)

        if PIL_AVAILABLE:
            img = Image.open(path).convert("RGBA")
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.ANTIALIAS
            img.thumbnail(size, resample)
            bg = Image.new("RGBA", size, (0, 0, 0, 0))
            ox = (size[0] - img.width) // 2
            oy = (size[1] - img.height) // 2
            bg.paste(img, (ox, oy), img)
            IMAGES[key] = ImageTk.PhotoImage(bg)
        else:
            IMAGES[key] = tk.PhotoImage(file=path)
        return True
    except Exception:
        return False


def seleccionar_imagen_y_cargar(key='pacman'):
    """Abre un diálogo para seleccionar una imagen y la carga en IMAGES[key].

    Uso: llamar `seleccionar_imagen_y_cargar('pacman')` desde el código (por ejemplo,
    antes de iniciar el juego) o enlazarlo a un botón en la UI.
    """
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("Todos los archivos", "*")],
    )
    if not ruta:
        return False
    return cargar_imagen_desde_ruta(ruta, key)

# --- CONFIGURACIÓN INICIAL ---
# No inicializamos pygame aquí para permitir llamar `main()` desde un menú.
# Usar el tamaño de celda y las dimensiones del mapa clásico
TAM_CELDA = mapa.TAM_CELDA
FPS = 8  # Velocidad del juego

# Colores
NEGRO = "#000000"
AZUL = "#0000FF"
AMARILLO = "#FFFF00"
BLANCO = "#FFFFFF"
ROJO = "#FF0000"
ROSA = "#FF6496"
CELESTE = "#00FFFF"
NARANJA = "#FF9600"

# --- TAMAÑO DEL MAPA ---
# Variables relacionadas con la ventana y el reloj. Se inicializan en main().
pantalla = None
COLUMNAS = len(mapa.mapa[0])
FILAS = len(mapa.mapa)
ANCHO = mapa.ANCHO
ALTO = mapa.ALTO

fuente = None
reloj = None

# --- VARIABLES DE JUEGO ---
x, y = 1, 1
puntos = 0
total_puntos = 0
vidas = 3
enemigos = []
power_mode = False
power_timer = 0
POWER_DURATION_SEC = 8  # segundos que dura el efecto del power pellet


# --- FUNCIONES ---
def cargar_mapa_clasico():
    """Carga el mapa clásico desde el módulo `mapa` y prepara el estado del juego."""
    global total_puntos, x, y, enemigos
    # Copiar la lista de filas (strings) como lista de listas (matriz)
    mapa_juego = [list(fila) for fila in mapa.mapa]

    # Posición inicial de Pac-Man según `mapa.py` (fila 17, columna 13)
    x, y = 13, 17

    # Contar puntos (pellets '.')
    total_puntos = sum(row.count('.') for row in mapa_juego)

    # Crear enemigos en celdas no muro
    enemigos = generar_enemigos(mapa_juego)
    return mapa_juego


def generar_enemigos(mapa):
    """Crea 4 enemigos con posiciones libres."""
    vacios = [
        (i, j)
        for j, fila in enumerate(mapa)
        for i, celda in enumerate(fila)
        # cualquier celda que no sea muro (#) es candidata
        if celda != "#" and (i, j) != (13, 17)
    ]
    random.shuffle(vacios)

    enemigos = []
    colores = [ROJO, ROSA, CELESTE, NARANJA]
    tipos = ["rojo", "rosa", "azul", "naranja"]

    for color, tipo in zip(colores, tipos):
        if vacios:
            pos = vacios.pop()
            enemigos.append({
                "x": pos[0],
                "y": pos[1],
                "color": color,
                "base_color": color,
                "tipo": tipo,
                "vulnerable": False,
            })
    return enemigos



def mover(dx, dy, mapa):
    """Mueve a Pac-Man solo si no hay paredes."""
    global x, y, puntos, total_puntos
    nuevo_x, nuevo_y = x + dx, y + dy

    if 0 <= nuevo_x < COLUMNAS and 0 <= nuevo_y < FILAS:
        if mapa[nuevo_y][nuevo_x] != "#":
            # Comer pellet pequeño
            if mapa[nuevo_y][nuevo_x] == ".":
                puntos += 1
                mapa[nuevo_y][nuevo_x] = " "
            # Comer power pellet -> activar power mode
            elif mapa[nuevo_y][nuevo_x] == "O":
                puntos += 10  # bonus por comer power pellet
                mapa[nuevo_y][nuevo_x] = " "
                activar_power_mode()
            x, y = nuevo_x, nuevo_y


def celda_valida(mapa, cx, cy):
    return 0 <= cx < COLUMNAS and 0 <= cy < FILAS and mapa[cy][cx] != "#"


def mover_enemigos(mapa):
    """Mueve cada enemigo según su tipo."""
    global enemigos, x, y

    nuevas_pos = []
    for e in enemigos:
        ex, ey = e["x"], e["y"]
        tipo = e["tipo"]

        # si está en power mode, el fantasma está vulnerable
        e["vulnerable"] = power_mode
        # cambiar color visual cuando es vulnerable
        if e["vulnerable"]:
            e["color"] = CELESTE
        else:
            e["color"] = e.get("base_color", e.get("color"))

        objetivo = None

        if tipo == "rojo":  # Persigue a Pac-Man
            objetivo = (x, y)
        elif tipo == "rosa":  # Apunta al frente de Pac-Man
            dx = x - ex
            dy = y - ey
            if abs(dx) > abs(dy):
                objetivo = (x + (1 if dx > 0 else -1) * 4, y)
            else:
                objetivo = (x, y + (1 if dy > 0 else -1) * 4)
        elif tipo == "azul":  # Intenta colocarse detrás de Pac-Man
            dx = x - ex
            dy = y - ey
            if abs(dx) > abs(dy):
                objetivo = (x - (1 if dx > 0 else -1) * 4, y)
            else:
                objetivo = (x, y - (1 if dy > 0 else -1) * 4)
        elif tipo == "naranja":  # Se mueve al azar
            objetivo = None

        # Movimiento hacia el objetivo (si existe)
        if objetivo:
            dx = objetivo[0] - ex
            dy = objetivo[1] - ey
            movs = []
            if abs(dx) > abs(dy):
                movs = [(1 if dx > 0 else -1, 0), (0, 1), (0, -1)]
            else:
                movs = [(0, 1 if dy > 0 else -1), (1, 0), (-1, 0)]
        else:
            movs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(movs)

        movido = False
        for dx, dy in movs:
            nx, ny = ex + dx, ey + dy
            if celda_valida(mapa, nx, ny):
                e["x"], e["y"] = nx, ny
                movido = True
                break

        if not movido:
            e["x"], e["y"] = ex, ey

        nuevas_pos.append(e)

    enemigos = nuevas_pos


def detectar_colision():
    """Detecta si Pac-Man toca a un enemigo.

    Devuelve el enemigo con el que colisiona o None.
    """
    for e in enemigos:
        if (x, y) == (e["x"], e["y"]):
            return e
    return None


def activar_power_mode():
    """Activa el modo power (fantasmas vulnerables)."""
    global power_mode, power_timer, enemigos
    power_mode = True
    power_timer = POWER_DURATION_SEC * FPS
    for e in enemigos:
        e["vulnerable"] = True
        e["color"] = CELESTE


def encontrar_pos_vacia(mapa):
    """Encuentra una posición vacía aleatoria para respawnear un fantasma."""
    vacios = [
        (i, j)
        for j, fila in enumerate(mapa)
        for i, celda in enumerate(fila)
        if celda == " " and not (i == x and j == y)
    ]
    if not vacios:
        return (13, 13)
    return random.choice(vacios)


# --- INICIO DEL JUEGO ---
def main():
    """Inicia el juego (puede ser llamado desde un menú)."""
    global pantalla, fuente, reloj, mapa_juego, puntos, vidas, enemigos, total_puntos, x, y, power_mode, power_timer

    ventana = tk.Tk()
    ventana.title("PAC-MAN con enemigos inteligentes y vidas")
    ventana.geometry(f"{ANCHO}x{ALTO}")
    ventana.resizable(False, False)
    
    canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg=NEGRO, highlightthickness=0)
    canvas.pack()

    # Cargar imágenes si existen en ./assets/ (opcional)
    cargar_imagenes()

    mapa_juego = cargar_mapa_clasico()
    
    teclas_presionadas = set()
    
    def on_key_press(event):
        teclas_presionadas.add(event.keysym.lower())
    
    def on_key_release(event):
        teclas_presionadas.discard(event.keysym.lower())
    
    ventana.bind('<KeyPress>', on_key_press)
    ventana.bind('<KeyRelease>', on_key_release)

    def actualizar_juego():
        global x, y, puntos, total_puntos, vidas, enemigos, power_mode, power_timer, mapa_juego

        # Movimiento del jugador
        if 'w' in teclas_presionadas:
            mover(0, -1, mapa_juego)
        if 's' in teclas_presionadas:
            mover(0, 1, mapa_juego)
        if 'a' in teclas_presionadas:
            mover(-1, 0, mapa_juego)
        if 'd' in teclas_presionadas:
            mover(1, 0, mapa_juego)
        if 'q' in teclas_presionadas:
            ventana.destroy()

        # Movimiento enemigos
        mover_enemigos(mapa_juego)
        # Colisión
        collided = detectar_colision()
        if collided:
            if power_mode and collided.get("vulnerable", False):
                puntos += 50
                nx, ny = encontrar_pos_vacia(mapa_juego)
                collided["x"], collided["y"] = nx, ny
                collided["vulnerable"] = False
                collided["color"] = collided.get("base_color", collided.get("color"))
            else:
                vidas -= 1
                if vidas > 0:
                    x, y = 13, 17
                else:
                    canvas.create_text(ANCHO // 2, ALTO // 2, text="¡Game Over!", font=("Arial", 40), fill=ROJO)
                    canvas.update()
                    ventana.after(2000, ventana.destroy)
                    return
                    vidas = 3
                    puntos = 0
                    mapa_juego = cargar_mapa_clasico()

        # Actualizar temporizador de power mode
        if power_mode:
            power_timer -= 1
            if power_timer <= 0:
                power_mode = False
                for e in enemigos:
                    e["vulnerable"] = False
                    e["color"] = e.get("base_color", e.get("color"))

        # Todos los puntos recolectados
        if puntos >= total_puntos and total_puntos > 0:
            canvas.create_text(ANCHO // 2, ALTO // 2, text="¡Nivel completado!", font=("Arial", 40), fill=CELESTE)
            canvas.update()
            ventana.after(1500)
            mapa_juego = cargar_mapa_clasico()
            puntos = 0

        # DIBUJAR
        canvas.delete("all")
        canvas.create_rectangle(0, 0, ANCHO, ALTO, fill=NEGRO, outline=NEGRO)
        
        # Dibujar el mapa
        for j, fila in enumerate(mapa_juego):
            for i, celda in enumerate(fila):
                cx = i * mapa.TAM_CELDA
                cy = j * mapa.TAM_CELDA
                center_x = cx + mapa.TAM_CELDA // 2
                center_y = cy + mapa.TAM_CELDA // 2
                if celda == "#":
                    if IMAGES.get('wall'):
                        canvas.create_image(center_x, center_y, image=IMAGES['wall'])
                    else:
                        canvas.create_rectangle(cx, cy, cx + mapa.TAM_CELDA, cy + mapa.TAM_CELDA, fill=AZUL, outline=AZUL)
                elif celda == ".":
                    if IMAGES.get('pellet'):
                        canvas.create_image(center_x, center_y, image=IMAGES['pellet'])
                    else:
                        ccx, ccy = center_x, center_y
                        canvas.create_oval(ccx - 2, ccy - 2, ccx + 2, ccy + 2, fill=BLANCO, outline=BLANCO)
                elif celda == "O":
                    if IMAGES.get('power'):
                        canvas.create_image(center_x, center_y, image=IMAGES['power'])
                    else:
                        ccx, ccy = center_x, center_y
                        canvas.create_oval(ccx - 5, ccy - 5, ccx + 5, ccy + 5, fill=BLANCO, outline=BLANCO)

        # Pac-Man
        px = x * mapa.TAM_CELDA + mapa.TAM_CELDA // 2
        py = y * mapa.TAM_CELDA + mapa.TAM_CELDA // 2
        if IMAGES.get('pacman'):
            canvas.create_image(px, py, image=IMAGES['pacman'])
        else:
            canvas.create_oval(px - 8, py - 8, px + 8, py + 8, fill=AMARILLO, outline=AMARILLO)

        # Enemigos
        for e in enemigos:
            ex = e["x"] * mapa.TAM_CELDA + mapa.TAM_CELDA // 2
            ey = e["y"] * mapa.TAM_CELDA + mapa.TAM_CELDA // 2
            key = f"ghost_{e['tipo']}"
            if IMAGES.get(key):
                canvas.create_image(ex, ey, image=IMAGES[key])
            else:
                canvas.create_oval(ex - 8, ey - 8, ex + 8, ey + 8, fill=e["color"], outline=e["color"])

        # HUD
        texto_puntos = f"Puntos: {puntos}/{total_puntos}"
        canvas.create_text(15, 15, text=texto_puntos, font=("Arial", 14), fill=BLANCO, anchor="nw")

        # Dibujar las vidas
        for i in range(vidas):
            vx = ANCHO - 150 + i * 30
            vy = 25
            canvas.create_oval(vx - 10, vy - 10, vx + 10, vy + 10, fill=AMARILLO, outline=AMARILLO)

        canvas.update()
        ventana.after(int(1000 / FPS), actualizar_juego)

    actualizar_juego()
    ventana.mainloop()


if __name__ == "__main__":
    main()
