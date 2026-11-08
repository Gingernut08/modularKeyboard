import pygame, json, tkinter, time, os, serial
from tkinter import filedialog, messagebox

WIDTH, HEIGHT = 1920, 1080

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


BG_COLOR = (20, 20, 20)
KEY_COLOR = (200, 200, 200)
DRAG_COLOR = (200, 220, 200)
SELECTED_COLOR = (100, 170, 255)
EDIT_COLOR = (255, 170, 100)
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
key_selected = False
remove_assign = False

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves", "autosave_layout.json")

font = pygame.font.SysFont("Arial", key_size//3, bold = True)

keys = {}
items = []

def create_buttons():
    button(screen, [100, 100], [500, 100], "DELETE_ASSIGNMENT", clear_button, KEY_COLOR, (255, 120, 100))
    button(screen, [100, 250], [225, 100], "LOAD_PRESET", load_button, KEY_COLOR, (120, 200, 100))
    button(screen, [375, 250], [225, 100], "SAVE_PRESET", save_button, KEY_COLOR, (120, 200, 100))
    button(screen, [650, 100], [400, 250], "UPLOAD", upload_assignment, KEY_COLOR, (120, 200, 100))

def upload_assignment(button=None, **kwargs):
    if button:
        button.selected = True
        button.draw()
        pygame.display.flip()

    SERIAL_PORT = "COM3"
    BAUD_RATE = 115200

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=3) as esp:
            time.sleep(2)
            esp.reset_input_buffer()

            esp.write(b"BEGIN\n")

            for key_id, key in keys.items():
                assignment = key.text.lower()

                if "," in assignment or "\n" in assignment:
                    raise ValueError(
                        f"Invalid assignment for key {key_id}"
                    )

                esp.write(
                    f"SET,{key_id},{assignment}\n".encode("utf-8")
                )

            esp.write(b"COMMIT\n")
            esp.flush()

            response = esp.readline().decode(
                "utf-8", errors="replace"
            ).strip()

            if response == "OK":
                messagebox.showinfo(
                    "Upload Complete",
                    "Keyboard layout uploaded successfully."
                )
            else:
                messagebox.showerror(
                    "Upload Failed",
                    f"ESP32 response: {response or 'No response'}"
                )

    except Exception as e:
        print(f"Upload error: {e}")
        messagebox.showerror("Upload Error", str(e))

    finally:
        if button:
            button.selected = False
            button.draw()
            pygame.display.flip()

def clear_button(button = None, **kwargs):
    global remove_assign
    button.selected = not button.selected
    if button.selected:
        remove_assign = True
    else:
        remove_assign = False

def save_button(button = None, **kwargs):
    button.selected = True
    button.draw()
    pygame.display.flip()
    
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    file_path = filedialog.asksaveasfilename(
        title = "Save Keytboard Layout",
        filetypes = [
            ("JSON Files", "*.json"),
            ("ALL Files", "*.*")
        ]
    )
    
    root.destroy()
    
    if file_path:
        save_state(file_path)
    
    button.selected = False
    button.draw()
    pygame.display.flip()

def load_button(button = None, **kwargs):
    button.selected = True
    button.draw()
    pygame.display.flip()
    root =  tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    file_path = filedialog.askopenfilename(
        title = "Open Keyboard Layout",
        filetypes = [
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ]
    )
    
    root.destroy()
    
    if file_path:
        keys.clear()
        items.clear()
        load_state(file_path)
        create_buttons()

    button.selected = False
    button.draw()
    pygame.display.flip()


def save_state(filePath = SAVE_FILE):
    data = {
        "settings": {
            "key_size": key_size,
            "snap_grid": snap_grid,
            "screen_border": screen_border,
            "live_update": live_update
        },
        "keys": {
            key.id: {
                "pos": key.pos,
                "text": key.text,
                "size": key.size
            }
            for key in keys.values()
        }
    }
    with open(filePath, "w") as file:
        json.dump(data, file, indent=4)

def load_state(filePath = SAVE_FILE):
    global key_size, snap_grid, screen_border, live_update
    
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
        
        settings = data.get("settings", {})
        key_size = settings.get("key_size",key_size)
        snap_grid = settings.get("snap_grid", snap_grid)
        screen_border = settings.get("screen_border", screen_border)
        live_update = settings.get("live_update", live_update)


        for key_id, state in data["keys"].items():
            key = Key(screen, key_id, state.get("pos", [100, 100]))
            key.size = state.get("size", [key_size, key_size])
            key.text = state.get("text", "")
    except FileNotFoundError:
        pass

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Could not load keyboard layout.")

def check_overlap(key, newPos):
    for other in items:
        if other == key:
            continue
        distanceX = abs(newPos[0] - other.pos[0])
        distanceY = abs(newPos[1] - other.pos[1])
        if distanceX < (key.size[0] + other.size[0]) / 2 and \
            distanceY < (key.size[1] + other.size[1]) / 2:
            return True
    return False

