import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, pi, sin
import variablesGovales as vg
import figuras as fg


def posicionMaus():
    """
    Obtiene la posición del mouse en coordenadas OpenGL.
    """
    x, y = pygame.mouse.get_pos()  # Obtiene la posición del mouse en píxeles
    # Convierte las coordenadas de píxeles a coordenadas OpenGL
    x = int(x)
    y = vg.Pantalla[1] - int(y) 
    
    x=(x*vg.ortogonal[1]) / vg.Pantalla[0] + vg.ortogonal[0]
    y=(y*vg.ortogonal[3]) / vg.Pantalla[1] + vg.ortogonal[2]
    
    
    
    return x, y  # Retorna las coordenadas en OpenGL

def posicionMausSpecial():
    """
    Obtiene la posición del mouse en coordenadas OpenGL.
    """
    x, y = pygame.mouse.get_pos()  # Obtiene la posición del mouse en píxeles
    # Convierte las coordenadas de píxeles a coordenadas OpenGL
    x = int(x)
    y = vg.Pantalla[1] - int(y) 
    
    x=(x*vg.ortogonal[1]) / vg.Pantalla[0] + vg.ortogonal[0]
    y=(y*vg.ortogonal[3]) / vg.Pantalla[1] + vg.ortogonal[2]
    
    
    if vg.modoDibujo == 2:  # Modo polar x
        y=vg.UltimasPosiciones[1]  # Mantiene la última posición y
    if vg.modoDibujo == 3:  # Modo polar y
        x=vg.UltimasPosiciones[0]  # Mantiene la última posición
    if vg.modoDibujo == 4:  # Modo angular
        dx = x - vg.UltimasPosiciones[0]
        dy = y - vg.UltimasPosiciones[1]
        modulo = (dx**2 + dy**2)**0.5
        angulo = vg.Angulo
        # Calcula la nueva posición manteniendo la distancia desde el punto inicial,
        # pero solo en la dirección del ángulo dado.
        x = vg.UltimasPosiciones[0] + modulo * cos((angulo * pi) / 180)
        y = vg.UltimasPosiciones[1] + modulo * sin((angulo * pi) / 180)
    
    return x, y  # Retorna las coordenadas en OpenGL

def mausEnPantalla():
    """
    Verifica si el mouse está dentro de los límites de la pantalla.
    
    :return: True si el mouse está dentro de la pantalla, False en caso contrario.
    """
    xMaus, yMaus = posicionMaus()
    if yMaus> vg.ortogonal[3] -vg.alturaBarraHeramientas:
        return False
    if yMaus< vg.ortogonal[2]:
        return False
    if xMaus < vg.ortogonal[0]:
        return False
    if xMaus > vg.ortogonal[1]:
        return False
    return True

# Función para dibujar un boton, con imaje y una funcion

def boton(x, y, ancho, alto, figura, funcion, color=vg.colorInterface):
    """
    Dibuja un botón en la pantalla y asigna una función al clic.
    
    :param x: Coordenada x del botón
    :param y: Coordenada y del botón
    :param ancho: Ancho del botón
    :param alto: Alto del botón
    :param figura: Imagen del botón en formato VECTOR
    :param funcion: Función a ejecutar al hacer clic en el botón
    """
    rectangulo=fg.rectangulo(((x,y),(x+ancho,y+alto)))
    figuraMovida=[]
    for punto in figura:
        xp,yp=punto
        xp=xp+x
        yp=yp+y
        figuraMovida.append((xp,yp))
        
    
    def detectorMaus():
        """
        Detecta si el mouse está dentro del área del botón y ejecuta la función asociada.
        """
        xMaus, yMaus = posicionMaus()
        if x <= xMaus and xMaus <= x + ancho and y <= yMaus and yMaus <= y + alto:
            funcion()
            
    vg.vectoresInterfaz.append((rectangulo,vg.grosorInterface,vg.colorInterface))
    vg.vectoresInterfaz.append((figuraMovida,vg.grosorInterface,color))
    vg.funcionesComprovacion.append(detectorMaus)
        
    return

def barraHeramientas():
    """
    Dibuja la barra de herramientas en la parte superior de la pantalla.
    """
    altura = vg.alturaBarraHeramientas  # Altura de la barra de herramientas
    # Dibuja un rectángulo para la barra de herramientas
    rectangulo = fg.rectangulo(((vg.ortogonal[0], vg.ortogonal[3]-altura), (vg.ortogonal[1], vg.ortogonal[3])))
    vg.vectoresInterfaz.append((rectangulo, vg.grosorInterface, vg.colorInterface))
    
   
    return


def dibujarFigura(figura):
    """
    Dibuja una figura en la pantalla.
    
    :param figura: puntos en verctor, el ancho y el color de la figura
    :return: None
    """
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    
    puntos, grosor, color = figura
    glColor3fv(color)  # Establece el color de la figura
    glLineWidth(grosor)  # Establece el grosor de la línea
    
    glBegin(GL_LINE_STRIP)  # Comienza a dibujar una línea abierta
    for punto in puntos:
        glVertex2f(punto[0], punto[1])  # Añade cada punto de la figura
    glEnd()  # Termina de dibujar la figura
    
    return