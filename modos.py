import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

import variablesGovales as vg
import figuras as fg
import interface as itf

def cambiarMain2(funcion):
    """
    Cambia la función principal que se ejecuta en el bucle principal del programa.
    
    :param funcion: La nueva función a asignar como main2.
    """
    vg.main2 = funcion  # Asigna la nueva función a la variable global main2

def modoBesier():
    global main2
    global mausPoint
    mausPoint=False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event ):
            global mausPoint
            
            if event.type == MOUSEBUTTONDOWN and itf.mausEnPantalla() and event.button == 3:
                if len(vg.vectoresPendientes) >3:
                    curva = fg.bezier(vg.vectoresPendientes)
                    vg.vectoresCompletos.append((curva, vg.grosorPincel, vg.colorPincel))
                    vg.vectoresPendientes = []
                    vg.figurasPendientes = []
            if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
                vg.vectoresPendientes.pop() if mausPoint else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = False
                    
        
            elif itf.mausEnPantalla() :
                    vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                    vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                    mausPoint = True
                    if len(vg.vectoresPendientes) > 2:
                        vg.figurasPendientes = fg.bezier(vg.vectoresPendientes)
    
    cambiarMain2(f)  # Cambia la función principal a la nueva función de modo Bézier
            
def modoRecta():
    global main2
    global mausPoint
    mausPoint=False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = False
            if len(vg.vectoresPendientes) == 2:
                linea = fg.linea(vg.vectoresPendientes)
                vg.vectoresCompletos.append((linea, vg.grosorPincel, vg.colorPincel))
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
                
        elif itf.mausEnPantalla():
            if len(vg.vectoresPendientes) < 3:
                vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = True
                if len(vg.vectoresPendientes) > 1:
                    vg.figurasPendientes = fg.linea(vg.vectoresPendientes)
    
    cambiarMain2(f)
        

def modoCirculo():
    global main2
    global mausPoint
    mausPoint=False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = False
            if len(vg.vectoresPendientes) == 2:
                circulo = fg.Circulo(vg.vectoresPendientes)
                vg.vectoresCompletos.append((circulo, vg.grosorPincel, vg.colorPincel))
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
                
        elif itf.mausEnPantalla():
            if len(vg.vectoresPendientes) < 3:
                vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = True
                if len(vg.vectoresPendientes) > 1:
                    vg.figurasPendientes = fg.Circulo(vg.vectoresPendientes)
    
    cambiarMain2(f)
    
def colorAzul():
    vg.colorPincel = (0, 0, 1)  # Cambia el color del pincel a azul
    
def colorRojo():
    vg.colorPincel = (1, 0, 0)  # Cambia el color del pincel a rojo
def colorVerde():
        vg.colorPincel = (0, 1, 0)  # Cambia el color del pincel a verde
def colorAmarillo():
        vg.colorPincel = (1, 1, 0)  # Cambia el color del pincel a amarillo

def colorCian():
        vg.colorPincel = (0, 1, 1)  # Cambia el color del pincel a cian

def colorMagenta():
        vg.colorPincel = (1, 0, 1)  # Cambia el color del pincel a magenta

    
def aumentarGrosor():
    vg.grosorPincel += 1  # Aumenta el grosor del pincel en 1
def disminuirGrosor():
    if vg.grosorPincel > 1:
        vg.grosorPincel -= 1  # Disminuye el grosor del pincel en 1, si es mayor que 1
    else:
        vg.grosorPincel = 1
        
def modoDibujoNormal():
    vg.modoDibujo = 1  # Establece el modo de dibujo a normal
def modoDibujoPolarX():
    vg.modoDibujo = 2  # Establece el modo de dibujo a polar X
def modoDibujoPolarY():
    vg.modoDibujo = 3  # Establece el modo de dibujo a polar Y
def modoDibujoAngular():
    vg.modoDibujo = 4  # Establece el modo de dibujo a angular
    vg.Angulo = int(input("Ingrese el ángulo en grados: "))  # Solicita al usuario el ángulo para el modo angular
    
    
    
    
def modoTrimRectangulo():
    global main2
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = False
            if len(vg.vectoresPendientes) == 2:
                fg.trimRectangulos(vg.vectoresPendientes)
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
                
        elif itf.mausEnPantalla():
            if len(vg.vectoresPendientes) < 3:
                vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = True
                if len(vg.vectoresPendientes) > 1:
                    vg.figurasPendientes = fg.rectangulo(vg.vectoresPendientes)
    
    cambiarMain2(f)
    
    
