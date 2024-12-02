def ordenar_puntajes_burbuja(puntajes):
    """Ordena los puntajes de mayor a menor

    Args:
        puntajes (list): lista con los puntajes desordenados

    Returns:
        list: lista con los puntajes ordenados
    """
    n = len(puntajes)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if puntajes[j]["puntaje"] < puntajes[j + 1]["puntaje"]:
                puntajes[j], puntajes[j + 1] = puntajes[j + 1], puntajes[j]
    return puntajes

# Función para mostrar el monigote (progresivo según los intentos)
def mostrar_monigote(intentos):
    print("\nMonigote:")
    # Base de la horca: estructura estática que se muestra siempre
    base_horca = [
        "  ________",
        "  |      |",
        "  |    ",  # Espacio donde irá el monigote
        "  |    ",
        "  |    ",
        "  |    ",
        " _|_  ",
    ]
    # Partes del monigote, dependiendo de los intentos fallidos
    monigote = {
        1: ["  O  "],  # Cabeza
        2: ["  O  ", "  |  "],  # Cabeza + cuerpo
        3: ["  O  ", " /|  "],  # Cabeza + cuerpo + un brazo
        4: ["  O  ", " /|\\ "],  # Cabeza + cuerpo + ambos brazos
        5: ["  O  ", " /|\\ ", " /   "],  # Cabeza + cuerpo + ambos brazos + una pierna
        6: ["  O  ", " /|\\ ", " / \\ "]  # Monigote completo
    }
        
    # Construir la horca con el monigote según los intentos
    for i in range(len(base_horca)):
        if i == 2 and intentos > 0:  # Línea donde comienza el monigote
            # Obtiene las partes del monigote correspondientes al número de intentos
            for parte in monigote.get(intentos, []):
                print(f"{base_horca[i]}{parte}")
                i += 1  # Avanzar para no sobrescribir la horca
        else:
            # Muestra las líneas restantes de la horca
            print(base_horca[i])
