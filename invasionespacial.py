import pygame
import random
import math
from pygame import mixer

#Inicizlizar pygame
pygame.init()

#Creacion de la pantalla
pantalla = pygame.display.set_mode((800,600))

#Configuracion de titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("juego/extraterrestre.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("juego/fondo.jpg")


#Musica
mixer.music.load("juego/Flying Microtonal Banana.mp3")
mixer.music.set_volume(0.6)
mixer.music.play(-1)

#Crear jugador
img_jugador = pygame.image.load("juego/transbordador-espacial.png")
jugadorX = 368
jugadorY = 500
jugadorX_cambio = 0

#Crear enemigo
img_enemigo = []
enemigoX = []
enemigoY = []
enemigoX_cambio = []
enemigoY_cambio= []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):

    img_enemigo.append(pygame.image.load("juego/ovni.png"))
    enemigoX.append(random.randint(0, 736))
    enemigoY.append(random.randint(50,200))
    enemigoX_cambio.append(0.5)
    enemigoY_cambio.append(50)

#Crear bala
balas = []
img_bala = pygame.image.load("juego/laser.png")
balaX = 0
balaY = 484
balaX_cambio = 0
balaY_cambio= 0.5
bala_visible = False


#Score
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 32)
textoX = 10
textoY = 10

#Texto del final
fuente_final = pygame.font.Font("freesansbold.ttf", 40)

#Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

#Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


#Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#Funcion disparo
def disparo(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+10))

#Deteccion de colisiones

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    if distancia < 30:
        return True
    else:
        return False
    

#Funcion texto final
def texto_final():
    mifuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mifuente_final, (200, 200))

#loop del juego
se_ejecuta = True
while se_ejecuta:
    #imagend e fondo
    pantalla.blit(fondo, (0,0))


# Iterar eventos 
    for evento in pygame.event.get():

        #Evento para cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento para presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugadorX_cambio = -0.2
            if evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0.2
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("juego/disparo.mp3")
                sonido_bala.play()
                if not bala_visible:
                     nueva_bala = {
                    "x": jugadorX,
                    "y": jugadorY,
                    "velocidad": -0.5
                    }
                balas.append(nueva_bala)
            

        #Evento de soltado de fechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0

    #Modificar posicion de jugador
    jugadorX += jugadorX_cambio
    #Mantener en bordes al jugador
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736


    #Modificar posicion de enemigo
    for e in range(cantidad_enemigos):

        #fin del juego
        if enemigoY[e] > 500:
            for k in range(cantidad_enemigos):
                enemigoY[k] = 1000
            texto_final()
            break

        enemigoX[e] += enemigoX_cambio[e]

    #Mantener en bordes al enemigo
        if enemigoX[e] <= 0:
            enemigoX_cambio[e] = 0.5
            enemigoY[e] += enemigoY_cambio[e]
        elif enemigoX[e] >= 736:
            enemigoX_cambio[e] = -0.5
            enemigoY[e] += enemigoY_cambio[e]

        #Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigoX[e], enemigoY[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("juego/Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigoX[e] = random.randint(0, 736)
                enemigoY[e] = random.randint(20, 200)
                break
 
        enemigo(enemigoX[e], enemigoY[e], e)



    #movimiento de bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)



    


    jugador(jugadorX, jugadorY)

    mostrar_puntaje(textoX, textoY)
    

    #Actualizar pantalla
    pygame.display.update()

   