def modoTrimRectanguloAfuera():
    global main2
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = False
            if len(vg.vectoresPendientes) == 2:
                fg.trimRectangulosAfuera(vg.vectoresPendientes)
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
                
        elif itf.mausEnPantalla():
            if len(vg.vectoresPendientes) < 3:
                vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = True
                if len(vg.vectoresPendientes) > 1:
                    vg.figurasPendientes = fg.rectangulo(vg.vectoresPendientes)
    
    cambiarMain2(f)
    
    
def modoRectangulo():
    global main2
    global mausPoint
    mausPoint=False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = False
            if len(vg.vectoresPendientes) == 2:
                circulo = fg.rectangulo(vg.vectoresPendientes)
                vg.vectoresCompletos.append((circulo, vg.grosorPincel, vg.colorPincel))
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
                
        elif itf.mausEnPantalla():
            if len(vg.vectoresPendientes) < 3:
                vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
                vg.vectoresPendientes.append((itf.posicionMausSpecial()))
                mausPoint = True
                if len(vg.vectoresPendientes) > 1:
                    vg.figurasPendientes = fg.rectangulo(vg.vectoresPendientes)
    
    cambiarMain2(f)
    
    
def modoSelecionarFigura():
    global main2
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def puntoEnFigura(figura, punto):
        """
        Verifica si un punto está dentro de una figura.
        
        :param figura: Lista de puntos que definen la figura.
        :param punto: Tupla (x, y) que representa el punto a verificar.
        :return: True si el punto está dentro de la figura, False en caso contrario.
        """
        def DistanciaRecta(punto, recta):
            """
            Calcula la distancia entre un punto y una recta definida por dos puntos.
            
            :param punto: Tupla (x, y) que representa el punto.
            :param recta: Tupla de dos puntos que definen la recta.
            :return: Distancia entre el punto y la recta.
            """
            x1, y1 = recta[0]
            x2, y2 = recta[1]
            num = abs((y2 - y1) * punto[0] - (x2 - x1) * punto[1] + x2 * y1 - y2 * x1)
            den = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
            return num / den if den != 0 else float('inf')
        
        n = len(figura)
        if n == 1:
            # Si la figura es un solo punto, verifica distancia al punto
            px, py = figura[0]
            if ((punto[0] - px) ** 2 + (punto[1] - py) ** 2) ** 0.5 < vg.grosorPincel:
                return True
            return False
        for i in range(n-1):
            punto1 = figura[i]
            punto2 = figura[i + 1]  # Cierra la figura
            if DistanciaRecta(punto, (punto1, punto2)) < vg.grosorPincel:
                return True
        return False  # Si no se encuentra el punto en ninguna recta de la figura, retorna False
            
    
    def f(event):
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            xMaus, yMaus = itf.posicionMausSpecial()
            for i, figura in enumerate(vg.vectoresCompletos):
                if puntoEnFigura(figura[0], (xMaus, yMaus)):
                    vg.figuraSelecionada = figura
                    vg.figuraSelecionadaIndex = i
              # Si no se selecciona ninguna figura
        elif itf.mausEnPantalla():
            xMaus, yMaus = itf.posicionMausSpecial()
            vg.vectoresPendientes = [(xMaus, yMaus)]
            
    
    cambiarMain2(f)
    
    
def modoMoverFigura():
    global main2
    mausPoint=False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []
    
    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append(itf.posicionMausSpecial())
            mausPoint = False
            if (vg.figuraSelecionada is not None) and len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                figuraMovida = fg.moverFigura(figura, vg.vectoresPendientes[0], vg.vectoresPendientes[1])
                vg.vectoresCompletos.pop(vg.figuraSelecionadaIndex)
                vg.vectoresCompletos.append((figuraMovida, vg.figuraSelecionada[1], vg.figuraSelecionada[2]))
                vg.figuraSelecionada = None
                vg.figuraSelecionadaIndex = -1
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
        elif itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint )else None
            vg.vectoresPendientes.append((itf.posicionMausSpecial()))
            mausPoint = True
            if len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                figuraMovida = fg.moverFigura(figura, vg.vectoresPendientes[0], vg.vectoresPendientes[1])
                vg.figurasPendientes = figuraMovida
                
    
    cambiarMain2(f)
    
