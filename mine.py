import pygame
import sys
import random

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
TAM_CELDA = 40
FPS = 6  # Velocidad moderada

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 150)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# --- TAMAÑO DEL MAPA ---
FILAS = 10
COLUMNAS = 15
ANCHO = COLUMNAS * TAM_CELDA
ALTO = FILAS * TAM_CELDA

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PAC-MAN con enemigos y colisiones fijas")

fuente = pygame.font.SysFont("Arial", 24)
reloj = pygame.time.Clock()

# --- VARIABLES DE JUEGO ---
x, y = 1, 1
puntos = 0
total_puntos = 0
enemigos = []


# --- FUNCIONES ---
def generar_mapa():
    """Genera un mapa aleatorio con paredes y puntos."""
    global total_puntos, x, y, enemigos
    mapa = []
    for j in range(FILAS):
        fila = ""
        for i in range(COLUMNAS):
            if j == 0 or j == FILAS - 1 or i == 0 or i == COLUMNAS - 1:
                fila += "#"
            else:
                r = random.random()
                if r < 0.2:
                    fila += "#"
                elif r < 0.7:
                    fila += "."
                else:
                    fila += " "
        mapa.append(fila)

    # Zona inicial libre
    mapa[1] = mapa[1][:1] + " " + mapa[1][2:]
    x, y = 1, 1
    total_puntos = sum(f.count('.') for f in mapa)

    # Crear enemigos
    enemigos = generar_enemigos(mapa, cantidad=3)
    return mapa


def generar_enemigos(mapa, cantidad=3):
    """Coloca enemigos en lugares libres del mapa."""
    enemigos = []
    vacios = [
        (i, j)
        for j, fila in enumerate(mapa)
        for i, celda in enumerate(fila)
        if celda == " " and (i, j) != (1, 1)
    ]
    for _ in range(cantidad):
        if vacios:
            enemigos.append(random.choice(vacios))
    return enemigos


def dibujar_mapa(mapa):
    """Dibuja las paredes y los puntos."""
    for j, fila in enumerate(mapa):
        for i, celda in enumerate(fila):
            rect = pygame.Rect(i * TAM_CELDA, j * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            if celda == "#":
                pygame.draw.rect(pantalla, AZUL, rect)
            elif celda == ".":
                pygame.draw.circle(pantalla, BLANCO, rect.center, 5)


def mover(dx, dy, mapa):
    """Mueve a Pac-Man solo si no hay paredes."""
    global x, y, puntos, total_puntos
    nuevo_x, nuevo_y = x + dx, y + dy

    # Verificar límites y paredes
    if 0 <= nuevo_x < COLUMNAS and 0 <= nuevo_y < FILAS:
        if mapa[nuevo_y][nuevo_x] != "#":
            # Comer punto
            if mapa[nuevo_y][nuevo_x] == ".":
                puntos += 1
                mapa[nuevo_y] = (
                    mapa[nuevo_y][:nuevo_x] + " " + mapa[nuevo_y][nuevo_x + 1:]
                )
            x, y = nuevo_x, nuevo_y


def mover_enemigos(mapa):
    """Mueve enemigos de forma aleatoria."""
    global enemigos
    nuevas_pos = []
    for ex, ey in enemigos:
        opciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(opciones)
        movido = False
        for dx, dy in opciones:
            nx, ny = ex + dx, ey + dy
            if (
                0 <= nx < COLUMNAS
                and 0 <= ny < FILAS
                and mapa[ny][nx] != "#"
            ):
                nuevas_pos.append((nx, ny))
                movido = True
                break
        if not movido:
            nuevas_pos.append((ex, ey))
    enemigos = nuevas_pos


def detectar_colision():
    """Detecta si Pac-Man toca a un enemigo."""
    for ex, ey in enemigos:
        if (x, y) == (ex, ey):
            return True
    return False


# --- INICIO DEL JUEGO ---
mapa = generar_mapa()

# --- BUCLE PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Movimiento del jugador ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        mover(0, -1, mapa)
    elif teclas[pygame.K_s]:
        mover(0, 1, mapa)
    elif teclas[pygame.K_a]:
        mover(-1, 0, mapa)
    elif teclas[pygame.K_d]:
        mover(1, 0, mapa)
    elif teclas[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # --- Movimiento enemigos ---
    mover_enemigos(mapa)

    # --- Colisión con enemigo ---
    if detectar_colision():
        mapa = generar_mapa()
        puntos = 0

    # --- Todos los puntos recolectados ---
    if puntos >= total_puntos and total_puntos > 0:
        mapa = generar_mapa()
        puntos = 0

    # --- DIBUJAR ---
    pantalla.fill(NEGRO)
    dibujar_mapa(mapa)

    # Pac-Man
    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (x * TAM_CELDA + TAM_CELDA // 2, y * TAM_CELDA + TAM_CELDA // 2),
        TAM_CELDA // 3,
    )

    # Enemigos
    for ex, ey in enemigos:
        pygame.draw.circle(
            pantalla,
            ROJO,
            (ex * TAM_CELDA + TAM_CELDA // 2, ey * TAM_CELDA + TAM_CELDA // 2),
            TAM_CELDA // 3,
        )

    # Texto
    texto = fuente.render(f"Puntos: {puntos}/{total_puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    reloj.tick(FPS)