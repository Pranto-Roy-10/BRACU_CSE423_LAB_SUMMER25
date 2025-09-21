from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time



W_Width, W_Height = 500, 500
SCREEN_LEFT=-W_Width / 2
SCREEN_RIGHT=W_Width / 2
SCREEN_TOP=W_Height / 2
SCREEN_BOTTOM=-W_Height / 2

gameState="playing"
has_started = False
score=0
last_frame_time=0

catcher_width=110
catcher_height=20
catcher_pos={'x':0,'y':SCREEN_BOTTOM+25}
catcher_color=(1.0,1.0,1.0)
catcher_speed=300

diamond_size=13
diamond_pos={'x': 0, 'y': SCREEN_TOP}
diamond_fall_speed=150
diamond_acceleration=10
diamond_color=(1.0,1.0,0.0)

restart_button = {'x': SCREEN_LEFT + 20, 'y': SCREEN_TOP - 50, 'w': 40, 'h': 40}
pause_button = {'x': -20, 'y': SCREEN_TOP - 50, 'w': 40, 'h': 40}
exit_button = {'x': SCREEN_RIGHT - 60, 'y': SCREEN_TOP - 50, 'w': 40, 'h': 40}
# ballx = bally = 0
# speed = 0.01
# ball_size = 2
# create_new = False


class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x

    return result


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def draw_points(x, y, s=2):
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(float(x), float(y))  # jekhane show korbe pixel
    glEnd()


def drawAxes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(250, 0)
    glVertex2f(-250, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0, 250)
    glVertex2f(0, -250)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 1.0, 0.0)
    glVertex2f(0, 0)

    glEnd()

def find_zone(dx, dy):
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx <= 0 and dy >= 0: return 3
        if dx <= 0 and dy <= 0: return 4
        if dx >= 0 and dy <= 0: return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx <= 0 and dy >= 0: return 2
        if dx <= 0 and dy <= 0: return 5
        if dx >= 0 and dy <= 0: return 6

def drawShapes():
    glBegin(GL_TRIANGLES)
    glVertex2d(-170, 170)
    glColor3f(0, 1.0, 0.0)
    glVertex2d(-180, 150)
    glColor3f(1, 0, 0.0)
    glVertex2d(-160, 150)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2d(-170, 120)
    glColor3f(1, 0, 1)
    glVertex2d(-150, 120)
    glColor3f(0, 0, 1)
    glVertex2d(-150, 140)
    glColor3f(0, 1, 0)
    glVertex2d(-170, 140)
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y
    return x, y

def convert_from_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y
    return x, y
