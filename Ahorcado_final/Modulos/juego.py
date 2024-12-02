import random
from Modulos.datos import *
from Modulos.utilidades import *
from Modulos.puntajes import *

def jugar():
    """
    Generacion del juego para cuando se selecciona la opcion de jugar
    """
    palabras = cargar_palabras()
    idioma = input("Seleccione el idioma (es/en): ").strip().lower()

    if idioma not in ["es", "en"]:
        print("Idioma no válido.")
        while idioma not in ["es", "en"]:
            idioma = input("Seleccione nuevamente el idioma (es/en): ").strip().lower()

    lista_palabras = [palabra[idioma.upper()] for palabra in palabras["ahorcado"]]
    palabra_secreta = random.choice(lista_palabras)
    progreso = "_" * len(palabra_secreta)
    letras_usadas = []
    intentos = 0
    puntaje = 0

    print("\n¡Bienvenido al juego del ahorcado!")

    while True:
        print(f"\nPalabra: {progreso}")
        print(f"Letras usadas: {', '.join(letras_usadas)}")
        print(f"Intentos restantes: {6 - intentos}")
        letra = input("Ingrese una letra: ").strip().lower()

        # Validación de entrada
        if len(letra) != 1 or not letra.isalpha():
            print("Ingreso no válido. Por favor, ingrese una letra válida.")
        elif letra in letras_usadas:
            print("Ya usaste esa letra. Intenta con otra.")
        else:
            letras_usadas.append(letra)

            if letra in palabra_secreta:
                for i in range(len(palabra_secreta)):
                    if palabra_secreta[i] == letra:
                        progreso = progreso[:i] + letra + progreso[i+1:]
                        puntaje += 1
            else:
                intentos += 1
                mostrar_monigote(intentos)

        # Condiciones de finalización
        if intentos == 6:
            print(f"\nHas perdido. La palabra secreta era: {palabra_secreta}")
            break

        if progreso == palabra_secreta:
            print(f"\n¡Felicidades! Has ganado. La palabra secreta era: {palabra_secreta}")
            puntaje += len(palabra_secreta)
            break

    nombre = input("\nIntroduce tu nombre: ")
    guardar_puntaje(nombre, puntaje)
    print(f"Tu puntaje final es: {puntaje} puntos.")
