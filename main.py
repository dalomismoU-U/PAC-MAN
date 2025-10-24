
import os
import time
import msvcrt  # solo en Windows

# Funciones equivalentes
def gotoxy(x, y):
    os.system(f"echo \033[{y};{x}H")  # mueve el cursor en consola

def clrscr():
    os.system("cls" if os.name == "nt" else "clear")

# Mapa simple
mapa = [
    "#####################",
    "#........#..........#",
    "#.##.###.#.###.##..#",
    "#...................#",
    "#####################"
]

# Posición inicial de Pacman
x, y = 1, 1
puntos = 0

def dibujar_mapa():
    for fila in mapa:
        print(fila)
    print(f"Puntos: {puntos}")

def mover(dx, dy):
    global x, y, puntos
    nuevo_x, nuevo_y = x + dx, y + dy
    if mapa[nuevo_y][nuevo_x] != "#":
        if mapa[nuevo_y][nuevo_x] == ".":
            puntos += 1
            mapa[nuevo_y] = mapa[nuevo_y][:nuevo_x] + " " + mapa[nuevo_y][nuevo_x+1:]
        x, y = nuevo_x, nuevo_y

# Bucle principal
while True:
    clrscr()
    dibujar_mapa()
    gotoxy(x + 1, y + 1)
    print("C", end="", flush=True)  # Pacman

    if msvcrt.kbhit():
        tecla = msvcrt.getch().lower()
        if tecla == b'w': mover(0, -1)
        elif tecla == b's': mover(0, 1)
        elif tecla == b'a': mover(-1, 0)
        elif tecla == b'd': mover(1, 0)
        elif tecla == b'q': break

    time.sleep(0.1)
