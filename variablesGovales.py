
Pantalla=[800,600]
ortogonal = [0,800,0,600]  # Proyección ortogonal 2D

vectoresCompletos = []
vectoresPendientes = []

vectoresInterfaz = []  # Vectores de la interfaz

figurasPendientes = []
funcionesComprovacion = []

resocuionCurva = 100  # Resolución de la curvas

colorInterface = (0.5, 0.5, 0.5)  # Color de la interfaz
grosorInterface = 3  # Grosor de la interfaz
alturaBarraHeramientas= 130

colorPincel = (1, 1, 1)  # Color del pincel
grosorPincel = 5  # Grosor del pincel


modoDibujo=1 # Modo de dibujo: 1 para normal, 2 para polar x, 3 polar y y 4 para angular
UltimasPosiciones = [ortogonal[1]/2, ortogonal[3]/2]  # Última posición del mouse
Angulo = 0  # Ángulo para el modo angular

figuraSelecionadaIndex = -1  # Índice de la figura seleccionada en la interfaz

figuraSelecionada = None  # Figura seleccionada en la interfaz


main2 = None  # Variable para almacenar la función principal del modo de dibujo