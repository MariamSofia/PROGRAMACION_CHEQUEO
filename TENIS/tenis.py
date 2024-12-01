import pygame
import random

# Función para dibujar la línea punteada en el centro
def dibujar_linea_punteada():
    # Establecer el color y el tamaño de la línea
    color = BLANCO
    x = ANCHO // 2  # Coordenada X en el centro de la pantalla
    y_inicio = 0
    y_fin = ALTO

    # Usamos un bucle para dibujar la línea punteada
    for y in range(y_inicio, y_fin, 20):  # A intervalos de 20 píxeles
        pygame.draw.line(ventana, color, (x, y), (x, y + 10))

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 800
ALTO = 600

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Cargar y reproducir música de fondo
pygame.mixer.music.load("African_fun_long.mp3")
pygame.mixer.music.set_volume(0.05)  # Volumen bajo
pygame.mixer.music.play(-1, 0.0)  # -1 para que se repita en bucle

rebote_sonido = pygame.mixer.Sound("sport_table_tennis_ping_pong_ball_bounce_hit_table_003.mp3")
ganador_sonido = pygame.mixer.Sound("claps.mp3")
ganador_sonido.set_volume(0.3)

# Configurar ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong")

# Configurar reloj
reloj = pygame.time.Clock()

# Clase para las paletas
class Paleta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 5

    def mover(self, arriba, abajo):
        teclas = pygame.key.get_pressed()
        if teclas[arriba] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[abajo] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

