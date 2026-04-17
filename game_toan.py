import pygame
import random
import os

# --- CẤU HÌNH HỆ THỐNG ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vở Toán Thông Minh - Bé Vân Lớp 3")

# Màu sắc
WHITE, BLACK, BLUE_GRID = (255, 255, 255), (0, 0, 0), (210, 235, 255)
RED_MARGIN, SUCCESS_GREEN = (255, 200, 200), (34, 139, 34)
HIGHLIGHT_BLUE = (0, 102, 204)

# File lưu kỷ lục
DATA_FILE = "ky_luc.txt"

def load_completed_count():
    """Hàm đọc số bài đã làm từ file txt"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_completed_count(count):
    """Hàm ghi số bài đã làm vào file txt"""
    with open(DATA_FILE, "w") as f:
        f.write(str(count))

def get_font(size):
    for f in ["Tahoma", "Segoe UI", "Arial"]:
        try: return pygame.font.SysFont(f, size, bold=True)
        except: continue
    return pygame.font.Font(None, size)

FONT_BIG = get_font(60)
FONT_MED = get_font(40)
FONT_SMALL = get_font(25)

class InputBox:
    def __init__(self, x, y, w, h, correct_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.correct_val = str(correct_val)
        self.active = False
        self.is_correct = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active and not self.is_correct:
            if event.unicode.isdigit():
                self.text = event.unicode
                if self.text == self.correct_val:
                    self.is_correct = True
                    self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = ""

    def draw(self, screen):
        color = SUCCESS_GREEN if self.is_correct else (HIGHLIGHT_BLUE if self.active else (180, 180, 180))
        pygame.draw.rect(screen, color, self.rect, 2)
        txt = FONT_MED.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 12, self.rect.y + 5))

def generate_question():
    mode = random.choice(["+", "-", "*"])
    if mode == "+":
        a, b = random.randint(1000, 9000), random.randint(1000, 9000)
        result = a + b
    elif mode == "-":
        a, b = random.randint(5000, 9999), random.randint(1000, 4999)
        result = a - b
    else:
        a, b = random.randint(1000, 5000), random.randint(2, 5)
        result = a * b
    
    label = f"{a} {mode} {b}"
    res_str = str(result)
    boxes = []
    start_x = 450
    for i in range(len(res_str)-1, -1, -1):
        boxes.append(InputBox(start_x, 320, 45, 55, res_str[i]))
        start_x -= 50
    return label, boxes

def main():
    label, boxes = generate_question()
    # 1. Đọc số bài cũ từ file khi bắt đầu
    completed_count = load_completed_count() 
    
    running = True
    show_success = False
    timer = 0

    while running:
        screen.fill(WHITE)
        # Vẽ giấy ô ly
        for i in range(0, WIDTH, 40):
            pygame.draw.line(screen, BLUE_GRID, (i, 0), (i, HEIGHT))
            pygame.draw.line(screen, BLUE_GRID, (0, i), (WIDTH, i))
        pygame.draw.line(screen, RED_MARGIN, (100, 0), (100, HEIGHT), 3)

        # Hiển thị bộ đếm (Bảng vàng)
        count_txt = FONT_SMALL.render(f"Bảng vàng của Vân: {completed_count} bài", True, (200, 0, 0))
        screen.blit(count_txt, (450, 20))

        parts = label.split()
        screen.blit(FONT_BIG.render(parts[0], True, BLACK), (300, 180))
        screen.blit(FONT_BIG.render(parts[1], True, BLACK), (230, 220))
        screen.blit(FONT_BIG.render(parts[2], True, BLACK), (300, 240))
        pygame.draw.line(screen, BLACK, (220, 310), (480, 310), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            for box in boxes: box.handle_event(event)

        for box in boxes: box.draw(screen)

        if all(b.is_correct for b in boxes):
            screen.blit(FONT_MED.render("GIỎI QUÁ!", True, SUCCESS_GREEN), (300, 450))
            if not show_success:
                completed_count += 1
                # 2. Lưu ngay vào file khi bé làm xong 1 bài
                save_completed_count(completed_count) 
                show_success = True
                timer = pygame.time.get_ticks()
            
            if pygame.time.get_ticks() - timer > 2000:
                label, boxes = generate_question()
                show_success = False

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()