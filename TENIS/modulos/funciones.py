import pygame
from modulos.configuracion import BLANCO, ANCHO, ALTO, NEGRO

def dibujar_linea_punteada(ventana):
    """
    Dibuja una línea punteada vertical en el centro de la pantalla,
    con intervalos de 20 píxeles entre cada segmento de la línea.

    Parámetros:
        ventana (pygame.Surface): La ventana donde se dibuja la línea.
    """
    color = BLANCO
    x = ANCHO // 2  # Coordenada X en el centro de la pantalla
    y_inicio = 0  # Comienza en la parte superior de la pantalla
    y_fin = ALTO  # Termina en la parte inferior de la pantalla

    # Bucle para dibujar la línea punteada
    for y in range(y_inicio, y_fin, 20):  # A intervalos de 20 píxeles
        pygame.draw.line(ventana, color, (x, y), (x, y + 10))  # Dibuja un segmento de línea

def pedir_nombres(ventana, ANCHO, ALTO):
    """
    Solicita a los jugadores que ingresen sus nombres a través del teclado.
    
    La función permite que el Jugador 1 ingrese su nombre primero, luego el Jugador 2.
    Si se deja un campo vacío o el nombre es el mismo que el del Jugador 1, 
    se muestra un mensaje de error pidiendo que se ingrese un nombre válido.
    
    Parámetros:
        ventana (pygame.Surface): La ventana donde se muestra el texto.
        ANCHO (int): Ancho de la ventana, utilizado para centrar el texto.
        ALTO (int): Alto de la ventana, utilizado para centrar el texto.
        
    Retorna:
        tuple: Una tupla con los nombres de los jugadores (nombre_j1, nombre_j2).
    """
    fuente = pygame.font.Font(None, 36)
    
    nombre_j1 = "" 
    nombre_j2 = ""  
    
    input_activo = 1  # 1 para Jugador 1, 2 para Jugador 2
    texto = "Ingrese nombre Jugador 1:" 
    mensaje_error = "" 

    while True:
        ventana.fill(NEGRO)  

        texto_instrucciones = fuente.render(texto, True, BLANCO)
        ventana.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 4))

        # Muestro el nombre ingresado por cada jugador
        if input_activo == 1:
            texto_j1_render = fuente.render(nombre_j1, True, BLANCO)
            ventana.blit(texto_j1_render, (ANCHO // 2 - texto_j1_render.get_width() // 2, ALTO // 2))
        elif input_activo == 2:
            texto_j2_render = fuente.render(nombre_j2, True, BLANCO)
            ventana.blit(texto_j2_render, (ANCHO // 2 - texto_j2_render.get_width() // 2, ALTO // 2))

        # Muestro mensaje de error si existe uno
        if mensaje_error:
            texto_error_render = fuente.render(mensaje_error, True, (255, 0, 0))  # Color rojo para el error
            ventana.blit(texto_error_render, (ANCHO // 2 - texto_error_render.get_width() // 2, ALTO // 1.5))

        pygame.display.flip()  # Actualizo la pantalla

        # Manejo los eventos de teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()  # Salir si se cierra la ventana
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    # Elimina el último carácter del nombre ingresado
                    if input_activo == 1:
                        nombre_j1 = nombre_j1[:-1]
                    elif input_activo == 2:
                        nombre_j2 = nombre_j2[:-1]
                elif evento.key == pygame.K_RETURN:
                    # Validar si el nombre está vacío antes de avanzar
                    if input_activo == 1:
                        if nombre_j1.strip() == "":  # Comprobar si el nombre está vacío
                            mensaje_error = "El nombre del Jugador 1 no puede estar vacío"
                            texto = "Ingrese nombre Jugador 1:"  # Volver al mensaje de Jugador 1
                            input_activo = 1  # Mantener al Jugador 1 activo
                        else:
                            texto = "Ingrese nombre Jugador 2:"  # Cambio la instrucción a Jugador 2
                            input_activo = 2  # Cambia al siguiente jugador
                            mensaje_error = ""  # Limpia mensaje de error si el nombre es válido
                    elif input_activo == 2:
                        if nombre_j2.strip() == "":  # Comprueba si el nombre está vacío
                            mensaje_error = "El nombre del Jugador 2 no puede estar vacío"
                            texto = "Ingrese nombre Jugador 2:"  # Volver al mensaje de Jugador 2
                        elif nombre_j2.strip().lower() == nombre_j1.strip().lower():  # Verifica si el nombre es igual al de Jugador 1
                            mensaje_error = "No puede tener el mismo nombre que el Jugador 1"
                            texto = "Ingrese nombre Jugador 2:"  # Volver al mensaje de Jugador 2
                        else:
                            return nombre_j1, nombre_j2  # Ambos nombres válidos, retornar los nombres
                else:
                    # Añade el carácter ingresado al nombre del jugador activo
                    if input_activo == 1:
                        nombre_j1 += evento.unicode
                    elif input_activo == 2:
                        nombre_j2 += evento.unicode
