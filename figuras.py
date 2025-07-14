import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, pi, sin
import variablesGovales as vg


def rectangulo(Puntos):
    """
    Genera una función que devuelve las coordenadas de un cuadrado como vector.
    """
    resultado = []
    # Asegurarse de que hay al menos 2 puntos
    if len(Puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir un rectángulo.")
    # Obtener las coordenadas  puntos
    x1, y1 = Puntos[0]
    x2, y2 = Puntos[1]
    resultado.append((x1, y1))  # Esquina inferior izquierda
    resultado.append((x2, y1))  # Esquina inferior derecha
    resultado.append((x2, y2))  # Esquina superior derecha
    resultado.append((x1, y2))  # Esquina superior izquierda
    resultado.append((x1, y1))  # Volver al punto inicial para cerrar el rectángulo
    
    return resultado



# Función que devuelve otra función para calcular puntos de una curva de Bézier
def bezier(puntos):
    # Función para calcular el factorial de un número
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    # Función para calcular el coeficiente binomial (n sobre k)
    def binomial(n, k):
        return factorial(n) / (factorial(k) * factorial(n - k))
    
    # Función interna que evalúa la curva de Bézier en el parámetro t
    def fT(t):
        result = [0, 0]
        for i in range(len(puntos)):
            binom = binomial(len(puntos) - 1, i)
            coef = ((1 - t) ** (len(puntos) - 1 - i)) * (t ** i)
            result[0] += binom * coef * puntos[i][0]
            result[1] += binom * coef * puntos[i][1]
        return result

    curva_puntos = []
    for i in range(vg.resocuionCurva + 1):
        t = i / vg.resocuionCurva
        curva_puntos.append(fT(t))  # Calcula los puntos de la curva

    return curva_puntos  # Devuelve la lista de puntos de la curva de Bézier


    
def linea(puntos):
    """
    Genera una función que devuelve las coordenadas de una línea como vector.
    """
    resultado = []
    # Asegurarse de que hay al menos 2 puntos
    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir una línea.")
    
    # Obtener las coordenadas de los puntos
    x1, y1 = puntos[0]
    x2, y2 = puntos[1]
    
    resultado.append((x1, y1))  # Punto inicial
    resultado.append((x2, y2))  # Punto final
    
    return resultado


def figuraContinua(puntos):
    """
    Genera una función que devuelve las coordenadas de una figura continua como vector.
    """
    resultado = []
    # Asegurarse de que hay al menos 2 puntos
    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir una figura continua.")
    
    # Agregar los puntos a la lista de resultados
    for punto in puntos:
        resultado.append(punto)
    # Cerrar la figura volviendo al primer punto
    resultado.append(puntos[0])
    
    return resultado  # Devuelve la lista de puntos de la figura continua

def figuraAvierta(puntos):
    """
    Genera una función que devuelve las coordenadas de una figura abierta como vector.
    """
    resultado = []
    # Asegurarse de que hay al menos 2 puntos
    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir una figura abierta.")
    
    # Agregar los puntos a la lista de resultados
    for punto in puntos:
        resultado.append(punto)
    
    return resultado  # Devuelve la lista de puntos de la figura abierta



def Circulo(puntos):
    centro = puntos[0]  # El primer punto es el centro del círculo
    # El radio se calcula como la distancia entre el centro y el segundo punto
    radio = ((puntos[0][0] - puntos[1][0]) ** 2 + (puntos[0][1] - puntos[1][1]) ** 2) ** 0.5

    # Retorna una función que genera coordenadas (x, y) del círculo según un parámetro t ∈ [0,1]
    def fT(t):
        x = centro[0] + radio * cos(2 * pi * t)
        y = centro[1] + radio * sin(2 * pi * t)
        return (x, y)
    
    puntos = []
    for i in range(vg.resocuionCurva + 1):  # Calcula puntos uniformemente en el círculo
        t = i / vg.resocuionCurva
        puntos.append(fT(t))
        
    return puntos  # Devuelve la lista de puntos del círculo






# Constantes para los códigos de región usados en el algoritmo de Cohen–Sutherland
INSIDE, IZQUIERDA, DERECHA, ABAJO, ARRIBA = 0, 1, 2, 4, 8

# Calcula el código de región de un punto según su posición relativa a la ventana de recorte
def calcular_codigo(x, y, xmin, xmax, ymin, ymax):
    codigo = INSIDE  # Por defecto, el punto está dentro
    if x < xmin:
        codigo |= IZQUIERDA
    elif x > xmax:
        codigo |= DERECHA
    if y < ymin:
        codigo |= ABAJO
    elif y > ymax:
        codigo |= ARRIBA
    return codigo

# Algoritmo de recorte de líneas de Cohen–Sutherland
def cohen_sutherland(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    codigo1 = calcular_codigo(x1, y1, xmin, xmax, ymin, ymax)
    codigo2 = calcular_codigo(x2, y2, xmin, xmax, ymin, ymax)
    aceptar = False  # Bandera para indicar si se acepta la línea

    while True:
        # Ambos puntos dentro: aceptar línea
        if codigo1 == 0 and codigo2 == 0:
            aceptar = True
            break
        # Ambos puntos fuera en la misma región: rechazar línea
        elif (codigo1 & codigo2) != 0:
            break
        else:
            # Al menos un punto está fuera: calcular intersección
            x, y = 0, 0
            fuera = codigo1 if codigo1 != 0 else codigo2

            # Determina el punto de intersección con el borde adecuado
            if fuera & ARRIBA:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif fuera & ABAJO:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif fuera & DERECHA:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif fuera & IZQUIERDA:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Sustituye el punto fuera por el punto de intersección y recalcula su código
            if fuera == codigo1:
                x1, y1 = x, y
                codigo1 = calcular_codigo(x1, y1, xmin, xmax, ymin, ymax)
            else:
                x2, y2 = x, y
                codigo2 = calcular_codigo(x2, y2, xmin, xmax, ymin, ymax)

    # Devuelve la línea recortada o None si no es visible
    if aceptar:
        return (x1, y1, x2, y2)
    else:
        return None





def trimRectangulos(puntos):
    """
    Recorta un rectángulo a partir de dos puntos.
    """
    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir un rectángulo.")
    
    x1, y1 = puntos[0]
    x2, y2 = puntos[1]
    
    # Algoritmo de recorte de líneas de Cohen–Sutherland a vectoresCompletos
    
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)
    
    
    nuevos_vectores = []
    for item in vg.vectoresCompletos:
        lineas = item[0]
        recortada = []
        for j in range(len(lineas) - 1):
            x1, y1 = lineas[j]
            x2, y2 = lineas[j + 1]
            recorte = cohen_sutherland(x1, y1, x2, y2, xmin, xmax, ymin, ymax)
            if recorte:
                # Mantener cada segmento recortado como una línea abierta
                recortada.append([(recorte[0], recorte[1]), (recorte[2], recorte[3])])
        if recortada:
            # Agregar cada segmento recortado como un nuevo vector completo, manteniendo la figura abierta
            for segmento in recortada:
                nuevos_vectores.append((segmento, item[1], item[2]))
    vg.vectoresCompletos = nuevos_vectores
    
    
                
                

def cohen_sutherland_inverso(x1, y1, x2, y2, xmin, xmax, ymin, ymax):
    codigo1 = calcular_codigo(x1, y1, xmin, xmax, ymin, ymax)
    codigo2 = calcular_codigo(x2, y2, xmin, xmax, ymin, ymax)

    segmentos_fuera = []

    # Si ambos puntos están dentro, no se conserva nada
    if codigo1 == 0 and codigo2 == 0:
        return []

    # Si ambos están fuera en la misma región, conservar segmento completo
    if (codigo1 & codigo2) != 0:
        return [(x1, y1, x2, y2)]

    # Se necesitan intersecciones
    puntoA = (x1, y1)
    puntoB = (x2, y2)

    # Se copia para no modificar los originales directamente
    xa, ya = x1, y1
    xb, yb = x2, y2
    ca = codigo1
    cb = codigo2

    # Lista para guardar intersecciones
    intersecciones = []

    for _ in range(2):  # Procesar ambos extremos
        if ca == 0:
            # Cambiar extremos si el primero está dentro
            xa, ya, xb, yb = xb, yb, xa, ya
            ca, cb = cb, ca

        if ca != 0:
            x, y = 0, 0
            if ca & ARRIBA:
                x = xa + (xb - xa) * (ymax - ya) / (yb - ya)
                y = ymax
            elif ca & ABAJO:
                x = xa + (xb - xa) * (ymin - ya) / (yb - ya)
                y = ymin
            elif ca & DERECHA:
                y = ya + (yb - ya) * (xmax - xa) / (xb - xa)
                x = xmax
            elif ca & IZQUIERDA:
                y = ya + (yb - ya) * (xmin - xa) / (xb - xa)
                x = xmin

            intersecciones.append((x, y))

            # Cambiar extremos para la siguiente intersección
            xa, ya = x, y
            ca = calcular_codigo(xa, ya, xmin, xmax, ymin, ymax)

    # Si se encontraron dos intersecciones, hay dos segmentos externos
    if len(intersecciones) == 2:
        seg1 = (x1, y1, intersecciones[0][0], intersecciones[0][1])
        seg2 = (intersecciones[1][0], intersecciones[1][1], x2, y2)
        segmentos_fuera.append(seg1)
        segmentos_fuera.append(seg2)
    elif len(intersecciones) == 1:
        # Solo un extremo fuera, una sola parte externa
        if codigo1 != 0:
            segmentos_fuera.append((x1, y1, intersecciones[0][0], intersecciones[0][1]))
        else:
            segmentos_fuera.append((intersecciones[0][0], intersecciones[0][1], x2, y2))

    return segmentos_fuera


def trimRectangulosAfuera(puntos):
    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos dos puntos para definir un rectángulo.")
    
    x1, y1 = puntos[0]
    x2, y2 = puntos[1]
    
    # Algoritmo de recorte de líneas de Cohen–Sutherland a vectoresCompletos
    
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)
    
    nuevos_vectores = []
    for item in vg.vectoresCompletos:
        lineas = item[0]
        recortada = []
        for j in range(len(lineas) - 1):
            x1, y1 = lineas[j]
            x2, y2 = lineas[j + 1]
            recorte = cohen_sutherland_inverso(x1, y1, x2, y2, xmin, xmax, ymin, ymax)
            if recorte:
                # Mantener cada segmento recortado como una línea abierta
                recortada.extend(recorte)
        if recortada:
            # Agregar cada segmento recortado como un nuevo vector completo, manteniendo la figura abierta
            for segmento in recortada:
                nuevos_vectores.append(([(segmento[0], segmento[1]), (segmento[2], segmento[3])], item[1], item[2]))
    vg.vectoresCompletos = nuevos_vectores
    
    
    
    
