from modulos.configuracion import ANCHO, ALTO, BLANCO, NEGRO
from modulos.Paleta import *
from modulos.Pelota import *
from modulos.funciones import *

def pantalla_inicio(ventana):
    """
    Muestra la pantalla de inicio con instrucciones del juego.
    
    Esta función presenta las instrucciones de control del juego, cómo mover las paletas,
    la meta del juego, y espera a que el jugador presione cualquier tecla para continuar.
    """
    fuente = pygame.font.Font(None, 36)
    
    # Texto de las instrucciones del juego
    instrucciones = [
        "El jugador 1 se mueve con 'W' y 'S'",
        "El jugador 2 se mueve con las flechas arriba y abajo",
        "",
        "",
        "El primero en llegar a 10 puntos gana",
        "",
        "",
        "",
        "",
        "Presione cualquier tecla para continuar"
    ]
    
    ventana.fill(NEGRO)
    
    for i, linea in enumerate(instrucciones):
        texto = fuente.render(linea, True, BLANCO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 4 + i * 40))
    
    pygame.display.flip()

    # Esperar hasta que el jugador presione una tecla
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False  # Salir del bucle al presionar cualquier tecla


def mostrarJuego():
    """
    Función principal del juego Pong.
    
    Esta función configura e inicia el juego, maneja el estado del juego (incluyendo la 
    música, los puntajes y los eventos de las teclas) y actualiza continuamente la ventana 
    con el progreso del juego.
    """
    pygame.init()

    # Inicializar música de fondo y sonidos
    pygame.mixer.music.load("sonidos/African_fun_long.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1, 0.0)  # -1 para que se repita en bucle

    rebote_sonido = pygame.mixer.Sound("sonidos/sport_table_tennis_ping_pong_ball_bounce_hit_table_003.mp3")
    ganador_sonido = pygame.mixer.Sound("sonidos/claps.mp3")
    punto_sonido = pygame.mixer.Sound("sonidos/punto.mp3")
    ganador_sonido.set_volume(0.3)

    # Variable para el estado de la música
    musica_activada = True 

    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pong")

    pantalla_inicio(ventana)

    # Configuro reloj para controlar los FPS del juego
    reloj = pygame.time.Clock()

    # Creo las palas y la pelota
    paleta_izquierda = Paleta(20, ALTO // 2 - 50, (pygame.K_w, pygame.K_s))
    paleta_derecha = Paleta(ANCHO - 40, ALTO // 2 - 50, (pygame.K_UP, pygame.K_DOWN))

    pelota = Pelota()

    jugadores = pygame.sprite.Group()
    jugadores.add(paleta_izquierda, paleta_derecha)

    elementos = pygame.sprite.Group()
    elementos.add(paleta_izquierda, paleta_derecha, pelota)

    # Pedir los nombres de los jugadores
    nombre_j1, nombre_j2 = pedir_nombres(ventana, ANCHO, ALTO)

    # Inicializar puntuaciones
    puntuacion_izq = 0
    puntuacion_der = 0
    fuente = pygame.font.Font(None, 36)
    fuente_puntaje = pygame.font.Font(None, 48)  

    ejecutando = True
    ganador = None
    pausado = False

    # Bucle principal del juego
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if ganador is not None:
                    if evento.key == pygame.K_j:
                        # Reiniciar puntajes y estado del juego
                        puntuacion_izq = 0
                        puntuacion_der = 0
                        ganador = None
                        pelota.rect.center = (ANCHO // 2, ALTO // 2)
                        pelota.velocidad_x = random.choice([-4, 4])
                        pelota.velocidad_y = random.choice([-4, 4])

                        # Reiniciar música de fondo si está activada
                        if musica_activada:
                            pygame.mixer.music.play(-1, 0.0)
                    elif evento.key == pygame.K_q:
                        ejecutando = False
                elif evento.key == pygame.K_p:
                    pausado = not pausado
                elif evento.key == pygame.K_m:  # Activar/desactivar música con 'M'
                    musica_activada = not musica_activada
                    if musica_activada:
                        pygame.mixer.music.unpause()  # Reanudar música si estaba pausada
                    else:
                        pygame.mixer.music.pause()  # Pausar música si estaba activada

        if ganador is None and not pausado:
            # Movimiento de las paletas
            paleta_izquierda.mover()
            paleta_derecha.mover()

            # Actualizar la posición de la pelota
            pelota.actualizar()

            # Verificar si la pelota salió por los límites
            if pelota.fuera_lateral:
                if pelota.fuera_lateral == "derecha":
                    puntuacion_der += 1
                elif pelota.fuera_lateral == "izquierda":
                    puntuacion_izq += 1
                punto_sonido.play()

                # Resetea la pelota
                pelota.rect.center = (ANCHO // 2, ALTO // 2)
                pelota.velocidad_x = random.choice([-4, 4])
                pelota.velocidad_y = random.choice([-4, 4])
                pelota.fuera_lateral = False  # Restablece el estado

            # Verifico si hay ganador
            if puntuacion_izq >= 10:
                ganador = f"{nombre_j1} Gana!"
                pygame.mixer.music.stop()
                ganador_sonido.play()
            elif puntuacion_der >= 10:
                ganador = f"{nombre_j2} Gana!"
                pygame.mixer.music.stop()
                ganador_sonido.play()

            # Rebote de la pelota en las paletas
        if pelota.rect.colliderect(paleta_izquierda.rect):
            if pelota.rect.centery < paleta_izquierda.rect.top + paleta_izquierda.rect.height // 3:
                pelota.rect.left = paleta_izquierda.rect.right
                pelota.velocidad_y = -abs(pelota.velocidad_y)
            elif pelota.rect.centery > paleta_izquierda.rect.top + 2 * paleta_izquierda.rect.height // 3:
                pelota.rect.left = paleta_izquierda.rect.right
                pelota.velocidad_y = abs(pelota.velocidad_y)
            else:
                pelota.rect.left = paleta_izquierda.rect.right
                pelota.velocidad_y *= -1
            pelota.velocidad_x *= -1
            pelota.rebotar()
            rebote_sonido.play()

        elif pelota.rect.colliderect(paleta_derecha.rect):
            if pelota.rect.centery < paleta_derecha.rect.top + paleta_derecha.rect.height // 3:
                pelota.rect.right = paleta_derecha.rect.left
                pelota.velocidad_y = -abs(pelota.velocidad_y)
            elif pelota.rect.centery > paleta_derecha.rect.top + 2 * paleta_derecha.rect.height // 3:
                pelota.rect.right = paleta_derecha.rect.left
                pelota.velocidad_y = abs(pelota.velocidad_y)
            else:
                pelota.rect.right = paleta_derecha.rect.left
                pelota.velocidad_y *= -1
            pelota.velocidad_x *= -1
            pelota.rebotar()
            rebote_sonido.play()

        fuente_pequeña = pygame.font.Font(None, 20) 

        ventana.fill(NEGRO)

        if ganador is None:
            # Muestra los nombres de los jugadores
            texto_j1 = fuente.render(nombre_j1, True, BLANCO)
            texto_j2 = fuente.render(nombre_j2, True, BLANCO)
            ventana.blit(texto_j1, (50, 20))
            ventana.blit(texto_j2, (ANCHO - 150, 20))

            # Muestro puntuación
            texto_puntos_izq = fuente_puntaje.render(f"{puntuacion_izq}", True, BLANCO)
            texto_puntos_der = fuente_puntaje.render(f"{puntuacion_der}", True, BLANCO)
            
            ventana.blit(texto_puntos_izq, (180, 20))
            ventana.blit(texto_puntos_der, (ANCHO - 180 - texto_puntos_der.get_width(), 20))

            if pausado:
                texto_pausa = fuente.render("Juego Pausado (Presiona 'P' para continuar)", True, BLANCO)
                ventana.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 2))
            else:
                elementos.draw(ventana)

            texto_musica = fuente_pequeña.render("Presiona 'M' para activar/desactivar la música", True, BLANCO)
            ventana.blit(texto_musica, (ANCHO // 2 - texto_musica.get_width() // 2, ALTO - 40))

            if not pausado:
                texto_pausa_abajo = fuente_pequeña.render("Presiona 'P' para pausar", True, BLANCO)
                ventana.blit(texto_pausa_abajo, (ANCHO // 2 - texto_pausa_abajo.get_width() // 2, ALTO - 80))

            # Dibuja la línea punteada
            dibujar_linea_punteada(ventana)

        else:
            # Muestro el nombre del ganador
            texto_ganador = fuente.render(ganador, True, BLANCO)
            ventana.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2))

            texto_jugar_otra_vez = fuente.render("Presiona 'J' para jugar de nuevo o 'Q' para salir", True, BLANCO)
            ventana.blit(texto_jugar_otra_vez, (ANCHO // 2 - texto_jugar_otra_vez.get_width() // 2, ALTO // 2 + 40))

        pygame.display.update()
        reloj.tick(60)

    pygame.quit()
