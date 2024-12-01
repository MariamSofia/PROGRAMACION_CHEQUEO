import json
from utilidades import *

def guardar_puntaje(nombre, puntaje):
    """Guarda los puntajes en el JSON de scores si ya existe y sino lo crea

    Args:
        nombre (string): nombre del jugador
        puntaje (int): puntaje de la partida
    """
    try:
        with open("scores.json", "r") as archivo:
            puntajes = json.load(archivo)
    except FileNotFoundError:
        puntajes = []

    puntajes.append({"nombre": nombre, "puntaje": puntaje})

    with open("scores.json", "w") as archivo:
        json.dump(puntajes, archivo, indent=4)

def mostrar_puntajes():
    """
    Muestra los 5 puntajes más altos
    """
    try:
        with open("scores.json", "r") as archivo:
            puntajes = json.load(archivo)
        
        # Ordena los puntajes de mayor a menor
        puntajes = ordenar_puntajes_burbuja(puntajes)

        # Muestra solo los 5 mejores puntajes
        print("\n--- Mejores Puntajes ---")
        for i, puntaje in enumerate(puntajes[:5]):
            print(f"{i + 1}. {puntaje['nombre']} - {puntaje['puntaje']} puntos")
    except FileNotFoundError:
        print("\nNo hay puntajes registrados todavía.")
