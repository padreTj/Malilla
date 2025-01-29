import pygame
import random
import os
import sys

# Inicializar Pygame
pygame.init()
if not pygame.font.get_init():
    print("Error: No se pudo inicializar el módulo de fuentes de Pygame.")
    sys.exit()

# Configuración inicial de la ventana
ANCHO = 900
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Juego de Cartas - Baraja Española")

# Colores
FONDO = (45, 140, 90)
TEXTO = (255, 255, 255)
ZONA_CENTRO = (70, 70, 70)
ZONA_EQUIPO = (100, 100, 100)

# Fuente
fuente = pygame.font.Font(None, 24)

# Tamaño de las cartas
CARTA_ANCHO = 70
CARTA_ALTO = 120

# Estados del juego
class EstadoJuego:
    def __init__(self):
        self.carta_arrastrada = None
        self.jugador_arrastrando = None
        self.cartas_centro = []
        self.cartas_equipo_a = []
        self.cartas_equipo_b = []
        self.mostrar_popup = False
        self.equipo_popup = ""

estado = EstadoJuego()

def crear_mazo():
    palos = ["oros", "copas", "espadas", "bastos"]
    numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
    return [(palo, numero) for palo in palos for numero in numeros]

def cargar_imagenes():
    imagenes = {}
    for palo in ["oros", "copas", "espadas", "bastos"]:
        for numero in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]:
            ruta = os.path.join("assets", f"{palo}{numero}.jpg")
            if os.path.exists(ruta):
                imagen = pygame.image.load(ruta).convert_alpha()
                imagen = pygame.transform.scale(imagen, (CARTA_ANCHO, CARTA_ALTO))
                imagenes[(palo, numero)] = imagen
    return imagenes

def repartir_cartas():
    mazo = crear_mazo()
    random.shuffle(mazo)
    return {
        "Jugador 1 (Equipo A)": mazo[0:10],
        "Jugador 2 (Equipo B)": mazo[10:20],
        "Jugador 3 (Equipo A)": mazo[20:30],
        "Jugador 4 (Equipo B)": mazo[30:40]
    }

def obtener_posicion_carta(jugador, i, num_cartas):
    solapamiento = 40  # Ajusta este valor para controlar el solapamiento (mitad del ancho de carta)
    
    if jugador == "Jugador 1 (Equipo A)":  # Arriba
        total_width = CARTA_ANCHO + (num_cartas-1)*solapamiento
        start_x = (ANCHO - total_width) // 2
        return (start_x + i*solapamiento, 50)
    
    elif jugador == "Jugador 3 (Equipo A)":  # Abajo
        total_width = CARTA_ANCHO + (num_cartas-1)*solapamiento
        start_x = (ANCHO - total_width) // 2
        return (start_x + i*solapamiento, ALTO - CARTA_ALTO - 50)
    
    elif jugador == "Jugador 2 (Equipo B)":  # Derecha
        total_height = CARTA_ANCHO + (num_cartas-1)*solapamiento
        start_y = (ALTO - total_height) // 2
        return (ANCHO - CARTA_ALTO - 20, start_y + i*solapamiento)
    
    elif jugador == "Jugador 4 (Equipo B)":  # Izquierda
        total_height = CARTA_ANCHO + (num_cartas-1)*solapamiento
        start_y = (ALTO - total_height) // 2
        return (20, start_y + i*solapamiento)

