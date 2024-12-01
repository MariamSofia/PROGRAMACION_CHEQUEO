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

def mostrar_monigote(intentos):
    """Genera el monigote según la cantidad de intentos usados

    Args:
        intentos (int): cantidad de intentos usados
    """
    estado = [
        "  O  ",  # Cabeza
        "     ",  # Brazos
        "     ",  # Cuerpo
        "     "   # Piernas
    ]

    if intentos >= 2: estado[1] = " /   "  # Brazo izquierdo
    if intentos >= 3: estado[1] = " / \\ "  # Ambos brazos
    if intentos >= 4: estado[2] = "  |   "  # Cuerpo
    if intentos >= 5: estado[3] = " /    "  # Pierna izquierda
    if intentos >= 6: estado[3] = " / \\ "  # Ambas piernas

    print("\nMonigote:")
    for linea in estado:
        print(linea)

