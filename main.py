import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import variablesGovales as vg
import figuras as fg
import interface as itf
import modos as md
import paint3d as paint3d

curvaVesier= fg.bezier(((10,10),(10,40),(40,40))) 

curva3d=fg.figuraAvierta(((10,40),(20,30),(10,25),(20,20),(10,10),(30,10),(30,40),(40,30),(40,20),(30,10)))

rectangulo= fg.rectangulo(((5,5),(20,20)))
recta=fg.linea(((10,10),(40,40)))
rectaDePincel=fg.linea(((750,550),(775,550)))

TrinanguloAriva=fg.figuraContinua(((5, 5), (12.5, 20), (20, 5)))
trianguloAbajo=fg.figuraContinua(((5, 20), (12.5, 5), (20, 20)))
lineaVertical=fg.linea(((12.5, 5),(12.5, 20)))
lineaHorizontal=fg.linea(((5, 12.5),(20, 12.5)))
Angulo=fg.figuraAvierta(((20, 5),(5, 5),(12.5, 20)))
puntoSimple=fg.rectangulo(((12, 12),(13, 13)))
rectanguloBoton=fg.rectangulo(((10,10),(40,40)))

circulo=fg.Circulo(((25,25),(40,25)))

lineaRecortada=fg.figuraAvierta(((10,10),(40,10),(40,40),(10,40),(10,10),(30,30)))

recorteAfueraRectangulo=fg.figuraAvierta(((10,10),(20,20),(30,20),(30,30),(20,30),(20,20),(30,20),(30,30),(40,40)))

unaM=fg.figuraAvierta(((5,5),(5,20),(12.5,10),(20,20),(20,5)))
cruz=fg.figuraAvierta(((5,12.5),(20,12.5),(12.5,12.5),(12.5,20),(12.5,5)))
unaR=fg.figuraAvierta(((5,5),(5,20),(12.5,18),(5,12.5),(12.5,5)))
unaE=fg.figuraAvierta(((12.5,20),(5,20),(5,12.5),(12.5,12.5),(5,12.5),(5,5),(12.5,5)))

def main2(event):
    """
    Función principal que se ejecuta en el bucle principal del programa.
    Aquí se pueden agregar más funcionalidades o lógica de la aplicación.
    """
    
    pass
mausPoint=False

vg.main2 = main2  # Asignar la función principal a la variable global

def main():
    pygame.init()
    pygame.display.set_mode((vg.Pantalla[0], vg.Pantalla[1]), DOUBLEBUF | OPENGL)
    gluOrtho2D(vg.ortogonal[0], vg.ortogonal[1], vg.ortogonal[2], vg.ortogonal[3])

    itf.boton(30,520, 50, 50, curvaVesier, md.modoBesier)
    itf.boton(90,520, 50, 50, recta, md.modoRecta)
    itf.boton(150,520, 50, 50, circulo, md.modoCirculo)
    itf.boton(210,520, 50, 50, rectanguloBoton, md.modoRectangulo)
    itf.boton(270,520, 50, 50, lineaRecortada, md.modoTrimRectangulo)
    itf.boton(330,520, 50, 50, recorteAfueraRectangulo, md.modoTrimRectanguloAfuera)
    itf.boton(390,520, 50, 50,curva3d,paint3d.main)
    
    itf.boton(450,520, 25, 25, unaR, md.modoRotarFigura)
    itf.boton(450,550, 25, 25, unaE, md.modorEscalarFigura)
    itf.boton(480,520, 25, 25, unaM, md.modoMoverFigura)
    itf.boton(480,550, 25, 25, cruz, md.modoSelecionarFigura)
    itf.boton(540,520, 25, 25, puntoSimple, md.modoDibujoNormal)
    itf.boton(540,550, 25, 25, lineaVertical, md.modoDibujoPolarY)
    itf.boton(570,550, 25, 25, lineaHorizontal, md.modoDibujoPolarX)
    itf.boton(570,520, 25, 25, Angulo, md.modoDibujoAngular)
    
    itf.boton(600,550, 25, 25, rectangulo, md.colorAzul, (0, 0, 1))
    itf.boton(600,520, 25, 25, rectangulo, md.colorRojo, (1, 0, 0))
    itf.boton(630,550, 25, 25, rectangulo, md.colorVerde, (0, 1, 0))
    itf.boton(630,520, 25, 25, rectangulo, md.colorAmarillo, (1, 1, 0))
    itf.boton(660,550, 25, 25, rectangulo, md.colorCian, (0, 1, 1))
    itf.boton(660,520, 25, 25, rectangulo, md.colorMagenta, (1, 0, 1))
    itf.boton(700,550, 25, 25, TrinanguloAriva, md.aumentarGrosor )
    itf.boton(700,520, 25, 25, trianguloAbajo, md.disminuirGrosor)
    itf.barraHeramientas()

    while True:
        
        for event in pygame.event.get():
            vg.main2(event)  # Llama a la función principal para manejar eventos
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == MOUSEBUTTONUP:
                vg.UltimasPosiciones = itf.posicionMausSpecial() if (itf.mausEnPantalla() and vg.modoDibujo != 4) else vg.UltimasPosiciones
                if event.button == 1:
                    for funcion in vg.funcionesComprovacion:
                         funcion()
            
            
            
        
        
        
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        for figura in vg.vectoresInterfaz:
            itf.dibujarFigura(figura)
       
        
        for figura in vg.vectoresCompletos:
            itf.dibujarFigura(figura)
            
        if vg.figuraSelecionada is not None:
            itf.dibujarFigura((vg.figuraSelecionada[0], vg.grosorPincel+1, (1, 0, 0)))
         
        itf.dibujarFigura((vg.figurasPendientes, vg.grosorPincel, vg.colorPincel))
        itf.dibujarFigura((rectaDePincel, vg.grosorPincel, vg.colorPincel))
        for punto in vg.vectoresPendientes:
            glPointSize(vg.grosorPincel)
            glBegin(GL_POINTS)
            glColor3fv(vg.colorPincel)
            glVertex2fv(punto)
            glEnd()
        
        
        pygame.display.flip()
        pygame.time.wait(10)
        
if __name__ == "__main__":
    main()