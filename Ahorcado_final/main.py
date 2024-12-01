from juego import *
from puntajes import *

def menu():
    """
    Genera el menu para elegir la opcion
    """
    while True:
        print("\n--- Menú Principal ---")
        print("1. Jugar")
        print("2. Ver puntajes")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            jugar()
        elif opcion == "2":
            mostrar_puntajes()
        elif opcion == "3":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
