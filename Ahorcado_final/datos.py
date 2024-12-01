import json

def cargar_palabras():
    """Si encuentra el archivo carga las palabras y sino inicializa una lista vacia y printea un mensaje de aviso

    Returns:
        list: lista con las palabras
    """
    try:
        with open("Datosjason.json", "r") as archivo:
            palabras = json.load(archivo)
    except FileNotFoundError:
        print("No se encontró el archivo 'Datosjason.json'. Se usará un conjunto de palabras vacío.")
        palabras = []
    return palabras
