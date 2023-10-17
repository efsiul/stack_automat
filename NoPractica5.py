import pygame
import sys
import time

pygame.init()

WHITE           = (255, 255, 255)
BLACK           = (0,   0,   0)
BLUE            = (0,   0,   255)
RED             = (255, 0,   0)
GREEN           = (0,   255, 0)
FUCHSIA         = (255, 0,   255)

WIDTH, HEIGHT   = 900, 800
screen          = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIMULACIÓN AUTÓMATA DE PILA")

ESTADO_INICIAL  = 'q0'
ESTADO_FINAL    = 'q2'
ESTADOS         = ['q0', 'q1', 'q2']

# perilla_x = 50
# perilla_y = 50

def draw(pila, estado_actual, cadena, resalta, mensaje):
    screen.fill(WHITE)

    font        = pygame.font.Font(None, 36)
    text        = font.render(f"Estado: {estado_actual}", True, BLACK)
    screen.blit(text, (20, 20))

    text_pila   = font.render("Pila:", True, BLACK)
    screen.blit(text_pila, (20, 100))

    for valor, rect in pila:
        color   = RED if valor == 'X' else BLUE
        pygame.draw.rect(screen, color, rect)
        text    = font.render(valor, True, WHITE)
        screen.blit(text, (rect.x + 10, rect.y + 10))

    cadena_x    = 200
    cadena_y    = 200

    for i, caracter in enumerate(cadena):
        color = FUCHSIA if i == resalta else BLACK
        text_caracter = font.render(caracter, True, color)
        screen.blit(text_caracter, (cadena_x, cadena_y))
        cadena_x += 36

    text_mensaje = font.render(mensaje, True, BLACK)
    screen.blit(text_mensaje, (50, 150))

    # pygame.draw.circle(screen, GREEN, (perilla_x, perilla_y), 30)
    pygame.display.flip()

def simular(cadena):
    global ESTADO_INICIAL
    
    pila            = [('Z', pygame.Rect(200, 700, 50, 50))]
    estado_actual   = ESTADO_INICIAL
    pila_y          = 700
    resalta         = 0
    
    for caracter in cadena:
        draw(pila, estado_actual, cadena, resalta, f"{caracter}")
        time.sleep(1)

        if estado_actual == ESTADO_INICIAL and caracter == 'a':
            if pila[0] == 'Z':
                continue
            pila.append((caracter, pygame.Rect(200, pila_y - 50, 50, 50)))
            pila_y  -= 50
            resalta += 1
        elif estado_actual == ESTADO_INICIAL and caracter == 'b':
            if pila[-1][0] == 'X':
                pila.pop()
                resalta += 1
            else:
                estado_actual = 'q1'
        elif estado_actual == 'q1' and caracter == 'b':
            pila.append(('X', pygame.Rect(200, pila_y - 50, 50, 50)))
            pila_y  -= 50
            resalta += 1
        elif estado_actual == 'q1' and caracter == 'c':
            pila.pop()
            pila_y  += 50
            resalta += 1
        elif estado_actual == 'q1' and caracter == 'd':
            if len(pila) > 1:
                pila.pop()
                pila_y  += 50
                resalta += 1
            else:
                estado_actual = ESTADO_FINAL
                resalta += 1
                break
        else:
            estado_actual = 'q2'
            break

    if estado_actual == ESTADO_FINAL and len(pila) == 1 and pila[0][0] == 'Z':
        mensaje = "La cadena pertenece al lenguaje L."
    else:
        mensaje = "La cadena no pertenece al lenguaje L."

    draw(pila, estado_actual, cadena, resalta, mensaje)
    time.sleep(5)


# Bucle principal
pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    cadena      = ""
    entrada     = ""
    ingresando  = True
    screen.fill(WHITE)

    while ingresando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key   == pygame.K_RETURN:
                    ingresando  = False
                elif event.key == pygame.K_BACKSPACE:
                    cadena      = cadena[:-1]
                    pos_cadena  = max(0, pos_cadena - 1)
                else:
                    cadena += event.unicode

        entrada = pygame.font.Font(None, 40).render(
            f"Ingresa una cadena: {cadena}", True, BLACK
        )
        screen.blit(entrada, (20, 60))
        pygame.display.flip()

    if cadena.lower() == 'salir':
        break

    pos_cadena = 0  
    simular(cadena)

pygame.quit()
sys.exit()
