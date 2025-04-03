from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLU import *
import sys
import numpy as np
from gym import spaces
import gym

# === SmartIrrigationEnv ===
class SmartIrrigationEnv(gym.Env):
    def __init__(self):
        super(SmartIrrigationEnv, self).__init__()
        self.observation_space = spaces.MultiDiscrete([3, 3, 4, 4])
        self.action_space = spaces.Discrete(4)
        self.state = np.array([1, 1, 0, 3])
        self.steps = 0
        self.max_steps = 50
        self.done = False


    def render(self, mode='human'):
        """Render the environment using OpenGL."""
        display()

    def step(self, action):
        soil, weather, stage, water = self.state

        if action == 0:
            soil = min(2, soil + 2)
            water = max(0, water - 2)
        elif action == 1:
            soil = min(2, soil + 1)
            water = max(0, water - 1)
        elif action == 2 and weather == 1:
            soil = max(0, soil - 1)
        elif action == 3:
            soil = max(0, soil - 1)

        reward = 10 if soil == 1 else -5

        if self.steps % 10 == 0 and stage < 3:
            stage += 1

        if water == 0 or stage == 3 or self.steps >= self.max_steps:
            self.done = True

        self.state = np.array([soil, weather, stage, water])
        self.steps += 1
        return self.state, reward, self.done, {}

    def reset(self):
        self.state = np.array([1, 1, 0, 3])
        self.steps = 0
        self.done = False
        return self.state

# === Global Vars ===
env = SmartIrrigationEnv()
state = env.reset()

agent_x = -0.1
agent_y = -0.1
agent_width = 0.2
agent_height = 0.2
direction = 1
terminated = False
last_action = 3
action_names = [
    "Full Irrigation",
    "Partial Irrigation",
    "Delay Irrigation",
    "Stop / Conserve Water"
]

# === Drawing Utilities ===
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

# === Render Scene ===
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    global state, agent_x, last_action, terminated

    soil, weather, stage, water = state

    soil_colors = [(0.8, 0.5, 0.3), (0.6, 0.4, 0.2), (0.4, 0.3, 0.1)]
    draw_rectangle(-1, -1, 2, 2, soil_colors[soil])

    water_heights = [0.05, 0.1, 0.2, 0.3]
    draw_rectangle(0.6, 0.6, 0.3, water_heights[water], (0, 0, 1))

    draw_rectangle(agent_x, agent_y, agent_width, agent_height, (0.0, 1.0, 0.0))

    crop_heights = [0.2, 0.4, 0.6, 0.8]
    crop_color = (0.0, 0.6 + 0.1 * stage, 0.0)
    for i in range(-8, 1, 4):
        draw_rectangle(i / 10.0, -0.3, 0.2, crop_heights[stage], crop_color)

    if not terminated:
        draw_text(-0.95, 0.9, f"Action Taken: {action_names[last_action]}")
    else:
        draw_text(-0.6, 0.9, "Simulation completed.")

    glutSwapBuffers()

# === Smooth Agent Movement Frame-by-Frame ===

def idle():
    global agent_x, direction, last_action

    # Agent moves only on irrigation
    if last_action in [0, 1] and not terminated:
        agent_x += 0.0015 * direction  # slower speed
        if agent_x > 0.8 or agent_x < -1.0:
            direction *= -1

    glutPostRedisplay()


# === Decision Maker (per second) ===
def update(value):
    global state, last_action, terminated

    if not env.done:
        action = env.action_space.sample()
        last_action = action
        state, _, done, _ = env.step(action)
        env.done = done
        glutTimerFunc(1000, update, 0)
    else:
        terminated = True
        print("Simulation completed.")

# === Keyboard ESC Handler ===
def keyboard(key, x, y):
    if key == b'\x1b':
        print("Exiting simulation...")
        sys.exit()

# === Main Launcher ===

def render(self, mode='human'):
    """Render the environment using OpenGL."""
    glutMainLoopEvent()
    display()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Smart Irrigation - Agent Movement")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glClearColor(1, 1, 1, 1)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()