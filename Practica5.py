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

estado_positions = {                                                # Posiciones de los estados en el círculo

    'q0': (300, 400),
    'q1': (450, 250),
    'q2': (600, 400),
}

circle_radius = 150                                                 # Radio del círculo que contiene los estados


def draw_pila(pila):
    font = pygame.font.Font(None, 36)
    for valor, rect in pila:
        color   = RED if valor == 'd' else BLUE
        pygame.draw.rect(screen, color, rect)
        text    = font.render(valor, True, WHITE)
        screen.blit(text, (rect.x + 10, rect.y + 10))

def draw_states(estado_actual):
    for estado, pos in estado_positions.items():
        color       = GREEN if estado == estado_actual else BLACK
        pygame.draw.circle(screen, color, pos, 30)
        font        = pygame.font.Font(None, 36)
        text        = font.render(estado, True, WHITE)
        text_rect   = text.get_rect(center=pos)
        screen.blit(text, text_rect)

def draw(cadena, pila, estado_actual, mensaje):
    screen.fill(WHITE)

    pygame.draw.circle(screen, BLACK, (450, 400), circle_radius, 2) # Dibuja el círculo que contiene los estados
    draw_states(estado_actual)

    font = pygame.font.Font(None, 36)                               # Dibuja la cadena y la pila
    text_cadena = font.render(f"Cadena: {cadena}", True, BLACK)     
    screen.blit(text_cadena, (20, 60))

    mensaje_lines = mensaje.split('\n')
    y_position = 150
    for line in mensaje_lines:
        text_mensaje = font.render(line, True, BLACK)
        screen.blit(text_mensaje, (20, y_position))
        y_position += 40


    draw_pila(pila)

    pygame.display.flip()

def simular(cadena):  # sourcery skip: low-code-quality
    global ESTADO_INICIAL
    pila            = [('Z', pygame.Rect(200, 700, 50, 50))]
    estado_actual   = ESTADO_INICIAL
    pila_y          = 700
    cont_D          = 0
    contadores      = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

    for caracter in cadena:
        draw(cadena, pila, estado_actual, f"Transición: {caracter}")
        time.sleep(1)

        if caracter not in ['a', 'b', 'c', 'd']:
            contadores['d'] += 1
            break
        contadores[caracter] += 1
        if caracter   == 'd':
            cont_D += 1

        if estado_actual    == ESTADO_INICIAL and caracter == 'a' and contadores['a'] == 1:
            estado_actual   = 'q1'

        elif estado_actual  == 'q1' and caracter == 'b':
            pila.append((caracter, pygame.Rect(200, pila_y - 50, 50, 50)))
            estado_actual   = 'q1' 
            pila_y          -= 50

        elif estado_actual  == 'q1' and caracter == 'c' and contadores['c'] == 1:
            estado_actual   = 'q2' 

        elif estado_actual  == 'q2' and caracter == 'd':
            if len(pila) > 1 and pila[-1][0] == 'b':
                pila.pop()
                pila_y          += 50
                contadores['d'] -= 1
            elif not pila:
                break
            else:
                estado_actual = ESTADO_FINAL
                break


    if  (   contadores['a'] == 1
        and contadores['c'] == 1
        and estado_actual   == ESTADO_FINAL
        and len(pila)       == 1
        and pila[0][0]      == 'Z'
        and contadores['d'] == 0):
        mensaje = f"LA CADENA {cadena} PERTENECE AL LENGUAJE L.\n CONTIENE {contadores['a']} AES, {contadores['b']} BES, {contadores['c']} CES y {cont_D} DES."
    else:
        mensaje = f"LA CADENA {cadena} NO PERTENECE AL LENGUAJE L.\n CONTIENE {contadores['a']} AES, {contadores['b']} BES, {contadores['c']} CES y {cont_D} DES."

    draw(cadena, pila, estado_actual, mensaje)
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
                else:
                    cadena += event.unicode

        entrada = pygame.font.Font(None, 40).render(
            f"Ingresa una cadena: {cadena}", True, BLACK
        )
        screen.blit(entrada, (30, 60))
        pygame.display.flip()

    if cadena.lower() == 'salir':
        break

    simular(cadena)

pygame.quit()
sys.exit()
