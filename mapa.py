import pygame
import sys

# --- CONFIGURACIÓN ---
TAM_CELDA = 24
ANCHO, ALTO = 28 * TAM_CELDA, 31 * TAM_CELDA
# Nota: la inicialización de pygame y la creación de la ventana
# se realizan sólo cuando este módulo se ejecuta directamente.

# --- COLORES ---
AZUL = (33, 33, 255)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS = (50, 50, 50)

# --- MAPA CLÁSICO ORIGINAL (28x31) ---
# Basado en la disposición auténtica del arcade original
mapa = [
"############################",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#O####.#####.##.#####.####O#",
"#.####.#####.##.#####.####.#",
"#..........................#",
"#.####.##.########.##.####.#",
"#.####.##.########.##.####.#",
"#......##....##....##......#",
"######.##### ## #####.######",
"######.##### ## #####.######",
"######.##          ##.######",
"######.## ######## ##.######",
"######.## ######## ##.######",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#.####.#####.##.#####.####.#",
"#O..##................##..O#",
"###.##.##.########.##.##.###",
"###.##.##.########.##.##.###",
"#......##....##....##......#",
"#.##########.##.##########.#",
"#.##########.##.##########.#",
"#..........................#",
"############################"
]

# --- FUNCIÓN PARA DIBUJAR EL MAPA ---
def dibujar_mapa(surface):
    """Dibuja el mapa sobre la superficie `surface`.

    Esta función es importable y no asume la existencia de una ventana global.
    """
    for fila_idx, fila in enumerate(mapa):
        for col_idx, celda in enumerate(fila):
            x = col_idx * TAM_CELDA
            y = fila_idx * TAM_CELDA
            if celda == "#":
                pygame.draw.rect(surface, AZUL, (x, y, TAM_CELDA, TAM_CELDA))
            elif celda == ".":
                pygame.draw.circle(surface, BLANCO, (x + TAM_CELDA // 2, y + TAM_CELDA // 2), 3)
            elif celda == "O":
                pygame.draw.circle(surface, BLANCO, (x + TAM_CELDA // 2, y + TAM_CELDA // 2), 6)
            elif celda == " ":
                pass  # espacio libre
            # Posición inicial de Pac-Man (centro inferior)
            if fila_idx == 17 and col_idx == 13:
                pygame.draw.circle(surface, AMARILLO, (x + TAM_CELDA // 2, y + TAM_CELDA // 2), 8)

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    # Si se ejecuta directamente, se inicializa pygame y se ejecuta el bucle.
    pygame.init()
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pac-Man - Mapa clásico original")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        VENTANA.fill(NEGRO)
        dibujar_mapa(VENTANA)
        pygame.display.flip()
        clock.tick(30)

