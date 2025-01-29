import pygame
import random
import os
import sys

# Inicializar Pygame
pygame.init()
if not pygame.font.get_init():
    print("Error: No se pudo inicializar el módulo de fuentes de Pygame.")
    sys.exit()

# Configuración de la ventana
ANCHO = 1200
ALTO = 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cartas - Baraja Española")

# Colores
FONDO = (45, 140, 90)
TEXTO = (255, 255, 255)

# Fuente
fuente = pygame.font.Font(None, 24)

# Tamaño de las cartas
CARTA_ANCHO = 80
CARTA_ALTO = 120

# Crear mazo español
def crear_mazo():
    palos = ["oros", "copas", "espadas", "bastos"]
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [(palo, numero) for palo in palos for numero in numeros]

# Cargar imágenes de las cartas
def cargar_imagenes():
    imagenes = {}
    palos = ["oros", "copas", "espadas", "bastos"]
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    
    for palo in palos:
        for numero in numeros:
            nombre_archivo = f"{palo}{numero}.jpg"
            ruta = os.path.join("assets", nombre_archivo)
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (CARTA_ANCHO, CARTA_ALTO))
                imagenes[(palo, numero)] = imagen
    return imagenes

# Barajar y repartir cartas
def repartir_cartas():
    mazo = crear_mazo()
    random.shuffle(mazo)
    return {
        "Jugador 1 (Equipo A)": mazo[0:10],
        "Jugador 2 (Equipo B)": mazo[10:20],
        "Jugador 3 (Equipo A)": mazo[20:30],
        "Jugador 4 (Equipo B)": mazo[30:40]
    }

# Dibujar cartas rotadas hacia el centro
def dibujar_cartas(jugadores, imagenes, mostrar_todas=False):
    ventana.fill(FONDO)
    posiciones = {
        "Jugador 1 (Equipo A)": (100, 50),              # Arriba
        "Jugador 2 (Equipo B)": (ANCHO - 120, ALTO//2), # Derecha
        "Jugador 3 (Equipo A)": (100, ALTO - 150),      # Abajo
        "Jugador 4 (Equipo B)": (50, ALTO//2)           # Izquierda
    }
    
    for jugador, cartas in jugadores.items():
        x, y = posiciones[jugador]
        texto = fuente.render(jugador, True, TEXTO)
        
        # Centrar texto para jugadores laterales
        if jugador in ["Jugador 2 (Equipo B)", "Jugador 4 (Equipo B)"]:
            ventana.blit(texto, (x - texto.get_width()//2, y - 50))
        else:
            ventana.blit(texto, (x, y - 30))
        
        cartas_a_mostrar = cartas if mostrar_todas else ([cartas[0]] if "Equipo A" in jugador else [])
        
        for i, carta in enumerate(cartas_a_mostrar):
            if carta not in imagenes:
                continue

            imagen = imagenes[carta]
            
            # Rotar cartas laterales hacia el centro
            if jugador == "Jugador 4 (Equipo B)":  # Izquierda
                imagen_rotada = pygame.transform.rotate(imagen, 90)
                pos_x = x
                pos_y = y + i * (imagen_rotada.get_height() + 10)
                
            elif jugador == "Jugador 2 (Equipo B)":  # Derecha
                imagen_rotada = pygame.transform.rotate(imagen, -90)
                pos_x = x
                pos_y = y + i * (imagen_rotada.get_height() + 10)
                
            else:  # Arriba y abajo
                imagen_rotada = imagen
                pos_x = x + i * (CARTA_ANCHO + 10)
                pos_y = y

            ventana.blit(imagen_rotada, (pos_x, pos_y))
    
    pygame.display.flip()

# Bucle principal
def main():
    jugadores = repartir_cartas()
    imagenes = cargar_imagenes()
    mostrar_todas = False
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                mostrar_todas = not mostrar_todas
        
        dibujar_cartas(jugadores, imagenes, mostrar_todas)

if __name__ == "__main__":
    main()