import pygame
from modulos.configuracion import BLANCO, ANCHO, ALTO

class Paleta(pygame.sprite.Sprite):
    """
    Clase que representa una paleta en el juego.
    """
    def __init__(self, x, y, controles):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(BLANCO)

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

        self.velocidad = 5

        self.controles = controles  # ('arriba', 'abajo') como tuplas de teclas

    def mover(self):
        """
        Mueve la paleta en función de las teclas presionadas.

        La paleta se mueve hacia arriba si se presiona la tecla de 'arriba' y si
        no se ha alcanzado el límite superior de la ventana. Se mueve hacia abajo
        si se presiona la tecla de 'abajo' y si no se ha alcanzado el límite inferior.
        """
        # Obtener el estado de todas las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Mover hacia arriba si se presiona la tecla 'arriba' y no se supera el límite superior
        if teclas[self.controles[0]] and self.rect.top > 0:
            self.rect.y -= self.velocidad

        # Mover hacia abajo si se presiona la tecla 'abajo' y no se supera el límite inferior
        if teclas[self.controles[1]] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad
