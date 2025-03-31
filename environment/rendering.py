from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

def draw_rectangle(x, y, width, height, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw background (soil field)
    draw_rectangle(-1, -1, 2, 2, (0.6, 0.4, 0.2))  # Brown soil
    
    # Draw water reservoir (top right corner)
    draw_rectangle(0.6, 0.6, 0.3, 0.3, (0, 0, 1))  # Blue water
    
    # Draw irrigation system (agent) at center
    draw_rectangle(-0.1, -0.1, 0.2, 0.2, (0.0, 1.0, 0.0))  # Green irrigation system
    
    # Draw crops at different stages
    draw_rectangle(-0.8, -0.3, 0.2, 0.4, (0.0, 0.8, 0.0))  # Crop 1
    draw_rectangle(-0.4, -0.3, 0.2, 0.5, (0.0, 0.9, 0.0))  # Crop 2
    draw_rectangle(0.0, -0.3, 0.2, 0.6, (0.0, 1.0, 0.0))  # Crop 3
    
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Smart Irrigation Visualization")
    glutDisplayFunc(display)
    glClearColor(1, 1, 1, 1)  # White background
    glutMainLoop()

if __name__ == "__main__":
    main()
