import pygame
import sys
import random

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
TAM_CELDA = 40
FPS = 6  # Velocidad inicial

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 150)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ROSA = (255, 105, 180)
AZUL_CLARO = (100, 149, 237)
NARANJA = (255, 165, 0)

# --- TAMAÑO DEL MAPA ---
FILAS = 15
COLUMNAS = 21
ANCHO = COLUMNAS * TAM_CELDA
ALTO = FILAS * TAM_CELDA

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PAC-MAN con laberintos y enemigos")

fuente = pygame.font.SysFont("Arial", 24)
reloj = pygame.time.Clock()

# --- VARIABLES DE JUEGO ---
x, y = 1, 1
puntos = 0
total_puntos = 0
enemigos = []
vidas = 3
nivel = 1
direccion_x, direccion_y = 0, 0  # Dirección de movimiento de Pac-Man


# --- FUNCIONES ---
def generar_laberinto(filas, columnas):
    """Genera un laberinto con el algoritmo DFS."""
    filas = filas if filas % 2 == 1 else filas - 1
    columnas = columnas if columnas % 2 == 1 else columnas - 1

    lab = [["#" for _ in range(columnas)] for _ in range(filas)]

    def en_rango(cx, cy):
        return 0 <= cx < columnas and 0 <= cy < filas

    def vecinos(cx, cy):
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        result = []
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if en_rango(nx, ny) and lab[ny][nx] == "#":
                result.append((nx, ny))
        return result

    def dfs(cx, cy):
        lab[cy][cx] = " "
        for nx, ny in random.sample(vecinos(cx, cy), len(vecinos(cx, cy))):
            if lab[ny][nx] == "#":
                lab[(cy + ny) // 2][(cx + nx) // 2] = " "
                dfs(nx, ny)

    dfs(1, 1)
    return ["".join(f) for f in lab]


def agregar_puntos_y_enemigos(lab, nivel):
    """Agrega puntos (.) y enemigos en espacios vacíos."""
    global total_puntos, enemigos, x, y

    mapa = []
    for fila in lab:
        nueva = ""
        for c in fila:
            if c == " " and random.random() < 0.8:
                nueva += "."
            else:
                nueva += c
        mapa.append(nueva)

    total_puntos = sum(f.count('.') for f in mapa)
    x, y = 1, 1

    enemigos = generar_enemigos(mapa, cantidad=min(3 + nivel, 12))
    return mapa


def generar_enemigos(mapa, cantidad=3):
    enemigos = []
    vacios = [
        (i, j)
        for j, fila in enumerate(mapa)
        for i, celda in enumerate(fila)
        if celda == " " or celda == "."
    ]
    colores = [ROJO, ROSA, AZUL_CLARO, NARANJA]  # Los colores de los enemigos
    for _ in range(cantidad):
        if vacios:
            x, y = random.choice(vacios)
            color = random.choice(colores)
            enemigos.append((x, y, color))
    return enemigos


def dibujar_mapa(mapa):
    for j, fila in enumerate(mapa):
        for i, celda in enumerate(fila):
            rect = pygame.Rect(i * TAM_CELDA, j * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            if celda == "#":
                pygame.draw.rect(pantalla, AZUL, rect)
            elif celda == ".":
                pygame.draw.circle(pantalla, BLANCO, rect.center, 5)


def mover(dx, dy, mapa):
    global x, y, puntos, direccion_x, direccion_y
    nuevo_x, nuevo_y = x + dx, y + dy
    if 0 <= nuevo_x < COLUMNAS and 0 <= nuevo_y < FILAS:
        if mapa[nuevo_y][nuevo_x] != "#":
            if mapa[nuevo_y][nuevo_x] == ".":
                puntos += 1
                mapa[nuevo_y] = (
                    mapa[nuevo_y][:nuevo_x] + " " + mapa[nuevo_y][nuevo_x + 1:]
                )
            x, y = nuevo_x, nuevo_y
            direccion_x, direccion_y = dx, dy


def mover_enemigos(mapa):
    global enemigos
    nuevas_pos = []
    for ex, ey, color in enemigos:
        if color == ROJO:
            # Rojo persigue a Pac-Man
            dx = 1 if ex < x else -1 if ex > x else 0
            dy = 1 if ey < y else -1 if ey > y else 0
        elif color == ROSA:
            # Rosa se posiciona al frente de Pac-Man
            dx, dy = direccion_x, direccion_y
        elif color == AZUL_CLARO:
            # Azul intenta posicionarse detrás de Pac-Man
            dx, dy = -direccion_x, -direccion_y
        elif color == NARANJA:
            # Naranja se mueve aleatoriamente
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

        nuevo_ex, nuevo_ey = ex + dx, ey + dy
        if 0 <= nuevo_ex < COLUMNAS and 0 <= nuevo_ey < FILAS and mapa[nuevo_ey][nuevo_ex] != "#":
            nuevas_pos.append((nuevo_ex, nuevo_ey, color))
        else:
            nuevas_pos.append((ex, ey, color))  # No se mueve si choca con un muro

    enemigos = nuevas_pos


def detectar_colision():
    for ex, ey, color in enemigos:
        if (x, y) == (ex, ey):
            return True
    return False


def mostrar_mensaje(texto, color=BLANCO, tiempo=1500):
    pantalla.fill(NEGRO)
    texto_render = fuente.render(texto, True, color)
    pantalla.blit(texto_render, (ANCHO // 2 - 100, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(tiempo)


# --- INICIO ---
lab = generar_laberinto(FILAS, COLUMNAS)
mapa = agregar_puntos_y_enemigos(lab, nivel)

# --- BUCLE PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    mover_enemigos(mapa)

    if detectar_colision():
        vidas -= 1
        if vidas <= 0:
            mostrar_mensaje("¡GAME OVER!", ROJO, 2000)
            pygame.quit()
            sys.exit()
        else:
            mostrar_mensaje("¡Has perdido una vida!", ROJO, 1000)
            lab = generar_laberinto(FILAS, COLUMNAS)
            mapa = agregar_puntos_y_enemigos(lab, nivel)
            puntos = 0

        if total_puntos > 0 and puntos >= total_puntos:
        nivel += 1
        mostrar_mensaje(f"¡Nivel {nivel} completado!", AMARILLO, 1500)
        lab = generar_laberinto(FILAS, COLUMNAS)
        mapa = agregar_puntos_y_enemigos(lab, nivel)
        puntos = 0
        FPS += 1  # Aumenta la velocidad cada nivel

    # --- DIBUJAR ---
    pantalla.fill(NEGRO)
    dibujar_mapa(mapa)
    pygame.draw.circle(
        pantalla, AMARILLO,
        (x * TAM_CELDA + TAM_CELDA // 2, y * TAM_CELDA + TAM_CELDA // 2),
        TAM_CELDA // 2 - 5
    )

    for ex, ey, color in enemigos:
        pygame.draw.circle(
            pantalla, color,
            (ex * TAM_CELDA + TAM_CELDA // 2, ey * TAM_CELDA + TAM_CELDA // 2),
            TAM_CELDA // 2 - 5
        )

    # --- HUD ---
    texto = fuente.render(
        f"Puntos: {puntos}/{total_puntos}  Vidas: {vidas}  Nivel: {nivel}",
        True,
        BLANCO,
    )
    pantalla.blit(texto, (10, 10))

    pygame.display.flip()
    reloj.tick(FPS)