def dibujar_zona_central():
    area_centro = pygame.Rect(ANCHO//2 - 100, ALTO//2 - 75, 200, 150)
    pygame.draw.rect(ventana, ZONA_CENTRO, area_centro, 2)
    
    # Dibujar cartas en el centro
    for i, carta in enumerate(estado.cartas_centro):
        x = ANCHO//2 - CARTA_ANCHO//2 + (i % 2) * 20
        y = ALTO//2 - CARTA_ALTO//2 + (i // 2) * 30
        ventana.blit(imagenes[carta], (x, y))

def dibujar_zonas_equipos():
    # Zona Equipo A
    equipo_a_rect = pygame.Rect(100, ALTO//2 - 50, 100, 100)
    pygame.draw.rect(ventana, ZONA_EQUIPO, equipo_a_rect, 2)
    
    # Zona Equipo B
    equipo_b_rect = pygame.Rect(ANCHO - 200, ALTO//2 - 50, 100, 100)
    pygame.draw.rect(ventana, ZONA_EQUIPO, equipo_b_rect, 2)

def mostrar_popup_cartas(equipo):
    estado.mostrar_popup = True
    estado.equipo_popup = equipo
    
    while estado.mostrar_popup:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                estado.mostrar_popup = False
        
        ventana.fill((200, 200, 200))
        cartas = estado.cartas_equipo_a if equipo == "A" else estado.cartas_equipo_b
        
        for i, carta in enumerate(cartas):
            x = 50 + (i % 4) * (CARTA_ANCHO + 10)
            y = 50 + (i // 4) * (CARTA_ALTO + 10)
            ventana.blit(imagenes[carta], (x, y))
        
        pygame.display.flip()
        pygame.time.wait(10)

def manejar_eventos(jugadores):
    mouse_pos = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif evento.type == pygame.VIDEORESIZE:
            global ANCHO, ALTO
            ANCHO, ALTO = evento.size
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Click izquierdo
                # Verificar si se clickeó una zona de equipo
                equipo_a_rect = pygame.Rect(100, ALTO//2 - 50, 100, 100)
                equipo_b_rect = pygame.Rect(ANCHO - 200, ALTO//2 - 50, 100, 100)
                
                if equipo_a_rect.collidepoint(mouse_pos):
                    mostrar_popup_cartas("A")
                elif equipo_b_rect.collidepoint(mouse_pos):
                    mostrar_popup_cartas("B")
                else:
                    # Buscar carta clickeada
                    found = False
                for jugador in reversed(jugadores.keys()):
                    cartas = jugadores[jugador]
                    for i in reversed(range(len(cartas))):
                        carta = cartas[i]
                        pos = obtener_posicion_carta(jugador, i, len(cartas))
                        
                        # Ajustar rectángulo de colisión según orientación
                        if jugador in ["Jugador 2 (Equipo B)", "Jugador 4 (Equipo B)"]:
                            rect = pygame.Rect(pos[0], pos[1], CARTA_ALTO, CARTA_ANCHO)
                        else:
                            rect = pygame.Rect(pos[0], pos[1], CARTA_ANCHO, CARTA_ALTO)
                        
                        if rect.collidepoint(mouse_pos):
                            estado.carta_arrastrada = carta
                            estado.jugador_arrastrando = jugador
                            found = True
                            break
                                
                    # Verificar cartas en el centro
                    centro_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2 - 75, 200, 150)
                    if centro_rect.collidepoint(mouse_pos) and len(estado.cartas_centro) >= 4:
                        estado.carta_arrastrada = "GRUPO_CENTRO"
                        
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and estado.carta_arrastrada:
                # Soltar en el centro
                centro_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2 - 75, 200, 150)
                if centro_rect.collidepoint(mouse_pos):
                    if estado.carta_arrastrada != "GRUPO_CENTRO":
                        jugadores[estado.jugador_arrastrando].remove(estado.carta_arrastrada)
                        estado.cartas_centro.append(estado.carta_arrastrada)
                
                # Soltar en equipo
                equipo_a_rect = pygame.Rect(100, ALTO//2 - 50, 100, 100)
                equipo_b_rect = pygame.Rect(ANCHO - 200, ALTO//2 - 50, 100, 100)
                
                if estado.carta_arrastrada == "GRUPO_CENTRO":
                    if equipo_a_rect.collidepoint(mouse_pos):
                        estado.cartas_equipo_a.extend(estado.cartas_centro)
                        estado.cartas_centro = []
                    elif equipo_b_rect.collidepoint(mouse_pos):
                        estado.cartas_equipo_b.extend(estado.cartas_centro)
                        estado.cartas_centro = []
                
                estado.carta_arrastrada = None
                estado.jugador_arrastrando = None

def dibujar_cartas(jugadores, imagenes, mostrar_todas=True):
    ventana.fill(FONDO)
    
    # Dibujar zonas
    dibujar_zona_central()
    dibujar_zonas_equipos()
    
    # Dibujar cartas de jugadores
    for jugador, cartas in jugadores.items():
        num_cartas = len(cartas)
        texto = fuente.render(jugador, True, TEXTO)
        
        for i, carta in enumerate(cartas):
            pos = obtener_posicion_carta(jugador, i, num_cartas)
            
            # Si es la carta arrastrada, dibujar en posición del mouse
            if carta == estado.carta_arrastrada and jugador == estado.jugador_arrastrando:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                ventana.blit(imagenes[carta], (mouse_x - CARTA_ANCHO//2, mouse_y - CARTA_ALTO//2))
            else:
                if jugador in ["Jugador 2 (Equipo B)", "Jugador 4 (Equipo B)"]:
                    img = pygame.transform.rotate(imagenes[carta], -90 if jugador == "Jugador 2 (Equipo B)" else 90)
                    ventana.blit(img, pos)
                else:
                    ventana.blit(imagenes[carta], pos)
        
        # Dibujar nombre del jugador
        # if jugador == "Jugador 1 (Equipo A)":
        #     texto_pos = (ANCHO//2 - texto.get_width()//2, 20)
        # elif jugador == "Jugador 3 (Equipo A)":
        #     texto_pos = (ANCHO//2 - texto.get_width()//2, ALTO - 30)
        # elif jugador == "Jugador 2 (Equipo B)":
        #     texto_pos = (ANCHO - texto.get_width() - 30, ALTO//2 - texto.get_height()//2)
        # else:
        #     texto_pos = (30, ALTO//2 - texto.get_height()//2)
            
        # ventana.blit(texto, texto_pos)
    
    # Dibujar grupo del centro si se está arrastrando
    if estado.carta_arrastrada == "GRUPO_CENTRO":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, carta in enumerate(estado.cartas_centro):
            x = mouse_x - CARTA_ANCHO//2 + (i % 2) * 20
            y = mouse_y - CARTA_ALTO//2 + (i // 2) * 30
            ventana.blit(imagenes[carta], (x, y))
    
    pygame.display.flip()

def main():
    global imagenes
    jugadores = repartir_cartas()
    imagenes = cargar_imagenes()
    
    while True:
        manejar_eventos(jugadores)
        dibujar_cartas(jugadores, imagenes)

if __name__ == "__main__":
    main()