def modoRotarFigura():
    global main2
    mausPoint = False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []

    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append(itf.posicionMausSpecial())
            mausPoint = False
            if (vg.figuraSelecionada is not None) and len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                centro = vg.vectoresPendientes[0]
                punto = vg.vectoresPendientes[1]
                dx = punto[0] - centro[0]
                dy = punto[1] - centro[1]
                angulo = math.degrees(math.atan2(dy, dx))
                figuraRotada = fg.rotarFigura(figura, centro, angulo)
                vg.vectoresCompletos.pop(vg.figuraSelecionadaIndex)
                vg.vectoresCompletos.append((figuraRotada, vg.figuraSelecionada[1], vg.figuraSelecionada[2]))
                vg.figuraSelecionada = None
                vg.figuraSelecionadaIndex = -1
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
        elif itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint) else None
            vg.vectoresPendientes.append(itf.posicionMausSpecial())
            mausPoint = True
            if (vg.figuraSelecionada is not None) and len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                centro = vg.vectoresPendientes[0]
                punto = vg.vectoresPendientes[1]
                dx = punto[0] - centro[0]
                dy = punto[1] - centro[1]
                angulo = math.degrees(math.atan2(dy, dx))
                vg.figurasPendientes = fg.rotarFigura(figura, centro, angulo)

    cambiarMain2(f)
    
def modorEscalarFigura():
    global main2
    mausPoint = False
    vg.vectoresPendientes = []
    vg.figurasPendientes = []

    def f(event):
        global mausPoint
        if event.type == MOUSEBUTTONUP and itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if mausPoint else None
            vg.vectoresPendientes.append(itf.posicionMausSpecial())
            mausPoint = False
            if (vg.figuraSelecionada is not None) and len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                centro = vg.vectoresPendientes[0]
                punto = vg.vectoresPendientes[1]
                dx = punto[0] - centro[0]
                dy = punto[1] - centro[1]
                escala = (dx**2+dy**2)**0.1
                figuraEscalada=fg.escalarFigura(figura,centro,escala)
                vg.vectoresCompletos.pop(vg.figuraSelecionadaIndex)
                vg.vectoresCompletos.append((figuraEscalada, vg.figuraSelecionada[1], vg.figuraSelecionada[2]))
                vg.figuraSelecionada = None
                vg.figuraSelecionadaIndex = -1
                vg.vectoresPendientes = []
                vg.figurasPendientes = []
        elif itf.mausEnPantalla():
            vg.vectoresPendientes.pop() if (len(vg.vectoresPendientes) > 0 and mausPoint) else None
            vg.vectoresPendientes.append(itf.posicionMausSpecial())
            mausPoint = True
            if (vg.figuraSelecionada is not None) and len(vg.vectoresPendientes) == 2:
                figura = vg.figuraSelecionada[0]
                centro = vg.vectoresPendientes[0]
                punto = vg.vectoresPendientes[1]
                dx = punto[0] - centro[0]
                dy = punto[1] - centro[1]
                escala = (dx**2+dy**2)**0.1
                
                vg.figurasPendientes = fg.escalarFigura(figura,centro,escala)

    cambiarMain2(f)

def dibujarCorazon():
    """
    Dibuja un corazón usando círculos intercalados, recorte horizontal y líneas diagonales.
    """
    # Obtener el centro de la pantalla
    centro_x = vg.ortogonal[1] / 2
    centro_y = vg.ortogonal[3] / 2 - vg.alturaBarraHeramientas / 2
    
    # Radio de los círculos
    radio = 50
    
    # Crear dos círculos intercalados (tocándose en el centro)
    # Círculo izquierdo
    centro_izq = (centro_x - radio/2, centro_y)
    punto_radio_izq = (centro_x - radio/2 + radio, centro_y)
    circulo_izq = fg.Circulo((centro_izq, punto_radio_izq))
    
    # Círculo derecho
    centro_der = (centro_x + radio/2, centro_y)
    punto_radio_der = (centro_x + radio/2 + radio, centro_y)
    circulo_der = fg.Circulo((centro_der, punto_radio_der))
    
    # Agregar los círculos
    vg.vectoresCompletos.append((circulo_izq, vg.grosorPincel, vg.colorPincel))
    vg.vectoresCompletos.append((circulo_der, vg.grosorPincel, vg.colorPincel))
    
    # Crear rectángulo para recorte horizontal (cortar la parte superior)
    punto1_recorte = (centro_x - radio * 1.5, centro_y)
    punto2_recorte = (centro_x + radio * 1.5, centro_y + radio * 1.5)
    
    # Aplicar recorte
    fg.trimRectangulos((punto1_recorte, punto2_recorte))
    
    # Crear las líneas diagonales hacia el punto central inferior
    punto_inferior = (centro_x, centro_y - radio * 1.2)
    
    # Línea desde esquina izquierda
    esquina_izq = (centro_x - radio, centro_y)
    linea_izq = fg.linea((esquina_izq, punto_inferior))
    
    # Línea desde esquina derecha  
    esquina_der = (centro_x + radio, centro_y)
    linea_der = fg.linea((esquina_der, punto_inferior))
    
    # Agregar las líneas
    vg.vectoresCompletos.append((linea_izq, vg.grosorPincel, vg.colorPincel))
    vg.vectoresCompletos.append((linea_der, vg.grosorPincel, vg.colorPincel))