def moverFigura(figura, puntoinicial, punto_final):
    """
    Mueve una figura a una nueva posición según un desplazamiento dado.
    
    :param figura: La figura a mover, representada como una lista de puntos.
    :param puntoinicial: El punto inicial de referencia para el movimiento.
    :param punto_final: El punto final de referencia para el movimiento.
    :return: Una nueva figura con los puntos desplazados.
    """
    desplazamiento_x = punto_final[0] - puntoinicial[0]
    desplazamiento_y = punto_final[1] - puntoinicial[1]
    
    figura_movil = []
    for punto in figura:
        nuevo_punto = (punto[0] + desplazamiento_x, punto[1] + desplazamiento_y)
        figura_movil.append(nuevo_punto)
    
    return figura_movil  # Devuelve la figura movida

def rotarFigura(figura,centro,angulo):
    angulo=pi*angulo/180
    figura_rotada = []
    cx, cy = centro
    for x, y in figura:
        # Trasladar al origen
        x0 = x - cx
        y0 = y - cy
        # Rotar
        xr = x0 * cos(angulo) - y0 * sin(angulo)
        yr = x0 * sin(angulo) + y0 * cos(angulo)
        # Trasladar de vuelta
        figura_rotada.append((xr + cx, yr + cy))
    return figura_rotada


def escalarFigura(figura,centro,escala):
    figura_escalada = []
    cx, cy = centro
    for x, y in figura:
        # Trasladar al origen
        x0 = x - cx
        y0 = y - cy
        # Escalar
        xs = x0 * escala
        ys = y0 * escala
        # Trasladar de vuelta
        figura_escalada.append((xs + cx, ys + cy))
    return figura_escalada
    
    
    
    