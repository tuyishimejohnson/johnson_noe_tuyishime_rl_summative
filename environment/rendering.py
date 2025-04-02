from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import sys
import numpy as np
from gym import spaces
import gym

# === Static SmartIrrigationEnv ===
class SmartIrrigationEnv(gym.Env):
    def __init__(self):
        super(SmartIrrigationEnv, self).__init__()
        self.observation_space = spaces.MultiDiscrete([3, 3, 4, 4])
        self.action_space = spaces.Discrete(4)
        self.state = np.array([1, 1, 2, 2])
        self.done = False

    def reset(self):
        return self.state

# === Initialize Environment ===
env = SmartIrrigationEnv()
state = env.reset()

# Static variables for display
agent_x = -0.1
agent_y = -0.1
agent_width = 0.2
agent_height = 0.2
last_action = 0  # ex: Full Irrigation
action_names = ["Full Irrigation", "Partial", "Delay", "Stop"]

# === Drawing Functions ===
def draw_rectangle(x, y, width, height, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0, 0, 0)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

# === Static Display ===
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    soil, weather, stage, water = state

    # Soil
    soil_colors = [(0.8, 0.5, 0.3), (0.6, 0.4, 0.2), (0.4, 0.3, 0.1)]
    draw_rectangle(-1, -1, 2, 2, soil_colors[soil])

    # Water tank
    water_heights = [0.05, 0.1, 0.2, 0.3]
    draw_rectangle(0.6, 0.6, 0.3, water_heights[water], (0, 0, 1))

    # Agent
    draw_rectangle(agent_x, agent_y, agent_width, agent_height, (0.0, 1.0, 0.0))

    # Crops
    crop_heights = [0.2, 0.4, 0.6, 0.8]
    crop_color = (0.0, 0.6 + 0.1 * stage, 0.0)
    for i in range(-8, 1, 4):
        draw_rectangle(i / 10.0, -0.3, 0.2, crop_heights[stage], crop_color)

    # Action label
    draw_text(-0.95, 0.9, f"Action: {action_names[last_action]}")

    glutSwapBuffers()

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Smart Irrigation - Static Environment")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glClearColor(1, 1, 1, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()