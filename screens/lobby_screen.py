import pygame
import pygame.freetype
import pygame_gui
import json
from pygame.surface import Surface
from pygame.event import Event

from utility import resolution
from client.networking import Networking
from screens.abc_screen import Screen
from screens.main_screen import MainScreen


class LobbyScreen(Screen):
    def __init__(self, surface: Surface, manager: pygame_gui.UIManager, networking: Networking):
        super().__init__(surface, manager, networking)

        self.screen_width, self.screen_height = resolution()
        WINDOW_SIZE = (self.screen_width, self.screen_height)

        self.background = pygame.Surface(WINDOW_SIZE)
        self.screen = pygame.display.set_mode((WINDOW_SIZE))
        self.screen_width, self.screen_height = WINDOW_SIZE
        self.next_screen = MainScreen

        # 다음 화면으로 전달해야 할 변수
        self.computer_number = 1
        self.user_name = "user"

        # User Name 텍스트 내용 및 크기, 위치
        self.text_username_content = "User Name"
        self.font_username = pygame.font.Font(None, 50)
        self.text_username = self.font_username.render(self.text_username_content, True, (255, 255, 255))
        self.text_username_width, self.text_username_height = self.font_username.size(self.text_username_content)
        self.text_username_x_pos = self.screen_width // 2 - self.text_username_width // 2
        self.text_username_y_pos = self.screen_height * 0.1

        # Computer Player 설명 텍스트 내용 및 크기, 위치
        self.text_complayer_content = "Computer Player"
        self.font_complayer = pygame.font.Font(None, 36)
        self.text_complayer = self.font_complayer.render(self.text_complayer_content, True, (255, 255, 255))
        self.text_complayer_width, self.text_complayer_height = self.font_complayer.size(self.text_complayer_content)
        self.text_complayer_x_pos = self.screen_width // 2 - self.text_complayer_width // 2
        self.text_complayer_y_pos = self.screen_height * 0.4

        # text entry 생성
        self.username_entry_width = 200
        self.username_entry_height = 50
        self.username_entry_x_pos = self.screen_width // 2 - self.username_entry_width // 2
        self.username_entry_y_pos = self.screen_height * 0.2
        self.username_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.username_entry_x_pos, self.username_entry_y_pos), (self.username_entry_width, self.username_entry_height)),
            manager=manager
        )

        # Add Player 버튼 크기 및 위치
        self.add_player_button_count = 5
        self.add_player_button_width = 110
        self.add_player_button_height = 110
        self.add_player_button_spacing = 10 # 버튼의 간격
        self.add_player_button_x_pos = self.screen_width // 2 - ((self.add_player_button_width * (self.add_player_button_count)) + (self.add_player_button_spacing * (self.add_player_button_count - 1))) // 2
        self.add_player_button_y_pos = self.screen_height // 2

        # Add Player 버튼 생성
        self.add_player_button_rects = []
        for i in range(self.add_player_button_count):
            button_rect = pygame.Rect(self.add_player_button_x_pos + i * (self.add_player_button_width + self.add_player_button_spacing), self.add_player_button_y_pos, self.add_player_button_width, self.add_player_button_height)
            self.add_player_button_rects.append(button_rect)

        # 버튼 생성 및 초기화
        self.add_player_buttons = []
        for i in range(self.add_player_button_count):
            button = pygame_gui.elements.UIButton(
                relative_rect=self.add_player_button_rects[i],
                text=str("-"),
                manager=manager
            )
            self.add_player_buttons.append(button)

        # Game Start 버튼 생성
        self.start_add_player_button_width = 270
        self.start_add_player_button_height = 70
        self.start_add_player_button_x_pos = self.screen_width // 2 - self.start_add_player_button_width // 2
        self.start_add_player_button_y_pos = self.screen_height * 0.8
        self.start_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.start_add_player_button_x_pos, self.start_add_player_button_y_pos), (self.start_add_player_button_width, self.start_add_player_button_height)),
                text=str("Game Start"),
                manager=manager
            )

        # Add Player 버튼 상태
        self.selected_index = 0
        self.active_index = 1
        self.button_states = ["inactive", "inactive", "inactive", "inactive", "inactive"]
        self.button_states[self.selected_index] = "selected"
        self.button_states[self.active_index] = "active"

        self.button_index = 0

    def save_player_info_to_json(self):
        player_info = {
            "computer_number": self.computer_number,
            "user_name": self.user_name
        }

        with open('player_info.json', 'w') as outfile:
            json.dump(player_info, outfile)


    # 버튼 상태 업데이트 함수
    def update_add_player_buttons(self):
        for i, button in enumerate(self.add_player_buttons):
            if self.button_states[i] == "selected":
                button.select()
                button.set_text("computer " + str(i + 1))
            elif self.button_states[i] == "active":
                button.unselect()       # 이 부분 코드 살짝 꼼수 ㅜㅜ
                button.enable()
                button.set_text("+")
            else:
                button.disable()
            
    # selected인 버튼의 개수 (computer player 수)
    def selected_number(self):
        count = 0
        for i in range(5):
            if (self.button_states[i] == "selected") :
                count += 1
        self.computer_number  = count
        print(self.computer_number)


    # 이벤트 처리 함수
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for i, button in enumerate(self.add_player_buttons):
                if event.ui_element == button:
                    self.button_index = i
                    self.add_player_button_logic()
                    
            self.update_add_player_buttons()
            self.selected_number()
            if event.ui_element == self.start_button:
                if self.username_entry.get_text() == "" :
                    pass
                else :
                    self.user_name = self.username_entry.get_text()
                    self.save_player_info_to_json()
                print(self.user_name)

                with open("setting_text.txt", "w") as file:
                    file.write(f"computer_number:{self.computer_number}\n")
                    file.write(f"user_name:{self.user_name}\n")
                self.next_screen = MainScreen
                self.is_running = False

                self.next_screen = MainScreen
                self.is_running = False



    # 버튼 로직 함수
    def add_player_button_logic(self):
        # 클릭된 버튼이 active 상태일 경우
        if self.button_states[self.button_index] == "active":
            if self.button_index == len(self.add_player_button_rects) - 1:
                self.button_states[self.active_index] = "selected"
                self.selected_index += 1
            else :
                self.button_states[self.active_index] = "selected"
                self.selected_index += 1
                self.active_index += 1
                self.button_states[self.active_index] = "active"
        # 클릭된 버튼이 inactive 상태일 경우
        elif self.button_states[self.button_index] == "inactive":
            pass
        # 클릭된 버튼이 selected 상태일 경우
        else:
            if self.button_index == 0 :
                pass
            elif self.button_index != self.selected_index:
                pass
            elif self.button_index == len(self.add_player_button_rects) - 1:
                self.button_states[self.selected_index] = "active"
                self.selected_index -= 1
            else:
                self.button_states[self.selected_index] = "active"
                self.button_states[self.active_index] = "inactive"
                self.selected_index -= 1
                self.active_index -= 1

    # run 함수
    def run(self, events: list[Event]) -> bool:
        
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text_username, (self.text_username_x_pos, self.text_username_y_pos))
        self.screen.blit(self.text_complayer, (self.text_complayer_x_pos, self.text_complayer_y_pos))

        for event in events:
            self.handle_event(event)

        self.update_add_player_buttons()

        if self.networking.current_game.is_started:
            self.is_running = False
        return self.is_running