import pygame, json, tkinter, time
from tkinter import filedialog, messagebox

WIDTH, HEIGHT = 1920, 1080

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


BG_COLOR = (20, 20, 20)
KEY_COLOR = (200, 200, 200)
SELECTED_COLOR = (100, 170, 255)
TEXT_COLOR = (20, 20, 20)

key_size = 80
border_size = key_size // 8
snap_grid = 8
snap_size = key_size / snap_grid

screen_border = 10

keyMax = [WIDTH // key_size, HEIGHT // key_size]
keyStartPos = [(WIDTH - keyMax[0] * key_size + key_size)//2, (HEIGHT - keyMax[1] * key_size + key_size)//2]

doubleClick = 0.2

live_update = True

font = pygame.font.SysFont("Arial", key_size//3, bold = True)
label_font = pygame.font.SysFont("Arial", key_size//2, bold = True)

keys = {}

def check_overlap(key, newPos):
    for other in keys.values():
        if other == key:
            continue
        distanceX = abs(newPos[0] - other.pos[0])
        distanceY = abs(newPos[1] - other.pos[1])
        if distanceX < key.size and distanceY < key.size:
            return True
    return False

class Key:
    def __init__(self, screen, id, pos):
        keys[id] = self
        self.id = id
        self.pos = pos
        self.size = key_size
        self.screen = screen
        self.text = ""
        self.drag = False
        self.selected = False
        self.selectedTime = 0

    def draw(self):
        color = SELECTED_COLOR if self.selected else KEY_COLOR
        rect = pygame.Rect(
            self.pos[0] - self.size // 2,
            self.pos[1] - self.size // 2,
            self.size,
            self.size
        )
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius = border_size
        )
        number = font.render(self.id, True, TEXT_COLOR)
        self.screen.blit(
            number,
            number.get_rect(center=(self.pos[0], self.pos[1] - self.size/3))
        )
        if self.text:
            label = label_font.render(
                self.text,
                True,
                TEXT_COLOR
            )
            self.screen.blit(
                label,
                label.get_rect(center=self.pos)
            )

    def update_pos(self, mousePos):
        if not self.drag:
            return
        self.pos = [mousePos[i] for i in range(2)]
        self.pos = [
                    keyStartPos[i] + round((mousePos[i] - keyStartPos[i]) / snap_size) * snap_size
                    for i in range(2)
                ]
        self.pos = [min(max(self.pos[i], keyStartPos[i] + screen_border + self.size // 2), [WIDTH, HEIGHT][i] - keyStartPos[i] - screen_border - self.size // 2) for i in range(2)]

        if live_update:
            self.find_nearest_valid()

    def find_nearest_valid(self):
        original_pos = list(self.pos)
        step = snap_size

        minX = keyStartPos[0] + screen_border + self.size // 2
        minY = keyStartPos[1] + screen_border + self.size // 2
        maxX = WIDTH - screen_border - self.size // 2
        maxY = HEIGHT - screen_border - self.size // 2

        minGridX = round((minX - keyStartPos[0]) / step)
        minGridY = round((minY - keyStartPos[1]) / step)
        maxGridX = int((maxX - keyStartPos[0]) / step)
        maxGridY = int((maxY - keyStartPos[1]) / step)

        centreX = round((original_pos[0] - keyStartPos[0]) / step)
        centreY = round((original_pos[1] - keyStartPos[1]) / step)

        bestPos = None
        bestDistance = float("inf")

        maxRadius = max(maxGridX - minGridX, maxGridY - minGridY)

        for radius in range(maxRadius + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):

                    if radius > 0 and abs(dx) != radius and abs(dy) != radius:
                        continue

                    gx = centreX + dx
                    gy = centreY + dy

                    if not (minGridX <= gx <= maxGridX):
                        continue
                    if not (minGridY <= gy <= maxGridY):
                        continue

                    candidate = [
                        keyStartPos[0] + gx * step,
                        keyStartPos[1] + gy * step
                    ]

                    if check_overlap(self, candidate):
                        continue

                    distance = (
                        (candidate[0] - original_pos[0]) ** 2 +
                        (candidate[1] - original_pos[1]) ** 2
                    )

                    if distance < bestDistance:
                        bestDistance = distance
                        bestPos = candidate

            if bestPos is not None and bestDistance <= ((radius + 1) * step) ** 2:
                break

        if bestPos is not None:
            self.pos = bestPos
        
    def collision_check(self, pos):
        return all(self.pos[i] - self.size // 2 < pos[i] <  self.pos[i] + self.size // 2 for i in range(2))

    def event(self, event):
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.collision_check(mousePos):
                    curTime = time.time()
                    if curTime - self.selectedTime < doubleClick:
                        self.selected = True
                    else:
                        self.drag = True
                    self.selectedTime = curTime
                else:
                    self.selected = False
                    self.drag = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.drag:
                    self.drag = False
                    if not live_update:
                        self.find_nearest_valid()
        if event.type == pygame.MOUSEMOTION:
            self.update_pos(mousePos)

for i in range(100):
    x = 100 + (i % 10) * 90
    y = 100 + (i // 10) * 90
    Key(screen, str(i), (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        for key in keys:
            keys[key].event(event)
    
    screen.fill(BG_COLOR)
    for key in keys:
        keys[key].draw()
    pygame.display.flip()



pygame.quit()