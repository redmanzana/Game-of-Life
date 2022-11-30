import pygame, sys
from PIL import Image
import numpy as np

pygame.init()

#Variables indican cuanto recorrer cuadricula (útiles en resize)
difx = 0
dify = 0

# Se establece el número de celdas en el eje x e y
ncx, ncy = 20, 20

#Definimos tamaño
altura = 400
ancho = 400
size = (ancho, altura)

#Tamaño de las celdas
tx = ancho/ncx
ty = altura/ncy

# Se crean las matriz que va a guardar los estados de las celdas
CellState = np.zeros((100, 100), np.int8)
nextCellState = np.zeros((100, 100), np.int8)

#Guarda el estado de juego
pause = True

#Definimos la escala a la que queremos que esten los botones
scale = .4

#Obtemeos la imagen (Especie de Array)
start = Image.open('starbotton.jpg')
#Ancho y Altura original de la imagen (útil para no perder proporción)
start_x, start_y = start.size
#Pasamos la imagen a un objeto de pygame para facilitar el uso de funciones como "blit"
start = pygame.image.fromstring(start.tobytes(),(start_x, start_y), start.mode)
#Se escala el tamaño de la imagen (Ancho como determinanate)
start = pygame.transform.smoothscale(start, (ancho*scale, (ancho*scale)*(start_y/start_x)))

#Hacemos un paralelo/otros botones
options = Image.open('starbotton.jpg')
options_x, options_y = options.size
options = pygame.image.fromstring(options.tobytes(),(options_x, options_y), options.mode)
options = pygame.transform.smoothscale(options, (ancho*scale, (ancho*scale)*(options_y/options_x)))

credit = Image.open('starbotton.jpg')
credit_x, credit_y = credit.size
credit = pygame.image.fromstring(credit.tobytes(),(credit_x, credit_y), credit.mode)
credit = pygame.transform.smoothscale(credit, (ancho*scale, (ancho*scale)*(credit_y/credit_x)))

#Se crea la pantalla
screen = pygame.display.set_mode((ancho, altura),  pygame.RESIZABLE)

# Se establece el color de fondo de la pantalla
bg = 25, 25, 25;
screen.fill(bg)

#Preparamos la velocidad de refresco
fps = 60;
clock=pygame.time.Clock()

#Delimita o reduce el area de colición (Usada en botones)
#Para evitar falsos clicks
HitBoxLeft = altura/20
HitBoxRigth = -ancho/20

# "Global" Le indica a las funciones que
# se trata de variables declaradas fuera (arriba)
# se debe usar cuando (=)

#Dibuja las superficies del ciclo principal (Botones/pantalla)
def Dibujo_Surfaces():
    screen.fill(bg)
    pygame.Surface.blit(screen, start, ((screen.get_width()/2)-(start.get_width()/2), altura/3))
    pygame.Surface.blit(screen, options, ((screen.get_width()/2)-(options.get_width()/2), altura/2))
    pygame.Surface.blit(screen, credit, ((screen.get_width()/2)-(credit.get_width()/2), altura/1.5))

#En caso de RESIZE se modifica el tamaño que tendran las celdas (Necesita nuevo tamaño)
def AjusteTamano_Celdas(event_w, event_h):
    #"global" para que tome las variables exteriores a la función ('=')
    global difx, dify, tx, ty, altura, ancho
    #Se toma al lado menor para conservar la proporción de un cuadrado
    if(event_w < event_h):
        altura = ancho = event_w
        dify = (event_h - ancho) / 2
        difx = 0
    else:
        altura = ancho = event_h
        difx = (event_w - altura) / 2
        dify = 0
    #Ajustamos tamaño de las celdas
    tx = ancho / ncx
    ty = altura / ncy

#En caso de RESIZE se modifica el tamaño de los botones, y pantalla (Necesita nuevo tamaño)
def AjusteTamano_Surfaces(event_w, event_h):
    #Ajustamos la pantalla de tamaño // POSIBLEMENTE NEGOCIABLE
    global screen, start, options, credit, HitBoxLeft, HitBoxRigth
    screen = pygame.display.set_mode((event_w, event_h), pygame.RESIZABLE)
    #Reajustamos tamaño boton
    start = pygame.transform.smoothscale(start, (ancho*scale, (ancho*scale)*(start_y/start_x)))
    options = pygame.transform.smoothscale(options, (ancho*scale, (ancho*scale)*(options_y/options_x)))
    credit = pygame.transform.smoothscale(credit, (ancho*scale, (ancho*scale)*(credit_y/credit_x)))
    #Nuevo valor para las HitBox
    HitBoxLeft = altura/20
    HitBoxRigth = -ancho/20

#Verifica si click sobre un boton (Necesita posición mouse) (Regresa string)
def Colision_Surfaces_Main(Mse_px, Mse_py):
    #Si se trata de los botones de menu
    if Mse_px > (screen.get_width()/2)-(start.get_width()/2)+HitBoxLeft and \
    Mse_px < ((screen.get_width()/2)+(start.get_width()/2))+HitBoxRigth:
        if Mse_py > (altura/3)+HitBoxLeft and \
        Mse_py < ((altura/3)+start.get_height())+HitBoxRigth:
            return "start"
        if Mse_py > (altura/2)+HitBoxLeft and \
        Mse_py < ((altura/2)+options.get_height())+HitBoxRigth:
            return "options"
        if Mse_py > (altura/1.5)+HitBoxLeft and \
        Mse_py < ((altura/1.5)+credit.get_height())+HitBoxRigth:
            return "credit"

