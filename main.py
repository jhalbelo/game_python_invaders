import random
import math
import pygame
from pygame import mixer
import io

pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))
fondo = pygame.image.load("fondo.jpg")
# Titulo e Icono

pygame.display.set_caption("Invasion del espacio")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
# agregar musica
sonido_colision = mixer.Sound('explosion.mp3')
sonido_bala = mixer.Sound('disparo.mp3')
sonido_fin = mixer.Sound('game-over.mp3')
mixer.music.load('fondo.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)
# variables jugador

img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

#Convertir fuente


def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes('retro.ttf')
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10


# Mostrar puntaje


def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# funcion texto final


fuente_final = pygame.font.Font(fuente_como_bytes, 48)


def texto_final():
    sonido_fin.play(1)
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (120, 200))

# funcion jugador


def jugador(x, y):
    pantalla.blit(img_jugador, [x, y])

# variables enemigo


img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("nave-espacial.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(0, 100))
    enemigo_x_cambio.append(0.2)
    enemigo_y_cambio.append(32)

# funcion enemigo


def enemigo(ene, x, y):
    pantalla.blit(img_enemigo[ene], [x, y])

# variables balas


img_bala = pygame.image.load("laser2.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 0.5
bala_visible = False

# Funcion disparar bala


def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y-10))

# Detectar colision


def hay_colision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distance < 27:
        return True
    else:
        return False

# Loop del juego


se_ejecuta = True
while se_ejecuta:
    # iterar eventos
    for event in pygame.event.get():
        # evento salir
        if event.type == pygame.QUIT:
            se_ejecuta = False
        # evento teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if event.key == pygame.K_SPACE:

                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        # evento parar
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    # modificar pantalla
    pantalla.blit(fondo, (0, 0))
    # modificar ubicacion jugador
    jugador_x += jugador_x_cambio
    # mantener dentor de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736
    # posicionar jugador
    jugador(jugador_x, jugador_y)
    # modificar ubicacion enemigo
    for e in range(cantidad_enemigos):
        # fin del juego
        if enemigo_y[e] > 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

    # mantener dentor de la pantalla al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.2
            enemigo_y[e] += enemigo_y_cambio[e]
        if enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.2
            enemigo_y[e] += enemigo_y_cambio[e]
        # Posicionar enemigo
        enemigo(e, enemigo_x[e], enemigo_y[e])
        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:

            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(0, 100)
    # mover bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio
    # mostrar puntaje
    mostrar_puntaje(texto_x, texto_y)

    # actualizar pantalla
    pygame.display.update()