def draw_line_midpoint(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = find_zone(dx, dy)
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    dx_z0, dy_z0 = x2_z0 - x1_z0, y2_z0 - y1_z0
    d = 2 * dy_z0 - dx_z0
    incE, incNE = 2 * dy_z0, 2 * (dy_z0 - dx_z0)
    x, y = x1_z0, y1_z0
    while x <= x2_z0:
        original_x, original_y = convert_from_zone0(x, y, zone)
        draw_points(original_x, original_y)
        x += 1
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
def draw_catcher():
    glColor3f(*catcher_color)
    x, y = catcher_pos['x'], catcher_pos['y']
    w, h = catcher_width / 2, catcher_height
    side = 20
    draw_line_midpoint(x - w, y, x + w, y)
    draw_line_midpoint(x - w, y, x - w + side, y - h)
    draw_line_midpoint(x + w, y, x + w - side, y - h)
    draw_line_midpoint(x - w + side, y - h, x + w - side, y - h)


def draw_diamond():
    glColor3f(*diamond_color)
    x, y = diamond_pos['x'], diamond_pos['y']
    s = diamond_size
    draw_line_midpoint(x, y + s, x + s // 2, y)
    draw_line_midpoint(x + s // 2, y, x, y - s)
    draw_line_midpoint(x, y - s, x - s // 2, y)
    draw_line_midpoint(x - s // 2, y, x, y + s)

def draw_ui():
    glColor3f(0.0, 1.0, 1.0)
    x, y = restart_button['x'], restart_button['y']
    draw_line_midpoint(x + 35, y + 20, x + 10, y + 20)
    draw_line_midpoint(x + 10, y + 20, x + 20, y + 30)
    draw_line_midpoint(x + 10, y + 20, x + 20, y + 10)
    glColor3f(1.0, 0.75, 0.0)
    x, y = pause_button['x'], pause_button['y']
    if gameState == 'playing':
        draw_line_midpoint(x + 12, y + 10, x + 12, y + 30)
        draw_line_midpoint(x + 28, y + 10, x + 28, y + 30)
    else:
        draw_line_midpoint(x + 10, y + 10, x + 10, y + 30)
        draw_line_midpoint(x + 10, y + 30, x + 30, y + 20)
        draw_line_midpoint(x + 30, y + 20, x + 10, y + 10)
    glColor3f(1.0, 0.0, 0.0)
    x, y = exit_button['x'], exit_button['y']
    draw_line_midpoint(x + 10, y + 10, x + 30, y + 30)
    draw_line_midpoint(x + 30, y + 10, x + 10, y + 30)

def start_new_diamond():
    global diamond_color
    diamond_pos['y'] = SCREEN_TOP-52
    diamond_pos['x'] = random.randint(int(SCREEN_LEFT + diamond_size), int(SCREEN_RIGHT - diamond_size))
    diamond_color = (random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5, random.random() * 0.5 + 0.5)

def restart_game():
    global score, gameState, catcher_color, diamond_fall_speed, last_frame_time, has_started
    score, gameState = 0, "playing"
    catcher_pos['x'] = 0
    catcher_color = (1.0, 1.0, 1.0)
    diamond_fall_speed = 150
    if has_started:
        print("Starting Over")
    start_new_diamond()
    last_frame_time = time.time()
    has_started = True

def aabb_collision_check():
    catcher_box = {'x': catcher_pos['x'] - catcher_width / 2, 'y': catcher_pos['y'], 'w': catcher_width,
                   'h': catcher_height}
    diamond_box = {'x': diamond_pos['x'] - diamond_size, 'y': diamond_pos['y'] - diamond_size, 'w': diamond_size * 2,
                   'h': diamond_size * 2}
    return (catcher_box['x'] < diamond_box['x'] + diamond_box['w'] and
            catcher_box['x'] + catcher_box['w'] > diamond_box['x'] and
            catcher_box['y'] < diamond_box['y'] + diamond_box['h'] and
            catcher_box['y'] + catcher_box['h'] > diamond_box['y'])

def keyboardListener(key, x, y):
    # global ball_size
    # if key == b'w':
    #     ball_size += 1
    #     print("Size Increased")
    # if key == b's':
    #     ball_size -= 1
    #     print("Size Decreased")
    # # if key==b's':
    # #    print(3)
    # # if key==b'd':
    # #     print(4)
    if key == b'\x1b':
        glutLeaveMainLoop()



def specialKeyListener(key, x, y):
    # global speed
    # if key == 'w':
    #     print(1)
    # if key == GLUT_KEY_UP:
    #     speed *= 2
    #     print("Speed Increased")
    # if key == GLUT_KEY_DOWN:  # // up arrow key
    #     speed /= 2
    #     print("Speed Decreased")
    # glutPostRedisplay()
    # if key==GLUT_KEY_RIGHT:

    # if key==GLUT_KEY_LEFT:

    # if key==GLUT_KEY_PAGE_UP:

    # if key==GLUT_KEY_PAGE_DOWN:

    # case GLUT_KEY_INSERT:
    #
    #
    # case GLUT_KEY_HOME:
    #
    # case GLUT_KEY_END:
    #
    if gameState == "playing":
        if key == GLUT_KEY_LEFT:
            catcher_pos['x'] -= 20
        elif key == GLUT_KEY_RIGHT:
            catcher_pos['x'] += 20
        left_boundary = SCREEN_LEFT + catcher_width / 2
        right_boundary = SCREEN_RIGHT - catcher_width / 2
        if catcher_pos['x'] < left_boundary:
            catcher_pos['x'] = left_boundary
        if catcher_pos['x'] > right_boundary:
            catcher_pos['x'] = right_boundary


def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    # global ballx, bally, create_new
    # if button == GLUT_LEFT_BUTTON:
    #     if (state == GLUT_DOWN):  # // 2 times?? in ONE click? -- solution is checking DOWN or UP
    #         print(x, y)
    #         c_X, c_y = convert_coordinate(x, y)
    #         ballx, bally = c_X, c_y
    #
    # if button == GLUT_RIGHT_BUTTON:
    #     if state == GLUT_DOWN:
    #         create_new = convert_coordinate(x, y)
    # # case GLUT_MIDDLE_BUTTON:
    # #     //........
    global gameState
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_x = x - W_Width / 2
        gl_y = W_Height / 2 - y
        if (restart_button['x'] <= gl_x <= restart_button['x'] + restart_button['w'] and
                restart_button['y'] <= gl_y <= restart_button['y'] + restart_button['h']):
            restart_game()
        elif (pause_button['x'] <= gl_x <= pause_button['x'] + pause_button['w'] and
              pause_button['y'] <= gl_y <= pause_button['y'] + pause_button['h']):
            gameState = "paused" if gameState == "playing" else "playing"
        elif (exit_button['x'] <= gl_x <= exit_button['x'] + exit_button['w'] and
              exit_button['y'] <= gl_y <= exit_button['y'] + exit_button['h']):
            print(f"Goodbye! Final Score: {score}")
            glutLeaveMainLoop()


def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(0, 0, 0, 0);  # //color black
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # # //load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # # //initialize the matrix
    glLoadIdentity()
    # # //now give three info
    # # //1. where is the camera (viewer)?
    # # //2. where is the camera looking?
    # # //3. Which direction is the camera's UP direction?
    # gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    # glMatrixMode(GL_MODELVIEW)
    #
    # drawAxes()
    # global ballx, bally, ball_size
    # draw_points(ballx, bally, ball_size)
    # drawShapes()
    #
    # glBegin(GL_LINES)
    # glVertex2d(180, 0)
    # glVertex2d(180, 180)
    # glVertex2d(180, 180)
    # glVertex2d(0, 180)
    # glEnd()
    #
    # if (create_new):
    #     m, n = create_new
    #     glBegin(GL_POINTS)
    #     glColor3f(0.7, 0.8, 0.6)
    #     glVertex2f(m, n)
    #     glEnd()
    draw_catcher()
    if gameState != 'gameover':
        draw_diamond()
    draw_ui()
    glutSwapBuffers()


def animate():
    # //codes for any changes in Models, Camera
    global last_frame_time, gameState, score, catcher_color, diamond_fall_speed
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time
    if gameState == "playing":
        diamond_fall_speed += diamond_acceleration * delta_time
        diamond_pos['y'] -= diamond_fall_speed * delta_time
        if aabb_collision_check():
            score += 1
            diamond_fall_speed += diamond_acceleration
            print(f"Score: {score}")
            start_new_diamond()
        elif diamond_pos['y'] < SCREEN_BOTTOM:
            gameState = "gameover"
            catcher_color = (1.0, 0.0, 0.0)
            print(f"Game Over! Score: {score}")
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(SCREEN_LEFT, SCREEN_RIGHT, SCREEN_BOTTOM, SCREEN_TOP)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(100, 100)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Catch the Diamonds!")
init()
restart_game()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
