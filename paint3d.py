import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import math

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    import numpy as np
except ImportError:
    print("Error: Se requieren las librerías OpenGL y numpy")
    print("Instala con: pip install PyOpenGL PyOpenGL_accelerate numpy")
    sys.exit(1)

class Shape3D:
    def __init__(self, shape_type, position, color, wireframe=False):
        self.shape_type = shape_type
        self.position = position
        self.color = color
        self.wireframe = wireframe
        self.rotation = [0, 0, 0]
        self.scale = 1.0

class OpenGLRenderer:
    def __init__(self):
        self.shapes = []
        self.current_shape = "Cube"
        self.current_color = [1.0, 0.0, 0.0, 1.0]  # Rojo por defecto
        self.wireframe_mode = False
        self.show_shadows = True
        self.rotation_x = 0
        self.rotation_y = 0
        self.mouse_old_x = 0
        self.mouse_old_y = 0
        self.mouse_pressed = False
        self.perspective_mode = True
        
        
        self.need_resize = False
        self.new_width = 800
        self.new_height = 600

        
        # Configuración de iluminación
        self.light_position = [2.0, 2.0, 2.0, 1.0]
        
    def init_opengl(self):
        """Inicializa OpenGL"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        
        # Configuración de luz
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
        # Habilitar blending para las sombras
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Color de fondo
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        # Configuración del material
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)
        
    def resize_viewport(self, width, height):
        """Ajusta el viewport"""
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        if self.perspective_mode:
            gluPerspective(45.0, width/height, 0.1, 100.0)
        else:
            size = 5.0
            if width <= height:
                glOrtho(-size, size, -size*height/width, size*height/width, -10.0, 10.0)
            else:
                glOrtho(-size*width/height, size*width/height, -size, size, -10.0, 10.0)
        
        glMatrixMode(GL_MODELVIEW)
        
    def compute_shadow_matrix(self, plane, light_pos):
            """Calcula la matriz de proyección de sombra sobre un plano dado"""
            a, b, c, d = plane
            x, y, z, w = light_pos

            dot = a * x + b * y + c * z + d * w

            shadow = np.array([
                [dot - a * x, -a * y,     -a * z,     -a * w],
                [-b * x,     dot - b * y, -b * z,     -b * w],
                [-c * x,     -c * y,     dot - c * z, -c * w],
                [-d * x,     -d * y,     -d * z,     dot - d * w]
            ], dtype=np.float32)

            return shadow.flatten()
        
    def draw_shadow(self, shape):
        """Dibuja la sombra proyectada en el suelo Y = -2"""
        
        

        if not self.show_shadows:
            return

        glPushMatrix()
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.4)

        ground_plane = [0.0, 1.0, 0.0, 2.0]  # Plano Y = -2 → Ax + By + Cz + D = 0 → 0x + 1y + 0z + 2 = 0
        light_pos = self.light_position

        # Calcular la matriz de sombra
        shadow_matrix = self.compute_shadow_matrix(ground_plane, light_pos)
        glMultMatrixf(shadow_matrix)

        # Aplicar transformaciones del objeto
        glTranslatef(*shape.position)
        glRotatef(shape.rotation[0], 1, 0, 0)
        glRotatef(shape.rotation[1], 0, 1, 0)
        glRotatef(shape.rotation[2], 0, 0, 1)
        glScalef(shape.scale, shape.scale, shape.scale)

        self.draw_shape_geometry(shape.shape_type, True)

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        
    def draw_shape_geometry(self, shape_type, is_shadow=False):
        """Dibuja la geometría de una forma específica"""
        if shape_type == "Cube":
            if is_shadow:
                glutSolidCube(1.0)
            else:
                if self.wireframe_mode:
                    glutWireCube(1.0)
                else:
                    glutSolidCube(1.0)
                    
        elif shape_type == "Sphere":
            if is_shadow:
                glutSolidSphere(0.5, 20, 20)
            else:
                if self.wireframe_mode:
                    glutWireSphere(0.5, 20, 20)
                else:
                    glutSolidSphere(0.5, 20, 20)
                    
        elif shape_type == "Cone":
            if is_shadow:
                glutSolidCone(0.5, 1.0, 20, 20)
            else:
                if self.wireframe_mode:
                    glutWireCone(0.5, 1.0, 20, 20)
                else:
                    glutSolidCone(0.5, 1.0, 20, 20)
                    
        elif shape_type == "Teapot":
            if is_shadow:
                glutSolidTeapot(0.5)
            else:
                if self.wireframe_mode:
                    glutWireTeapot(0.5)
                else:
                    glutSolidTeapot(0.5)
                    
        elif shape_type == "Torus":
            if is_shadow:
                glutSolidTorus(0.2, 0.5, 20, 20)
            else:
                if self.wireframe_mode:
                    glutWireTorus(0.2, 0.5, 20, 20)
                else:
                    glutSolidTorus(0.2, 0.5, 20, 20)
                    
        elif shape_type == "Tetrahedron":
            if is_shadow:
                glutSolidTetrahedron()
            else:
                if self.wireframe_mode:
                    glutWireTetrahedron()
                else:
                    glutSolidTetrahedron()
                    
        elif shape_type == "Octahedron":
            if is_shadow:
                glutSolidOctahedron()
            else:
                if self.wireframe_mode:
                    glutWireOctahedron()
                else:
                    glutSolidOctahedron()
                    
        elif shape_type == "Dodecahedron":
            if is_shadow:
                glutSolidDodecahedron()
            else:
                if self.wireframe_mode:
                    glutWireDodecahedron()
                else:
                    glutSolidDodecahedron()
                    
        elif shape_type == "Icosahedron":
            if is_shadow:
                glutSolidIcosahedron()
            else:
                if self.wireframe_mode:
                    glutWireIcosahedron()
                else:
                    glutSolidIcosahedron()
                    
    def draw_shape_without_shadow(self, shape):
        """Dibuja una forma 3D sin sombra"""
        glPushMatrix()
        glTranslatef(shape.position[0], shape.position[1], shape.position[2])
        glRotatef(shape.rotation[0], 1, 0, 0)
        glRotatef(shape.rotation[1], 0, 1, 0)
        glRotatef(shape.rotation[2], 0, 0, 1)
        glScalef(shape.scale, shape.scale, shape.scale)
        
        glColor4fv(shape.color)
        self.draw_shape_geometry(shape.shape_type)
        
        glPopMatrix()
        
    def draw_shape(self, shape):
        """Dibuja una forma 3D (método legacy mantenido por compatibilidad)"""
        self.draw_shape_without_shadow(shape)
        
    def draw_ground(self):
        """Dibuja el suelo"""
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-5, -2, -5)
        glVertex3f(5, -2, -5)
        glVertex3f(5, -2, 5)
        glVertex3f(-5, -2, 5)
        glEnd()
        glEnable(GL_LIGHTING)
        glPopMatrix()
        
    def render(self):
        if self.need_resize:
            self.resize_viewport(self.new_width, self.new_height)
            self.need_resize = False

        """Renderiza la escena"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posición de la cámara
        gluLookAt(5, 3, 5, 0, 0, 0, 0, 1, 0)
        
        # Aplicar rotación global
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Actualizar posición de la luz después de las rotaciones
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        
        # Dibujar suelo
        self.draw_ground()
        
        # Dibujar sombras primero (sin profundidad)
        glDisable(GL_DEPTH_TEST)
        for shape in self.shapes:
            self.draw_shadow(shape)
        glEnable(GL_DEPTH_TEST)
        
        # Dibujar todas las formas
        for shape in self.shapes:
            self.draw_shape_without_shadow(shape)
            
        glutSwapBuffers()
        
    def add_shape(self, x, y):
        """Añade una forma en la posición del mouse"""
        # Convertir coordenadas de pantalla a coordenadas del mundo
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        
        # Obtener la coordenada Z del punto
        z = glReadPixels(x, viewport[3] - y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        
        # Si no hay profundidad, usar el plano del suelo
        if z == 1.0:
            z = 0.5
            
        # Proyectar de vuelta al espacio del mundo
        try:
            world_coords = gluUnProject(x, viewport[3] - y, z, modelview, projection, viewport)
            pos_x, pos_y, pos_z = world_coords
        except:
            # Si falla, usar posición por defecto
            pos_x, pos_y, pos_z = 0, 0, 0
            
        # Crear nueva forma
        new_shape = Shape3D(
            self.current_shape, 
            [pos_x, pos_y, pos_z], 
            self.current_color.copy(),
            self.wireframe_mode
        )
        
        # Añadir rotación aleatoria
        new_shape.rotation = [
            np.random.uniform(0, 360),
            np.random.uniform(0, 360),
            np.random.uniform(0, 360)
        ]
        
        self.shapes.append(new_shape)
        
    def mouse_click(self, button, state, x, y):
        """Maneja los clicks del mouse"""
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_pressed = True
                self.mouse_old_x = x
                self.mouse_old_y = y
                # Añadir forma en la posición del click
                self.add_shape(x, y)
            else:
                self.mouse_pressed = False
                
    def mouse_motion(self, x, y):
        """Maneja el movimiento del mouse"""
        if self.mouse_pressed:
            dx = x - self.mouse_old_x
            dy = y - self.mouse_old_y
            
            self.rotation_y += dx * 0.5
            self.rotation_x += dy * 0.5
            
            self.mouse_old_x = x
            self.mouse_old_y = y
            
            glutPostRedisplay()

class App3D:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplicativo 3D con GLUT")
        self.root.geometry("400x600")
        
        self.renderer = OpenGLRenderer()
        self.opengl_thread = None
        self.running = False
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configura la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Aplicativo 3D con GLUT", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Selección de figura
        ttk.Label(main_frame, text="Seleccionar Figura:").grid(row=1, column=0, sticky=tk.W)
        self.shape_var = tk.StringVar(value="Cube")
        shapes = ["Cube", "Sphere", "Cone", "Teapot", "Torus", 
                 "Tetrahedron", "Octahedron", "Dodecahedron", "Icosahedron"]
        shape_combo = ttk.Combobox(main_frame, textvariable=self.shape_var, 
                                  values=shapes, state="readonly")
        shape_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        shape_combo.bind('<<ComboboxSelected>>', self.on_shape_change)
        
        # Selección de color
        ttk.Label(main_frame, text="Color:").grid(row=2, column=0, sticky=tk.W)
        color_frame = ttk.Frame(main_frame)
        color_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        colors = [("Rojo", [1.0, 0.0, 0.0, 1.0]), ("Verde", [0.0, 1.0, 0.0, 1.0]), 
                 ("Azul", [0.0, 0.0, 1.0, 1.0]), ("Amarillo", [1.0, 1.0, 0.0, 1.0]),
                 ("Magenta", [1.0, 0.0, 1.0, 1.0]), ("Cyan", [0.0, 1.0, 1.0, 1.0])]
        
        self.color_var = tk.StringVar(value="Rojo")
        for i, (name, color) in enumerate(colors):
            if i % 2 == 0:
                row = 3 + i // 2
                col = 0
            else:
                col = 1
            ttk.Radiobutton(main_frame, text=name, variable=self.color_var, 
                           value=name, command=self.on_color_change).grid(row=row, column=col, sticky=tk.W)
        
        # Opciones de renderizado
        ttk.Label(main_frame, text="Opciones de Renderizado:", 
                 font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=(20, 10))
        
        self.wireframe_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Modo Wireframe", 
                       variable=self.wireframe_var, 
                       command=self.on_wireframe_change).grid(row=7, column=0, columnspan=2, sticky=tk.W)
        
        self.shadows_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Mostrar Sombras", 
                       variable=self.shadows_var, 
                       command=self.on_shadows_change).grid(row=8, column=0, columnspan=2, sticky=tk.W)
        
        self.perspective_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Perspectiva", 
                       variable=self.perspective_var, 
                       command=self.on_perspective_change).grid(row=9, column=0, columnspan=2, sticky=tk.W)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Iniciar Visualización", 
                  command=self.start_opengl).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Escena", 
                  command=self.clear_scene).pack(side=tk.LEFT, padx=5)
        
        # Instrucciones
        instructions = """
Instrucciones:
1. Selecciona una figura y color
2. Haz clic en "Iniciar Visualización"
3. Haz clic en la ventana OpenGL para añadir figuras
4. Arrastra para rotar la vista
5. Usa las opciones para cambiar el renderizado
        """
        ttk.Label(main_frame, text=instructions, 
                 font=("Arial", 9), justify=tk.LEFT).grid(row=11, column=0, columnspan=2, pady=20)
        
        # Configurar expansión
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def on_shape_change(self, event=None):
        """Cambia la figura seleccionada"""
        self.renderer.current_shape = self.shape_var.get()
        
    def on_color_change(self):
        """Cambia el color seleccionado"""
        colors = {"Rojo": [1.0, 0.0, 0.0, 1.0], "Verde": [0.0, 1.0, 0.0, 1.0], 
                 "Azul": [0.0, 0.0, 1.0, 1.0], "Amarillo": [1.0, 1.0, 0.0, 1.0],
                 "Magenta": [1.0, 0.0, 1.0, 1.0], "Cyan": [0.0, 1.0, 1.0, 1.0]}
        self.renderer.current_color = colors[self.color_var.get()]
        
    def on_wireframe_change(self):
        """Cambia el modo wireframe"""
        self.renderer.wireframe_mode = self.wireframe_var.get()
        if self.running:
            glutPostRedisplay()
            
    def on_shadows_change(self):
        """Cambia la visualización de sombras"""
        self.renderer.show_shadows = self.shadows_var.get()
        if self.running:
            glutPostRedisplay()
            
    def on_perspective_change(self):
        """Cambia el modo de perspectiva"""
        self.renderer.perspective_mode = self.perspective_var.get()
        if self.running:
            self.renderer.new_width = glutGet(GLUT_WINDOW_WIDTH)
            self.renderer.new_height = glutGet(GLUT_WINDOW_HEIGHT)
            self.renderer.need_resize = True

            glutPostRedisplay()
            
    def clear_scene(self):
        """Limpia todas las figuras de la escena"""
        self.renderer.shapes.clear()
        if self.running:
            glutPostRedisplay()
            
    def start_opengl(self):
        """Inicia la visualización OpenGL"""
        if not self.running:
            self.running = True
            self.opengl_thread = threading.Thread(target=self.run_opengl)
            self.opengl_thread.daemon = True
            self.opengl_thread.start()
            
    def run_opengl(self):
        """Ejecuta la ventana OpenGL"""
        try:
            glutInit(sys.argv)
            glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
            glutInitWindowSize(800, 600)
            glutInitWindowPosition(100, 100)
            glutCreateWindow(b"Aplicativo 3D - Click para annadir figuras, arrastra para rotar")
            
            self.renderer.init_opengl()
            
            glutDisplayFunc(self.renderer.render)
            glutReshapeFunc(self.renderer.resize_viewport)
            glutMouseFunc(self.renderer.mouse_click)
            glutMotionFunc(self.renderer.mouse_motion)
            glutIdleFunc(lambda: glutPostRedisplay())
            
            glutMainLoop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar OpenGL: {str(e)}")
            self.running = False
            
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    try:
        app = App3D()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicación terminada por el usuario")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Error al ejecutar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()