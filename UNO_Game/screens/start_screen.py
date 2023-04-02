import pygame
import pygame_gui
import sys


class MainScreen:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = None


basic = MainScreen()
pygame.init()

screen_width = basic.width
screen_height = basic.height

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UNO GAME")

manager = pygame_gui.UIManager((screen_width, screen_height))


def play_mode_function():
    print('Button1 clicked!')


def setting_mode_function():
    print('Button2 clicked!')


def exit_mode_function():
    pygame.quit()
    quit()


button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    basic.width // 2 - 100, basic.height // 2, 200, 50), text='SINGLE PLAY', manager=manager)
button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    basic.width // 2 - 100, basic.height // 2 * 1.3, 200, 50), text='SETTING', manager=manager)
button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    basic.width // 2 - 100, basic.height // 2 * 1.6, 200, 50), text='EXIT', manager=manager)

# button dictionary
button_functions = {button1: play_mode_function,
                    button2: setting_mode_function, button3: exit_mode_function}

# 키보드로 버튼 클릭을 제어하는 객체 생성


class KeyboardController:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_button_index = 0
        self.buttons[self.selected_button_index]._set_active()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_button_index = (
                    self.selected_button_index - 1) % len(self.buttons)
                self.buttons[self.selected_button_index]._set_active()
                self.buttons[(self.selected_button_index + 1) %
                             len(self.buttons)].unselect()
                self.buttons[(self.selected_button_index + 1) %
                             len(self.buttons)].enable()
            elif event.key == pygame.K_DOWN:
                self.selected_button_index = (
                    self.selected_button_index + 1) % len(self.buttons)
                self.buttons[(self.selected_button_index) %
                             len(self.buttons)]._set_active()
                self.buttons[(self.selected_button_index - 1) %
                             len(self.buttons)].unselect()
                self.buttons[(self.selected_button_index - 1) %
                             len(self.buttons)].enable()
            elif event.key == pygame.K_RETURN:
                clicked_button = self.buttons[self.selected_button_index]
                if clicked_button in button_functions.keys():
                    button_functions[clicked_button]()
                elif self.selected_button_index == len(self.buttons) - 1:
                    pygame.quit()
                    sys.exit()

    def draw(self, surface):
        pass


# 키보드로 제어할 버튼 객체 리스트 생성
keyboard_buttons = [button1, button2, button3]

# 키보드 컨트롤러 객체 생성
keyboard_controller = KeyboardController(keyboard_buttons)

# 폰트 설정
font = pygame.font.SysFont(None, 100)

# "UNO" 텍스트 생성
text = font.render("UNO", True, (255, 255, 255))

# 텍스트의 중심 좌표 계산
text_rect = text.get_rect(center=(basic.width//2, basic.height//2 - 100))

# pygame_gui의 UILabel 생성
label = pygame_gui.elements.UILabel(
    relative_rect=text_rect,
    text="",
    manager=manager
)

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        manager.process_events(event)
        keyboard_controller.handle_event(event)

        # 마우스 클릭시 버튼 함수 실행
        if event.type == pygame.MOUSEBUTTONUP:
            for button in button_functions.keys():
                if button.rect.collidepoint(event.pos):
                    button_functions[button]()

    manager.update(1 / 60)
    screen.fill((0, 0, 0))
    keyboard_controller.draw(screen)
    screen.blit(text, text_rect)
    manager.draw_ui(screen)
    pygame.display.flip()
