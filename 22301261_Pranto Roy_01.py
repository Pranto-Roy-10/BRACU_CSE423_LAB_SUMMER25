#Task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random

raindrops=[]
rain_speed=0.5
rain_displace=0.0
is_night = False
TILT_LIMIT = 0.5
current_bg = [0.8, 0.9, 1.0]
target_bg = [0.8, 0.9, 1.0]
transition_speed = 0.0005

W_Width, W_Height = 1920,1080

ballx = bally = 0
speed = 0.01
ball_size = 2
create_new = False


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


def draw_points(x, y, s):
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()

def draw_line(x1, y1, x2, y2):
    glLineWidth(3)  # Line thickness (default is 1)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
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


def draw_Quad(x1, y1,x2,y2):
    glLineWidth(5) #pixel size. by default 1 thake
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)  # Bottom-left
    glVertex2f(x2, y1)  # Bottom-right
    glVertex2f(x2, y2)  # Top-right
                                             #USED FOR GROUND
    # Second triangle
    glVertex2f(x1, y1)  # Bottom-left
    glVertex2f(x2, y2)  # Top-right
    glVertex2f(x1, y2)  # Top-left
    glEnd()

def draw_triangle_tree(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x1, y1)  # First vertex
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x2, y2)  # Second vertex
    glColor3f(0.0, 0.4, 0.0)
    glVertex2f(x3, y3)  # Third vertex
    glEnd()

def draw_triangle_roof(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)  # First vertex
    glVertex2f(x2, y2)  # Second vertex
    glVertex2f(x3, y3)  # Third vertex
    glEnd()

def draw_repeating_triangles(start_x, end_x, base_y, height, count):
    glColor3f(0.0, 0.8, 0.0)  # Green color
    step = (end_x - start_x) / count
    for i in range(count):
        x1 = start_x + i * step
        x2 = x1 + step
        mid_x = (x1 + x2) / 2
        draw_triangle_tree(x1, base_y, x2, base_y, mid_x, base_y + height)

def init_rain(count=600):
    global raindrops
    raindrops = []

    max_length = 30
    max_displace = TILT_LIMIT  # max sideways reach
    x_margin = int(max_length * max_displace * 4) + 200
    y_spawn_height = 1080 + 300  # vertical spawn space above screen

    for _ in range(count):
        x = random.randint(-x_margin, 1920 + x_margin)
        y = random.randint(0, y_spawn_height)
        length = random.randint(10, max_length)
        alpha = random.uniform(0.3, 1.0)
        raindrops.append([x, y, length, alpha])


def draw_rain():
    glLineWidth(2)
    glBegin(GL_LINES)
    for drop in raindrops:
        x, y, length, alpha = drop
        if is_night:
            glColor4f(0.5, 0.6, 0.8, alpha * 0.8)  # dim blue
        else:
            glColor4f(0.6, 0.8, 1.0, alpha)        # bright blue
        glVertex2f(x, y)
        glVertex2f(x + rain_displace * length, y - length)
    glEnd()

def update_rain():
    global raindrops
    for drop in raindrops:
        drop[0] += rain_displace
        drop[1] -= rain_speed

        # If off-screen from any side, recycle with wider spawn area
        if drop[1] < 0 or drop[0] < -600 or drop[0] > 1920 + 600:
            drop[0] = random.randint(-600, 1920 + 600)
            drop[1] = 1080 + random.randint(0, 300)


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
    #
    # glutPostRedisplay()
    global target_bg
    if key == b'd' or key == b'D':
        target_bg = [0.8, 0.9, 1.0]  # Day sky
        print("Transitioning to DAY")
    elif key == b'n' or key == b'N':
        target_bg = [0.05, 0.05, 0.1]  # Night sky
        print("Transitioning to NIGHT")

def update_background_color():
    global current_bg, target_bg
    for i in range(3):
        if abs(current_bg[i] - target_bg[i]) > 0.01:
            if current_bg[i] < target_bg[i]:
                current_bg[i] += transition_speed
            else:
                current_bg[i] -= transition_speed

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
    global rain_displace, rain_speed

    if key == GLUT_KEY_LEFT:
        rain_displace -= 0.1
        rain_speed = 0.8

    elif key == GLUT_KEY_RIGHT:
        rain_displace += 0.1
        rain_speed = 0.8
    elif key == GLUT_KEY_DOWN:
        rain_displace = 0.0
        rain_speed = 0.5
        print("Rain reset to vertical.")

    # Clamp tilt and speed
    rain_displace = max(-TILT_LIMIT, min(TILT_LIMIT, rain_displace))
    print(f"Tilt: {rain_displace:.2f}, Speed: {rain_speed:.2f}")
    glutPostRedisplay()

def mouseListener(button, state, x, y):  # /#/x, y is the x-y of the screen (2D)
    global ballx, bally, create_new
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):  # // 2 times?? in ONE click? -- solution is checking DOWN or UP
            print(x, y)
            c_X, c_y = convert_coordinate(x, y)
            ballx, bally = c_X, c_y

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            create_new = convert_coordinate(x, y)
    # case GLUT_MIDDLE_BUTTON:
    #     //........

    glutPostRedisplay()


