import pygame
import pygame_gui
import pygame.freetype
import json
import sys
from pygame.surface import Surface
from pygame.event import Event
from pygame_gui.elements.ui_button import UIButton

from utility import resolution
from client.networking import Networking
from screens.abc_screen import Screen
# from game_logic import load_achievements
from game_class import *


ob = GameInit()

#업적 로드
# load_achievements(ob)


class Achievement(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)

        self.screen_width, self.screen_height = resolution()
        WINDOW_SIZE = (self.screen_width, self.screen_height)

        self.background = pygame.Surface(WINDOW_SIZE)
        self.screen = pygame.display.set_mode((WINDOW_SIZE))
        self.screen_width, self.screen_height = WINDOW_SIZE
        self.next_screen = None

        self.text_title_content = "Achievement"
        self.font_title = pygame.font.Font(None, 100)
        self.text_title = self.font_title.render(
            self.text_title_content, True, (0, 0, 0))
        self.text_achieve_rect = self.text_title.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 * 0.3))

        self.button_rect = pygame.Rect((self.screen_width // 2 * 1.5, self. screen_height //
                                       2 * 0.6), (self.screen_width // 5, self.screen_height // 15))
        self.achieve1_button = UIButton(
            relative_rect=self.button_rect, text='Stage1', manager=manager)

        self.button_rect2 = pygame.Rect((self.screen_width // 2 * 1.5, self. screen_height //
                                         2 * 0.9), (self.screen_width // 5, self.screen_height // 15))
        self.achieve2_button = UIButton(
            relative_rect=self.button_rect2, text='Stage2', manager=manager)

        self.button_rect3 = pygame.Rect((self.screen_width // 2 * 1.5, self. screen_height //
                                         2 * 1.2), (self.screen_width // 5, self.screen_height // 15))
        self.achieve3_button = UIButton(
            relative_rect=self.button_rect3, text='Stage3', manager=manager)

        self.button_rect4 = pygame.Rect((self.screen_width // 2 * 1.5, self. screen_height //
                                         2 * 1.5), (self.screen_width // 5, self.screen_height // 15))
        self.achieve4_button = UIButton(
            relative_rect=self.button_rect4, text='Stage4', manager=manager)

        self.button_rect5 = pygame.Rect(
            (self.screen_width // 2 * 0.8, self.screen_height // 2 * 1.7), (self.screen_width // 5, self.screen_height // 15))
        self.home_button = UIButton(
            relative_rect=self.button_rect5, text='HOME', manager=manager)

        self.button_rect6 = pygame.Rect(
            (self.screen_width * 0.1, self.screen_height // 2 * 1.7), (self.screen_width // 5, self.screen_height // 15))
        self.before_button = UIButton(
            relative_rect=self.button_rect6, text='BEFORE', manager=manager)

        self.button_rect7 = pygame.Rect(
            (self.screen_width * 0.7, self.screen_height // 2 * 1.7), (self.screen_width // 5, self.screen_height // 15))
        self.next_button = UIButton(
            relative_rect=self.button_rect7, text='Next', manager=manager)

        self.achievements = []  # 업적 정보를 저장할 리스트

    def load_achievements(self):
        with open('achievements.json', 'r') as f:
            self.achievements = json.load(f)

    def draw_achievements(self):
        # 아이콘 크기 설정
        self.icon_width = 40
        self.icon_height = 40

        self.offset_y = self.screen_height // 2 * 0.6
        for achievement in self.achievements:
            self.icon_path = achievement["icon"]
            self.name = achievement["name"]
            self.achieved = achievement["achieved"]
            self.date_achieved = achievement["date_achieved"]

            self.icon = pygame.image.load(self.icon_path)
            self.icon = pygame.transform.scale(
                self.icon, (self.icon_width, self.icon_height))
            self.screen.blit(
                self.icon, (self.screen_width // 2 * 0.5, self.offset_y - 10))

            self.text_offset_x = self.screen_width // 2 * 0.7
            self.text_offset_y = self.offset_y * 1.0

            self.text_name_rect = pygame.Rect(
                (self.text_offset_x, self.text_offset_y), (200, 35))
            pygame.draw.rect(self.screen, (255, 255, 255), self.text_name_rect)

            self.text_achieved_rect = pygame.Rect(
                (self.text_offset_x + 100, self.text_offset_y), (100, 35))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             self.text_achieved_rect)

            self.text_date_rect = pygame.Rect(
                (self.text_offset_x + 200, self.text_offset_y), (150, 35))
            pygame.draw.rect(self.screen, (255, 255, 255), self.text_date_rect)

            self.font = pygame.font.Font(None, 25)
            self.text_name = self.font.render(self.name, True, (0, 0, 0))
            self.screen.blit(self.text_name, self.text_name_rect.topleft)

            self.text_achieved = self.font.render(
                str(self.achieved), True, (0, 0, 0))
            self.screen.blit(self.text_achieved,
                             self.text_achieved_rect.topleft)

            self.text_date = self.font.render(
                self.date_achieved, True, (0, 0, 0))
            self.screen.blit(self.text_date, self.text_date_rect.topleft)

            self.offset_y += 95

    def create_popup(self, manager):
        popup_window = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(
                (self.screen_width//2 * 0.5, self.screen_height//2 * 0.6), (450, 250)),
            manager=manager,
            window_title='Stage 1',
            action_long_desc='You clear the stage 1!',
            action_short_name='OK',
            blocking=True)
        return popup_window

    def create_popup2(self, manager):
        popup_window = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(
                (self.screen_width//2 * 0.5, self.screen_height//2 * 0.6), (450, 250)),
            manager=manager,
            window_title='Stage 2',
            action_long_desc='You clear the stage 2!',
            action_short_name='OK',
            blocking=True)
        return popup_window

    def create_popup3(self, manager):
        popup_window = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(
                (self.screen_width//2 * 0.5, self.screen_height//2 * 0.6), (450, 250)),
            manager=manager,
            window_title='Stage 3',
            action_long_desc='You clear the stage 3!',
            action_short_name='OK',
            blocking=True)
        return popup_window

    def create_popup4(self, manager):
        popup_window = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(
                (self.screen_width//2 * 0.5, self.screen_height//2 * 0.6), (450, 250)),
            manager=manager,
            window_title='Stage 4',
            action_long_desc='You clear the stage 4!',
            action_short_name='OK',
            blocking=True)
        return popup_window

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.achieve1_button:
                    self.popup_window = self.create_popup(self.manager)
                elif event.ui_element == self.achieve2_button:
                    self.popup_window = self.create_popup2(self.manager)
                elif event.ui_element == self.achieve3_button:
                    self.popup_window = self.create_popup3(self.manager)
                elif event.ui_element == self.achieve4_button:
                    self.popup_window = self.create_popup4(self.manager)
                elif event.ui_element == self.home_button:
                    from screens.start_screen import StartScreen
                    self.next_screen = StartScreen
                    self.is_running = False
                elif event.ui_element == self.before_button:
                    pass
                elif event.ui_element == self.next_button:
                    from screens.achievement_screen2 import AchieveScreen2
                    self.next_screen = AchieveScreen2
                    self.is_running = False

    def run(self, events: list[Event]) -> bool:
        self.screen.blit(self.background, (0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.text_title, self.text_achieve_rect)
        self.load_achievements()
        self.draw_achievements()
        for event in events:
            self.handle_events(event)

        if self.networking.current_game.is_started:
            self.is_running = False
        return self.is_running
