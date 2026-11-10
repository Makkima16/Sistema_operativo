import random

import pygame


def iniciar_culebrita():
    pygame.init()

    ANCHO, ALTO = 800, 600
    TAMANIO_CUADRO = 20

    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    VERDE = (0, 255, 0)
    ROJO = (255, 0, 0)

    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Culebrita")
    reloj = pygame.time.Clock()

    def dibujar_serpiente(serpiente):
        for segmento in serpiente:
            pygame.draw.rect(
                ventana, VERDE,
                pygame.Rect(segmento[0], segmento[1], TAMANIO_CUADRO, TAMANIO_CUADRO),
            )

    def generar_comida():
        x = random.randint(0, (ANCHO // TAMANIO_CUADRO) - 1) * TAMANIO_CUADRO
        y = random.randint(0, (ALTO // TAMANIO_CUADRO) - 1) * TAMANIO_CUADRO
        return x, y

    def mostrar_game_over(puntuacion):
        fuente = pygame.font.Font(None, 48)
        texto = fuente.render("Game Over", True, ROJO)
        texto_reiniciar = pygame.font.Font(None, 36).render(
            "Presiona R para reiniciar o Q para salir", True, BLANCO
        )
        puntuacion_texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)

        ventana.fill(NEGRO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 3))
        ventana.blit(puntuacion_texto, (ANCHO // 2 - puntuacion_texto.get_width() // 2, ALTO // 2))
        ventana.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 1.5))
        pygame.display.flip()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        return True
                    if evento.key == pygame.K_q:
                        return False

    def jugar():
        serpiente = [[100, 100]]
        direccion = "DERECHA"
        comida = generar_comida()
        puntuacion = 0

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        return False
                    if evento.key == pygame.K_UP and direccion != "ABAJO":
                        direccion = "ARRIBA"
                    elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
                        direccion = "ABAJO"
                    elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
                        direccion = "IZQUIERDA"
                    elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                        direccion = "DERECHA"

            cabeza = serpiente[0][:]
            if direccion == "ARRIBA":
                cabeza[1] -= TAMANIO_CUADRO
            elif direccion == "ABAJO":
                cabeza[1] += TAMANIO_CUADRO
            elif direccion == "IZQUIERDA":
                cabeza[0] -= TAMANIO_CUADRO
            elif direccion == "DERECHA":
                cabeza[0] += TAMANIO_CUADRO

            serpiente.insert(0, cabeza)

            if cabeza == list(comida):
                comida = generar_comida()
                puntuacion += 1
            else:
                serpiente.pop()

            choco_pared = (
                cabeza[0] < 0 or cabeza[0] >= ANCHO
                or cabeza[1] < 0 or cabeza[1] >= ALTO
            )
            choco_consigo = cabeza in serpiente[1:]

            if choco_pared or choco_consigo:
                return mostrar_game_over(puntuacion)

            ventana.fill(NEGRO)
            dibujar_serpiente(serpiente)
            pygame.draw.rect(
                ventana, ROJO,
                pygame.Rect(comida[0], comida[1], TAMANIO_CUADRO, TAMANIO_CUADRO),
            )

            fuente = pygame.font.Font(None, 36)
            texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
            ventana.blit(texto, (10, 10))

            pygame.display.flip()
            reloj.tick(3 + puntuacion // 3)

    reiniciar = True
    while reiniciar:
        reiniciar = jugar()

    pygame.quit()
