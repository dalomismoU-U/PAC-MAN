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

# --- TAMAÑO DEL MAPA ---
FILAS = 15
COLUMNAS = 21
ANCHO = COLUMNAS * TAM_CELDA
ALTO = FILAS * TAM_CELDA

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PAC-MAN con laberintos y dificultad progresiva")

fuente = pygame.font.SysFont("Arial", 24)
reloj = pygame.time.Clock()

# --- VARIABLES DE JUEGO ---
x, y = 1, 1
puntos = 0
total_puntos = 0
enemigos = []
vidas = 3
nivel = 1


# --- FUNCIONES ---
def generar_laberinto(filas, columnas):
    """Genera un laberinto con el algoritmo DFS."""
    # Asegurar que las dimensiones sean impares
    filas = filas if filas % 2 == 1 else filas - 1
    columnas = columnas if columnas % 2 == 1 else columnas - 1

    # Inicializar todas las celdas como muros
    lab = [["#" for _ in range(columnas)] for _ in range(filas)]

    # Elegir una celda inicial impar
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
                # Eliminar muro intermedio
                lab[(cy + ny) // 2][(cx + nx) // 2] = " "
                dfs(nx, ny)

    dfs(1, 1)

    # Convertir el laberinto en lista de strings
    return ["".join(f) for f in lab]


def agregar_puntos_y_enemigos(lab, nivel):
    """Agrega puntos (.) y enemigos en espacios vacíos."""
    global total_puntos, enemigos, x, y

    # Reemplazar algunos espacios por puntos
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

    # Generar enemigos según el nivel
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
    for _ in range(cantidad):
        if vacios:
            enemigos.append(random.choice(vacios))
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
    global x, y, puntos
    nuevo_x, nuevo_y = x + dx, y + dy
    if 0 <= nuevo_x < COLUMNAS and 0 <= nuevo_y < FILAS:
        if mapa[nuevo_y][nuevo_x] != "#":
            if mapa[nuevo_y][nuevo_x] == ".":
                puntos += 1
                mapa[nuevo_y] = (
                    mapa[nuevo_y][:nuevo_x] + " " + mapa[nuevo_y][nuevo_x + 1:]
                )
            x, y = nuevo_x, nuevo_y


def mover_enemigos(mapa):
    global enemigos
    nuevas_pos = []
    for ex, ey in enemigos:
        opciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(opciones)
        movido = False
        for dx, dy in opciones:
            nx, ny = ex + dx, ey + dy
            if 0 <= nx < COLUMNAS and 0 <= ny < FILAS and mapa[ny][nx] != "#":
                nuevas_pos.append((nx, ny))
                movido = True
                break
        if not movido:
            nuevas_pos.append((ex, ey))
    enemigos = nuevas_pos


def detectar_colision():
    for ex, ey in enemigos:
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
        FPS = min(FPS + 1, 12)  # Aumenta la velocidad un poco cada nivel
        mostrar_mensaje(f"¡Nivel {nivel}!", AMARILLO, 1500)
        lab = generar_laberinto(FILAS, COLUMNAS)
        mapa = agregar_puntos_y_enemigos(lab, nivel)
        puntos = 0

    # --- DIBUJAR ---
    pantalla.fill(NEGRO)
    dibujar_mapa(mapa)

    pygame.draw.circle(
        pantalla,
        AMARILLO,
        (x * TAM_CELDA + TAM_CELDA // 2, y * TAM_CELDA + TAM_CELDA // 2),
        TAM_CELDA // 3,
    )

    for ex, ey in enemigos:
        pygame.draw.circle(
            pantalla,
            ROJO,
            (ex * TAM_CELDA + TAM_CELDA // 2, ey * TAM_CELDA + TAM_CELDA // 2),
            TAM_CELDA // 3,
        )

    texto = fuente.render(f"Puntos: {puntos}/{total_puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, AMARILLO)
    pantalla.blit(texto_vidas, (ANCHO - 120, 10))
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto_nivel, (ANCHO // 2 - 50, 10))

    pygame.display.flip()
    reloj.tick(FPS)