def display():
    update_background_color()
    glClearColor(current_bg[0], current_bg[1], current_bg[2], 1.0)
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(0, 0, 0, 0);  # //color black
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # # //load the correct matrix -- MODEL-VIEW matrix
    # glMatrixMode(GL_MODELVIEW)
    # # //initialize the matrix
    glLoadIdentity()
    # //now give three info
    # //1. where is the camera (viewer)?
    # //2. where is the camera looking?
    # //3. Which direction is the camera's UP direction?
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
    glColor3f(107 / 255.0, 67 / 255.0, 28 / 255.0)  # konokichur color set (RGB)
    # call the draw methods here
    draw_Quad(0, 0, 1920, 720)  # Ground ready 1st layer

    # TREES
    # glColor3f(0.0, 0.8, 0.0)
    draw_repeating_triangles(start_x=0, end_x=1920, base_y=570, height=120, count=30)

    # Roof
    glColor3f(71 / 255, 17 / 255, 189 / 255)
    draw_triangle_roof(540, 590, 960, 750, 1380, 590)

    # HouseBody
    glColor3f(1, 1, 1)
    draw_Quad(590, 340, 1330, 590)

    # Windows1
    glColor3f(143 / 255, 179 / 255, 242 / 255)
    draw_Quad(740, 420, 880, 540)
    glColor3f(0, 0, 0)
    draw_line(810, 420, 810, 540)
    draw_line(740, 480, 880, 480)

    # Door
    glColor3f(92 / 255, 86 / 255, 88 / 255)
    draw_Quad(920, 340, 1040, 540)
    glColor3f(0, 0, 0)
    draw_points(1020, 440,20)

    # Windows2
    glColor3f(143 / 255, 179 / 255, 242 / 255)
    draw_Quad(1080, 420, 1220, 540)
    glColor3f(0, 0, 0)
    draw_line(1150, 420, 1150, 540)
    draw_line(1080, 480, 1220, 480)

    # Layer Rain
    update_rain()
    draw_rain()
    glutSwapBuffers()



def animate():
    # //codes for any changes in Models, Camera
    glutPostRedisplay()
    global ballx, bally, speed
    ballx = (ballx + speed) % 180
    bally = (bally + speed) % 180


def init():
    # //clear the screen
    glClearColor(0, 0, 0, 0)
    # //load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # //initialize the matrix
    glLoadIdentity()
    # //give PERSPECTIVE parameters
    # gluPerspective(104, 1, 1, 1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    # //near distance
    # //far distance
    gluOrtho2D(0, W_Width, 0, W_Height)
    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # //Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)  # display callback function
# glutIdleFunc(animate)  # what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)
init()
init_rain()
glutIdleFunc(display)
glutMainLoop()

glutMainLoop()  # The main loop of OpenGL
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#TASK2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math,random

W_Width, W_Height = 500, 500

ballx = bally = 0
speed = 0.01
ball_size = 2
create_new = False
boundary = 260
points = []             # list of all active points
global_speed = 0.05      # multiplier for every point
frozen = False          # freeze flag
blinking = False        # blink flag
blink_timer = 0         # cycles through 0..59 for 1-second blink

class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.z = 0
        self.dx = random.choice([-1, 1]) * random.uniform(0.5, 2.0)
        self.dy = random.choice([-1, 1]) * random.uniform(0.5, 2.0)
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
    def move(self):
        if frozen:
            return
        self.x += self.dx * global_speed
        self.y += self.dy * global_speed

        # bounce on the boundary
        if abs(self.x) >= boundary:
            self.dx *= -1
            self.x = boundary * (-1 if self.x < 0 else 1)
        if abs(self.y) >= boundary:
            self.dy *= -1
            self.y = boundary * (-1 if self.y < 0 else 1)

    def draw(self):
        if blinking :      # black for 30 frames
            glColor3f(0, 0, 0)
        else:
            glColor3f(self.r, self.g, self.b)
        draw_points(self.x, self.y, 5)

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


def draw_points(x, y, s):
    glPointSize(s)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()

def draw_boundary():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    for dx, dy in [(-1,-1),(1,-1),(1,1),(-1,1)]:
        glVertex2f(dx * boundary, dy * boundary)
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


def keyboardListener(key, x, y):
    global global_speed, frozen
    if frozen and key != b' ':
        return

    if key == b' ':
        frozen = not frozen
    # if key==b's':
    #    print(3)
    # if key==b'd':
    #     print(4)

    glutPostRedisplay()


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
    global global_speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        global_speed = min(global_speed * 1.5, 10.0)
    elif key == GLUT_KEY_DOWN:
        global_speed = max(global_speed / 1.5, 0.1)
    glutPostRedisplay()


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
    global blinking
    c_X, c_Y = convert_coordinate(x, y)
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not frozen:
        points.append(point(c_X, c_Y))

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not frozen:
        blinking = not blinking

    glutPostRedisplay()



def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0);  # //color black
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # //load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # //initialize the matrix
    glLoadIdentity()
    # //now give three info
    # //1. where is the camera (viewer)?
    # //2. where is the camera looking?
    # //3. Which direction is the camera's UP direction?
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
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

    if blinking and (blink_timer // 120) % 2:
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)

    draw_boundary()
    for p in points:
        p.draw()
    glutSwapBuffers()


def animate():
    # //codes for any changes in Models, Camera
    # glutPostRedisplay()
    # global ballx, bally, speed
    # ballx = (ballx + speed) % 180
    # bally = (bally + speed) % 180
    global blink_timer
    if not frozen:
        for p in points:
            p.move()
    if blinking:
        blink_timer = (blink_timer + 1) % 60
    glutPostRedisplay()

def init():
    # //clear the screen
    # glClearColor(0, 0, 0, 0)
    # # //load the PROJECTION matrix
    # glMatrixMode(GL_PROJECTION)
    # # //initialize the matrix
    # glLoadIdentity()
    # # //give PERSPECTIVE parameters
    # gluPerspective(104, 1, 1, 1000.0)
    # # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    # # //near distance
    # # //far distance
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # //Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Magic box")
init()
glutDisplayFunc(display)  # display callback function
glutIdleFunc(animate)  # what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()  # The main loop of OpenGL
