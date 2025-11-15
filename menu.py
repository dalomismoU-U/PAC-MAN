import tkinter as tk
from tkinter import Canvas
import sys
import mine


def dibujar_texto(canvas, texto, size, color, x, y):
    canvas.create_text(x, y, text=texto, font=("Arial", size), fill=color)


def menu():
    ventana = tk.Tk()
    ventana.title("PAC-MAN - Menú")
    ventana.geometry(f"{mine.ANCHO}x{mine.ALTO}")
    ventana.resizable(False, False)
    
    canvas = Canvas(ventana, width=mine.ANCHO, height=mine.ALTO, bg="#000000", highlightthickness=0)
    canvas.pack()
    
    opciones = ["Iniciar juego", "Instrucciones", "Salir"]
    seleccionado = [0]
    
    def dibujar_menu():
        canvas.delete("all")
        canvas.create_rectangle(0, 0, mine.ANCHO, mine.ALTO, fill="#000000", outline="#000000")
        
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