#Función que limpia el tablero
def ClearCells():
    for i in range(100):
        for j in range(100):
            nextCellState[i, j] = CellState[i, j] = 0

#Función del juego
def GameLife():
    global pause, screen
    run = True
    while run:
        # Se hace una copia del juego en cada iteración que guarda los cambios sin afectar a
        # las demás celdas
        CellState = np.copy(nextCellState)
        
        # Se limpia la pantalla en cada iteración para que no se sobrepongan los cambios
        # Se pone un retraso para que vaya más lento el programa y se aprecie mejor 
        screen.fill(bg)
        
        # Se registran los eventos que ocurran durante la ejecución
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Si se presiona una tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #Space = pausar el juego
                    pause = not pause
                elif event.key == pygame.K_c: #C = limpiar tablero
                    ClearCells()
                elif event.key == pygame.K_q: #Q = salir de la pantalla de juego
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                px, py = pygame.mouse.get_pos()
                #Revisamos que sea dentro del tablero del juego
                if px > difx and px < ((ncx+1)*tx)+difx and \
                py > dify and py < ((ncy+1)*ty)+dify:
                    cx, cy = int((np.floor((px-difx) / tx))), int((np.floor((py-dify) / ty)))
                    if nextCellState[cx, cy] == 1:
                        nextCellState[cx, cy] = 0
                    else:
                        nextCellState[cx, cy] = 1
            if event.type == pygame.VIDEORESIZE:
                AjusteTamano_Celdas(event.w, event.h)
                AjusteTamano_Surfaces(event.w, event.h)
        
        # Se establecen los bucles que recorrerán las matrices y diujarán las celdas
        # de izquierda a derecha 
        for y in range (ncy):
            for x in range (ncx):
                
                # Se ejecuta o no cada que se presiona una tecla. Al pausar, las celdas
                # quedan como están, sin cambios
                if not pause:
                     
                    # Se examina el estado de las celdas vecinas
                    AliveCells = CellState[(x - 1) % ncx, (y - 1) % ncy] + \
                                 CellState[(x    ) % ncx, (y - 1) % ncy] + \
                                 CellState[(x + 1) % ncx, (y - 1) % ncy] + \
                                 CellState[(x - 1) % ncx, (y    ) % ncy] + \
                                 CellState[(x + 1) % ncx, (y    ) % ncy] + \
                                 CellState[(x - 1) % ncx, (y + 1) % ncy] + \
                                 CellState[(x    ) % ncx, (y + 1) % ncy] + \
                                 CellState[(x + 1) % ncx, (y + 1) % ncy] 
        
                    # Se establecen las reglas del juego
                    if CellState[x, y] == 0 and AliveCells == 3:
                        nextCellState[x, y] = 1
                        
                    elif CellState[x, y] == 1 and (AliveCells < 2 or AliveCells > 3):
                        nextCellState[x, y] = 0
                
                # Se establecen las coordenadas de los cubos que formarán la rejilla
                cube = [(((x)*tx)+difx, ((y)*ty)+dify), (((x)*tx)+difx, ((y+1)*ty)+dify), 
                        ((x+1)*tx+difx, ((y+1)*ty)+dify), (((x+1)*tx)+difx, ((y)*ty)+dify)]
                
                # Dependiendo del estado de la celda, el cubo será blanco u oscuro            
                if nextCellState[x, y] == 1:
                    pygame.draw.polygon(screen, (255, 255, 255), cube, 0)
                    
                else:
                    pygame.draw.polygon(screen, (130, 130, 130), cube, 1)
        
        #Se limita la velocidad de refresco
        clock.tick(fps)
        # Se muestra en pantalla la cuadrícula
        pygame.display.update()
    #Se prepara pantalla para volver a dibujar el menu
    screen.fill(bg)

# Se inicia el bucle principal (Menu Principal)
while True:
    #Redibujo de superficies
    Dibujo_Surfaces()
    # Se registran los eventos que ocurran durante la ejecución
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            px, py = pygame.mouse.get_pos()
            #Guardamos la string que nos da "Colision_Surfaces"
            Place_Colis = Colision_Surfaces_Main(px, py)
            #Escogemos acciones según la string
            if Place_Colis == "start":
                screen.fill(bg)
                GameLife()
                #Terminando el juego se vuelve a poner el menu
                Dibujo_Surfaces()
            elif Place_Colis == "options":
                print("Options")
            elif Place_Colis == "credit":
                print("Credit")
        #Si se cambia de tamaño la pantalla
        if event.type == pygame.VIDEORESIZE:
            AjusteTamano_Celdas(event.w, event.h)
            AjusteTamano_Surfaces(event.w, event.h)
        
    
    #Se limita la velocidad de refresco
    clock.tick(fps)
    # Se muestra en pantalla la cuadrícula
    pygame.display.update()