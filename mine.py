import pygame
import sys
import random
import mapa

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
# Usar el tamaño de celda y las dimensiones del mapa clásico
TAM_CELDA = mapa.TAM_CELDA
FPS = 8  # Velocidad del juego

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 150)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ROSA = (255, 100, 150)
CELESTE = (0, 255, 255)
NARANJA = (255, 150, 0)

# --- TAMAÑO DEL MAPA ---
pantalla = pygame.display.set_mode((mapa.ANCHO, mapa.ALTO))
COLUMNAS = len(mapa.mapa[0])
FILAS = len(mapa.mapa)
ANCHO = mapa.ANCHO
ALTO = mapa.ALTO

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PAC-MAN con enemigos inteligentes y vidas")

fuente = pygame.font.SysFont("Arial", 24)
reloj = pygame.time.Clock()

# --- VARIABLES DE JUEGO ---
x, y = 1, 1
puntos = 0
total_puntos = 0
vidas = 3
enemigos = []


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
            enemigos.append({"x": pos[0], "y": pos[1], "color": color, "tipo": tipo})
    return enemigos



def dibujar_mapa_juego(surface, mapa_juego):
    """Dibuja el mapa_juego (matriz lista-de-listas) sobre la surface."""
    for j, fila in enumerate(mapa_juego):
        for i, celda in enumerate(fila):
            x = i * TAM_CELDA
            y = j * TAM_CELDA
            rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
            if celda == "#":
                pygame.draw.rect(surface, AZUL, rect)
            elif celda == ".":
                pygame.draw.circle(surface, BLANCO, rect.center, max(2, TAM_CELDA // 8))
            elif celda == "O":
                pygame.draw.circle(surface, BLANCO, rect.center, max(4, TAM_CELDA // 6))


def mover(dx, dy, mapa):
    """Mueve a Pac-Man solo si no hay paredes."""
    global x, y, puntos, total_puntos
    nuevo_x, nuevo_y = x + dx, y + dy

    if 0 <= nuevo_x < COLUMNAS and 0 <= nuevo_y < FILAS:
        if mapa[nuevo_y][nuevo_x] != "#":
            if mapa[nuevo_y][nuevo_x] == ".":
                puntos += 1
                # al usar matriz, asignar directamente
                mapa[nuevo_y][nuevo_x] = " "
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
    """Detecta si Pac-Man toca a un enemigo."""
    for e in enemigos:
        if (x, y) == (e["x"], e["y"]):
            return True
    return False


def game_over():
    pantalla.fill(NEGRO)
    texto_game_over = fuente.render("¡Game Over!", True, ROJO)
    pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 3))
    pygame.display.flip()
    pygame.time.wait(2000)


# --- INICIO DEL JUEGO ---
mapa_juego = cargar_mapa_clasico()

# --- BUCLE PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        mover(0, -1, mapa_juego)
    elif teclas[pygame.K_s]:
        mover(0, 1, mapa_juego)
    elif teclas[pygame.K_a]:
        mover(-1, 0, mapa_juego)
    elif teclas[pygame.K_d]:
        mover(1, 0, mapa_juego)
    elif teclas[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # Movimiento enemigos
    mover_enemigos(mapa_juego)

    # Colisión
    if detectar_colision():
        vidas -= 1
        if vidas > 0:
            # Mostrar mensaje al perder una vida
            texto_vida = fuente.render("¡Perdiste una vida!", True, ROJO)
            pantalla.fill(NEGRO)
            pantalla.blit(texto_vida, (ANCHO // 2 - texto_vida.get_width() // 2, ALTO // 2))
            pygame.display.flip()
            pygame.time.wait(1000)
            x, y = 13, 17
        else:
            game_over()
            vidas = 3
            puntos = 0
            mapa_juego = cargar_mapa_clasico()

    # Todos los puntos recolectados
    if puntos >= total_puntos and total_puntos > 0:
        texto_nivel = fuente.render("¡Nivel completado!", True, CELESTE)
        pantalla.fill(NEGRO)
        pantalla.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(1500)
        mapa_juego = cargar_mapa_clasico()
        puntos = 0

    # DIBUJAR
    pantalla.fill(NEGRO)
    # dibujar el mapa desde la matriz editable
    dibujar_mapa_juego(pantalla, mapa_juego)

    # Pac-Man
    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (x * TAM_CELDA + TAM_CELDA // 2, y * TAM_CELDA + TAM_CELDA // 2),
        TAM_CELDA // 3,
    )

    # Enemigos
    for e in enemigos:
        pygame.draw.circle(
            pantalla,
            e["color"],
            (e["x"] * TAM_CELDA + TAM_CELDA // 2, e["y"] * TAM_CELDA + TAM_CELDA // 2),
            TAM_CELDA // 3,
        )

    # HUD (puntos y vidas)
    texto = fuente.render(f"Puntos: {puntos}/{total_puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    # Dibujar las vidas como mini Pac-Man
    for i in range(vidas):
        pygame.draw.circle(pantalla, AMARILLO, (ANCHO - 150 + i * 30, 25), 10)

    pygame.display.flip()
    reloj.tick(FPS)