class button:
    def __init__(self, screen, pos, size, label, func, color, altColor):
        items.append(self)
        self.id = id
        self.pos = list(pos)
        self.size = list(size)
        self.screen = screen
        self.text = label
        self.selected = False
        self.function = func
        self.color = color
        self.altColor = altColor

    def collision_check(self, pos):
        return all(self.pos[i] < pos[i] <  self.pos[i] + self.size[i] for i in range(2))

    def event(self, event):
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.collision_check(mousePos):
                    self.function(button = self)

    def draw(self):
        color = self.altColor if self.selected else self.color
        rect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius = min(self.size) // 8
        )
        if self.text:
            font_size = self.size[0] // 2
            while font_size > 5:
                label_font = pygame.font.SysFont("Arial", font_size, bold=True)
                text_width, text_height = label_font.size(self.text)
                
                if text_width <= self.size[0] - 10 and text_height <= self.size[1] - 1:
                    break
                
                font_size -= 1

            label = label_font.render(
                self.text,
                True,
                TEXT_COLOR
            )
            self.screen.blit(
                label,
                label.get_rect(center=[self.pos[i] + self.size[i] // 2 for i in range(2)])
            )
class Key:
    def __init__(self, screen, id, pos):
        keys[id] = self
        items.append(self)
        self.id = id
        self.pos = list(pos)
        self.size = [key_size, key_size]
        self.screen = screen
        self.text = ""
        self.drag = False
        self.selected = False
        self.edit = False
        self.selectedTime = 0

    def draw(self):
        color = SELECTED_COLOR if self.selected else DRAG_COLOR if self.drag else EDIT_COLOR if self.edit else KEY_COLOR
        mult = 0.9
        offset = 1
        rect = pygame.Rect(
            self.pos[0] - self.size[0] // 2,
            self.pos[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius = border_size
        )
        pygame.draw.rect(
            self.screen,
            [color[0] * mult, color[1] * mult, color[2] * mult],
            [rect[0] + offset, rect[1] + offset, self.size[0] - 2 * offset, self.size[1] - 2 * offset],
            border_radius = border_size - offset,
            width = 3
        )
        number = font.render(self.id, True, TEXT_COLOR)
        self.screen.blit(
            number,
            number.get_rect(center=(self.pos[0], self.pos[1] - 9 * self.size[1] / 28))
        )
        
        if self.text:
            font_size = self.size[0] // 2
            while font_size > 5:
                label_font = pygame.font.SysFont("Arial", font_size, bold=True)
                text_width, text_height = label_font.size(self.text)
                
                if text_width <= self.size[0] - 10 and text_height <= self.size[1] - 1:
                    break
                
                font_size -= 1

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
        self.pos = [min(max(self.pos[i], keyStartPos[i] + screen_border + self.size[i] // 2), [WIDTH, HEIGHT][i] - keyStartPos[i] - screen_border - self.size[i] // 2) for i in range(2)]

        if live_update:
            self.find_nearest_valid()

    def find_nearest_valid(self):
        original_pos = list(self.pos)
        step = snap_size

        minX = keyStartPos[0] + screen_border + self.size[0] // 2
        minY = keyStartPos[1] + screen_border + self.size[1] // 2
        maxX = WIDTH - screen_border - self.size[0] // 2
        maxY = HEIGHT - screen_border - self.size[1] // 2

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
        return all(self.pos[i] - self.size[i] // 2 < pos[i] <  self.pos[i] + self.size[i] // 2 for i in range(2))

    def event(self, event):
        global key_selected
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if self.selected:
                self.text = pygame.key.name(event.key).upper()
            if self.edit:
                if event.key == pygame.K_UP:
                    self.size[1] += key_size // 4
                if event.key == pygame.K_DOWN:
                    self.size[1] = max(self.size[1] - key_size // 4, key_size)
                if event.key == pygame.K_RIGHT:
                    self.size[0] += key_size // 4
                if event.key == pygame.K_LEFT:
                    self.size[0] = max(self.size[0] - key_size // 4, key_size)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.edit = False
            self.selected = False
            if event.button == 1:
                if self.collision_check(mousePos):
                    if remove_assign:
                        self.text = ""
                        return
                    curTime = time.time()
                    if curTime - self.selectedTime < doubleClick:
                        self.selected = True
                    else:
                        self.drag = True
                    self.selectedTime = curTime
                else:
                    self.selected = False
                    self.drag = False
            if event.button == 3:
                if self.collision_check(mousePos):
                    self.edit = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.drag:
                    self.drag = False
                    if not live_update:
                        self.find_nearest_valid()
        if event.type == pygame.MOUSEMOTION:
            self.update_pos(mousePos)
        if self.selected:
            key_selected = True

load_state(SAVE_FILE)

create_buttons()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not key_selected:
                    running = False
            if event.key == pygame.K_RETURN:
                if not key_selected:
                    Key(screen, str(len(keys) + 1), (100, 100))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                save_state(SAVE_FILE)
        key_selected = False
        for item in items:
            item.event(event)
    
    screen.fill(BG_COLOR)
    for item in items:
        item.draw()
    pygame.display.flip()

save_state(SAVE_FILE)

pygame.quit()