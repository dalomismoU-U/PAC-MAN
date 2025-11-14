import pygame
import sys
import mine


def dibujar_texto(surface, texto, fuente, color, x, y):
    txt = fuente.render(texto, True, color)
    surface.blit(txt, (x, y))


def menu():
    pygame.init()
    ANCHO, ALTO = mine.ANCHO, mine.ALTO
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PAC-MAN - Menú")
    fuente = pygame.font.SysFont("Arial", 30)
    clock = pygame.time.Clock()

    opciones = ["Iniciar juego", "Instrucciones", "Salir"]
    seleccionado = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    if opciones[seleccionado] == "Iniciar juego":
                        # Cerrar el display del menú y lanzar el juego
                        pygame.quit()
                        mine.main()
                        return
                    elif opciones[seleccionado] == "Instrucciones":
                        mostrar_instrucciones(pantalla, fuente)
                    elif opciones[seleccionado] == "Salir":
                        pygame.quit()
                        sys.exit()

        pantalla.fill((0, 0, 0))
        dibujar_texto(pantalla, "PAC-MAN", fuente, (255, 255, 0), ANCHO // 2 - 80, 50)

        for i, op in enumerate(opciones):
            color = (255, 255, 255) if i != seleccionado else (255, 200, 0)
            dibujar_texto(pantalla, op, fuente, color, ANCHO // 2 - 100, 150 + i * 50)

        pygame.display.flip()
        clock.tick(30)


def mostrar_instrucciones(pantalla, fuente):
    reloj = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                # cualquier tecla vuelve al menú
                return

        pantalla.fill((0, 0, 0))
        instrucciones = [
            "WASD - Mover Pac-Man",
            "Q - Salir del juego",
            "Comer O activa power pellet (come fantasmas)",
            "Pulsa cualquier tecla para volver al menú",
        ]
        for i, linea in enumerate(instrucciones):
            txt = fuente.render(linea, True, (200, 200, 200))
            pantalla.blit(txt, (50, 120 + i * 40))

        pygame.display.flip()
        reloj.tick(30)


if __name__ == "__main__":
    menu()
