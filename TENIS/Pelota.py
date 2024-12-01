import pygame
import random
from configuracion import *

class Pelota(pygame.sprite.Sprite):

    def __init__(self):
        """
        Inicializa la pelota con una posición centrada en la pantalla y una velocidad aleatoria.
        También establece los valores iniciales de los atributos relacionados con los rebotes y límites.
        """
        super().__init__()
        self.image = pygame.Surface((20, 20)) 
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect() 
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad_x = random.choice([-4, 4]) 
        self.velocidad_y = random.choice([-4, 4]) 
        self.rebote_tiempo = 0
        self.fuera_lateral = False  

    def actualizar(self):
        """
        Actualiza la posición de la pelota según su velocidad, detecta los rebotes en los bordes 
        superior e inferior, y verifica si la pelota cruzó los límites izquierdo o derecho de la pantalla.
        """
        # Actualiza la posición de la pelota sumando las velocidades a las coordenadas de la recta
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote en los bordes superior e inferior (al tocar los bordes, la pelota rebota verticalmente)
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.velocidad_y *= -1  # Invierte la velocidad en el eje Y para hacer el rebote

        # Detectar si la pelota cruzó los límites izquierdo o derecho
        if self.rect.left <= 0:  # Si la pelota cruzó el borde izquierdo
            self.fuera_lateral = "derecha"  # Marca que la pelota salió por el lado derecho
        elif self.rect.right >= ANCHO:  # Si la pelota cruzó el borde derecho
            self.fuera_lateral = "izquierda"  # Marca que la pelota salió por el lado izquierdo

        # Si la pelota ha tenido un rebote, disminuye el tiempo de espera para el siguiente rebote
        if self.rebote_tiempo > 0:
            self.rebote_tiempo -= 1

    def incrementar_velocidad(self):
        """
        Incrementa la velocidad de la pelota en un 10% en ambas direcciones (X, Y).
        """
        self.velocidad_x *= 1.1  # Incrementa la velocidad en el eje X
        self.velocidad_y *= 1.1  # Incrementa la velocidad en el eje Y

    def rebotar(self):
        """
        Realiza el rebote de la pelota en las paletas. Solo se ejecuta si el tiempo de rebote ha llegado a 0.
        Al rebotar, la dirección de la pelota en el eje X se invierte, y la velocidad de la pelota aumenta.
        """
        # Solo se ejecuta si el tiempo de rebote ha llegado a 0 (para evitar rebotes consecutivos rápidos)
        if self.rebote_tiempo == 0:
            self.velocidad_x *= -1  # Invierte la dirección de la pelota en el eje X
            self.incrementar_velocidad()  # Incrementa la velocidad de la pelota
            self.rebote_tiempo = 10  # Establece un tiempo de espera de 10 antes del siguiente rebote
