import pygame
import numpy as np
from scipy.special import comb
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Editor")

# Fonts
font = pygame.font.Font(None, 20)

# Helper functions
def bezier_curve(points, num_points=100):
    points = np.array(points)
    t = np.linspace(0, 1, num_points)
    curve = np.zeros((num_points, 2))
    n = len(points) - 1
    for i in range(num_points):
        curve[i] = sum(
            comb(n, k) * (1 - t[i]) ** (n - k) * t[i] ** k * points[k]
            for k in range(n + 1)
        )
    return curve

def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    screen.blit(font.render(text, True, WHITE), (rect[0] + 10, rect[1] + 10))

def draw_curve(screen, points):
    if len(points) > 1:
        curve = bezier_curve(points)
        pygame.draw.lines(screen, RED, False, curve, 2)

def draw_points(screen, points):
    for point in points:
        pygame.draw.circle(screen, GREEN, point, 5)

def draw_selection(screen, point):
    pygame.draw.rect(screen, BLUE, (point[0] - 10, point[1] - 10, 20, 20), 2)

def curve_0(curve_no):
    print(curve_no)


# Main loop
running = True
clock = pygame.time.Clock()
points = []
curves = []
dropdown = None
selected_point = None
selected_point_c = None
selected_curve = None
drawing = True
select_mode = False
current_state = None
choices_drop =['None']
values_drop =[0]
values = [0]
choices = ['None']
# Button setup
add_curve_button = pygame.Rect(10, 10, 150, 50)
select_button = pygame.Rect(10, 70, 150, 50)
dropdown_button = pygame.Rect(170, 10, 150, 50)
select_curve = pygame.Rect(10, 70, 150, 50)
# dropdown = Dropdown(
#     screen, 170, 10, 100, 50, name='Select Color', choices=choices_drop,
#     textColour=(255, 255, 255), colour=pygame.Color(BLUE), values=values_drop, direction='down', textHAlign='left',
# )
delete_point_button = pygame.Rect(10, 130, 150, 50)
delete_curve_button = pygame.Rect(10, 190, 150, 50)

while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    # Event handling
    for event in events:
        pygame_widgets.update(event)
        if event.type == pygame.QUIT:
            running = False
        # Mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if dropdown_button.collidepoint(mouse_pos):    # If select button is pressed stop drawing
                drawing = False                          # and enter select mode
                select_mode = False

                if points != []:                           # is pressed and start drawing a new curve
                    curves.append(points[:])
                points = []
                if curves:
                    num_curves = len(curves)
                    for i, curve in enumerate(curves):
                        if i == 0:
                            choices_drop = [f'curve{i+1}']
                            values_drop = [i+1]
                        if i > 0:
                            choices_drop.append(f'curve{i+1}')
                            values_drop.append(i+1)
                    values = values_drop
                    choices = choices_drop
                dropdown = Dropdown(
                    screen, 330, 10, 150, 50, name='Select Curve', choices=choices_drop,
                    textColour=(255, 255, 255), colour=pygame.Color(BLUE), values=values_drop, direction='down',
                    textHAlign='left',
                )

                #dropdown_curves = curves
            if add_curve_button.collidepoint(mouse_pos):   # Add active curve to curves when add curves button
                if points != []:                           # is pressed and start drawing a new curve
                    curves.append(points[:])
                points = []
                drawing = True
                select_mode = False
                values = ['None']
                selected_curve = None
                dropdown = None
            elif drawing:
                if not select_button.collidepoint(mouse_pos):
                    points.append(list(mouse_pos))
            if select_button.collidepoint(mouse_pos):    # If select button is pressed stop drawing
                drawing = False                          # and enter select mode
                select_mode = True
            if select_mode:                              # If in select mode and mouse position is
                for j, point in enumerate(points):       # less than 10pxls from point select point as j
                    if pygame.Vector2(point).distance_to(mouse_pos) < 10:
                        selected_point = j
                if selected_curve:
                    for y, curve_point in enumerate(curves[selected_curve-1]):       # less than 10pxls from point select point as j
                        if pygame.Vector2(curve_point).distance_to(mouse_pos) < 10:
                            selected_point_c = y

        if event.type == pygame.MOUSEBUTTONUP:
            selected_point = None
            selected_point_c = None
        if event.type == pygame.MOUSEMOTION:
            if selected_point is not None:
                points[selected_point] = list(event.pos)
            if selected_point_c is not None:
                curves[selected_curve-1][selected_point_c] = list(event.pos)
        # Key inputs
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_p):               # If any key is pressed and if key is p print curve in curves
                if curves:
                    num_curves = len(curves)
                    if dropdown:
                        selected_curve = dropdown.getSelected()
                        print(f'Selected curve {selected_curve}')           # This is temporary
                    for i, curve in enumerate(curves):
                        print(f'curve{i+1}: ',curve)

            if (event.key == pygame.K_RETURN):         # If key is return append points to curve and set points to blank list
                select_mode = False
                drawing = False
                values = ['None']
                selected_curve = None
                dropdown = None
                if points != []:
                    curves.append(points[:])
                    points = []
    pygame_widgets.update(events)



    # Drawing
    draw_button(screen, "Add Curve", add_curve_button, BLUE)
    draw_button(screen, "Edit Points", select_button, BLUE)
    draw_button(screen, "Update Curves", dropdown_button, BLUE)
    for i, curve_points in enumerate(curves):
        draw_curve(screen, curve_points)

    if dropdown:
        selected_curve = dropdown.getSelected()
    if selected_curve:
        draw_points(screen, curves[selected_curve-1])

    draw_points(screen, points)
    draw_curve(screen, points)

    if selected_point is not None:
        draw_selection(screen, points[selected_point])
    if selected_point_c is not None:
        draw_selection(screen, curves[selected_curve-1][selected_point_c])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()