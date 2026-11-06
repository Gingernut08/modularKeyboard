import pygame, json, tkinter
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

font = pygame.font.SysFont("Arial", key_size//3, bold = True)
label_font = pygame.font.SysFont("Arial", key_size//2, bold = True)

keys = {}

class Key:
    def __init__(self, screen, id, pos):
        keys[id] = self
        self.id = id
        self.pos = pos
        self.size = key_size
        self.screen = screen
        self.text = "Q"
        self.selected = False
    
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



testKey = Key(screen, "001", (100, 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill(BG_COLOR)
    for key in keys:
        keys[key].draw()
    pygame.display.flip()



pygame.quit()