# Clase para la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad_x = random.choice([-4, 4])
        self.velocidad_y = random.choice([-4, 4])
        self.rebote_tiempo = 0  # Tiempo de espera para evitar múltiples rebotes
        self.fuera_lateral = False  # Indica si cruzó los límites izquierdo o derecho

    def actualizar(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote en los bordes superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.velocidad_y *= -1

        # Detectar si cruza los límites izquierdo o derecho
        if self.rect.left <= 0:
            self.fuera_lateral = "derecha"
        elif self.rect.right >= ANCHO:
            self.fuera_lateral = "izquierda"

        # Reducir el contador de tiempo de rebote
        if self.rebote_tiempo > 0:
            self.rebote_tiempo -= 1

    def incrementar_velocidad(self):
        self.velocidad_x *= 1.1
        self.velocidad_y *= 1.1

    def rebotar(self):
        # Solo rebota si el tiempo de rebote ha llegado a 0
        if self.rebote_tiempo == 0:
            self.velocidad_x *= -1  # Cambia de dirección
            self.incrementar_velocidad()
            self.rebote_tiempo = 10  # Establece un tiempo de espera para el próximo rebote

# Función para pedir el nombre de los jugadores
def pedir_nombres():
    # Crear fuente de texto
    fuente = pygame.font.Font(None, 36)
    
    nombre_j1 = ""
    nombre_j2 = ""
    
    input_activo = 1  # 1 para jugador 1, 2 para jugador 2
    texto = "Ingrese nombre Jugador 1:"  # Instrucción de texto

    while True:
        ventana.fill(NEGRO)

        # Mostrar las instrucciones
        texto_instrucciones = fuente.render(texto, True, BLANCO)
        ventana.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 4))

        # Mostrar el texto ingresado por cada jugador
        if input_activo == 1:
            texto_j1_render = fuente.render(nombre_j1, True, BLANCO)
            ventana.blit(texto_j1_render, (ANCHO // 2 - texto_j1_render.get_width() // 2, ALTO // 2))
        elif input_activo == 2:
            texto_j2_render = fuente.render(nombre_j2, True, BLANCO)
            ventana.blit(texto_j2_render, (ANCHO // 2 - texto_j2_render.get_width() // 2, ALTO // 2))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    # Eliminar el último carácter
                    if input_activo == 1:
                        nombre_j1 = nombre_j1[:-1]
                    elif input_activo == 2:
                        nombre_j2 = nombre_j2[:-1]
                elif evento.key == pygame.K_RETURN:
                    # Avanzar al siguiente jugador o empezar el juego
                    if input_activo == 1:
                        texto = "Ingrese nombre Jugador 2:"
                        input_activo = 2
                    elif input_activo == 2:
                        return nombre_j1, nombre_j2
                else:
                    # Añadir el carácter a la entrada del jugador
                    if input_activo == 1:
                        nombre_j1 += evento.unicode
                    elif input_activo == 2:
                        nombre_j2 += evento.unicode

# Configurar juego
paleta_izquierda = Paleta(20, ALTO // 2 - 50)
paleta_derecha = Paleta(ANCHO - 40, ALTO // 2 - 50)
pelota = Pelota()

jugadores = pygame.sprite.Group()
jugadores.add(paleta_izquierda, paleta_derecha)

elementos = pygame.sprite.Group()
elementos.add(paleta_izquierda, paleta_derecha, pelota)

# Pedir los nombres de los jugadores
nombre_j1, nombre_j2 = pedir_nombres()

# Inicializar puntuaciones
puntuacion_izq = 0
puntuacion_der = 0
fuente = pygame.font.Font(None, 36)
fuente_puntaje = pygame.font.Font(None, 48)  # Fuente más grande para el puntaje

ejecutando = True
ganador = None
pausado = False

# Bucle principal
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

                    # Reiniciar música de fondo
                    pygame.mixer.music.play(-1, 0.0)
                elif evento.key == pygame.K_q:
                    ejecutando = False
            elif evento.key == pygame.K_p:
                pausado = not pausado

    if ganador is None and not pausado:
        # Movimiento de las paletas
        paleta_izquierda.mover(pygame.K_w, pygame.K_s)
        paleta_derecha.mover(pygame.K_UP, pygame.K_DOWN)

        # Actualizar la posición de la pelota
        pelota.actualizar()

        # Verificar si la pelota salió por los límites
        if pelota.fuera_lateral:
            if pelota.fuera_lateral == "derecha":
                puntuacion_der += 1
            elif pelota.fuera_lateral == "izquierda":
                puntuacion_izq += 1

            # Resetear la pelota
            pelota.rect.center = (ANCHO // 2, ALTO // 2)
            pelota.velocidad_x = random.choice([-4, 4])
            pelota.velocidad_y = random.choice([-4, 4])
            pelota.fuera_lateral = False  # Restablecer el estado

        # Verificar si hay ganador
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

    # Dibujar elementos
    ventana.fill(NEGRO)
    if ganador is None:
        # Mostrar nombres de los jugadores
        texto_j1 = fuente.render(nombre_j1, True, BLANCO)
        texto_j2 = fuente.render(nombre_j2, True, BLANCO)
        ventana.blit(texto_j1, (50, 20))
        ventana.blit(texto_j2, (ANCHO - 150, 20))

        # Mostrar puntuación
        texto_puntos_izq = fuente_puntaje.render(f"{puntuacion_izq}", True, BLANCO)
        texto_puntos_der = fuente_puntaje.render(f"{puntuacion_der}", True, BLANCO)
        
        # Dibujar los puntajes un poco más lejos de los nombres
        ventana.blit(texto_puntos_izq, (180, 20))
        ventana.blit(texto_puntos_der, (ANCHO - 180 - texto_puntos_der.get_width(), 20))

        if pausado:
            texto_pausa = fuente.render("Juego Pausado (Presiona 'P' para continuar)", True, BLANCO)
            ventana.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 2))
        else:
            elementos.draw(ventana)

        # Dibujar la línea punteada
        dibujar_linea_punteada()

    else:
        # Pantalla de fin del juego
        texto_ganador = fuente.render(ganador, True, BLANCO)
        texto_reinicio = fuente.render("Aprete 'J' para jugar nuevamente o 'Q' para salir", True, BLANCO)
        ventana.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, ALTO // 2 - 50))
        ventana.blit(texto_reinicio, (ANCHO // 2 - texto_reinicio.get_width() // 2, ALTO // 2 + 10))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
