import pygame
import json
import math
import time

from game_class import *
# from game_logic import *

# 이미지 로드 및 애니메이션을 위한 Card 클래스
class CardLoad:
    def __init__(self, card_value):
        self.screen_width, self.screen_height = resolution()
        self.card_value = card_value    # 카드의 정보 (튜플 값, ("Red", 5) 형식)
        self.image = pygame.image.load(f"assets/images/cards/{self.card_value[0]}_{self.card_value[1]}.png")  # 카드 이미지 로드
        self.image_rect = self.image.get_rect()
        self.background = BackGround()  # BackGround 객체 생성
        self.current_card_pos = self.opendeck_image_pos()  # currentCard(오픈 카드)일 때 이미지 위치
        self.deck_pos = self.deck_image_pos()    # 덱 좌표
        self.speed = 10  # 이동 속도
        self.spacing = 15   # myboard와 카드와의 간격
        self.cards_per_row = 12  # myboard에서 한 줄당 카드의 수
        self.x_interval = self.background.card_pos(self.background.my_board_image.get_rect().size,
                        self.spacing, self.image, self.cards_per_row) # myboard에서 카드끼리의 수평 간격
        self.y_interval = 70 # myboard에서 카드끼리의 수직 간격
        self.position = self.deck_pos  # 현재 position
        self.origin_pos = self.deck_pos
        self.target_pos = self.current_card_pos

        self.click_sound = pygame.mixer.Sound("assets/musics/Mario Jumping Sound.mp3")

        self.set_back_pos()


    def set_back_pos(self) :
        if self.card_value == ("card", "back") :
            self.image_rect.x, self.image_rect.y = self.deck_pos

    # 컴퓨터가 카드 낼 때 함수
    def set_current_pos(self, player_pos) :
        self.origin_pos = player_pos
        self.target_pos = self.current_card_pos

    # 컴퓨터가 카드 받을 때 함수
    def set_player_pos(self, player_pos) :
        self.origin_pos = self.deck_pos
        self.target_pos = player_pos

    # 카드 이미지 로드
    def card_load(self, surface, pos):
        surface.blit(self.image, pos)

    # 카드가 선택되었을 때
    def card_select(self, is_hovered):
        origin_pos1 = self.position
        target_pos1 = [self.position[0], self.position[1] - 5]
        origin_pos2 = [self.position[0], self.position[1] - 5]
        target_pos2 = self.position

        if is_hovered == True :
            self.origin_pos = origin_pos1
            self.target_pos = target_pos1
        elif is_hovered == False :
            self.origin_pos = origin_pos2
            self.target_pos = target_pos2

    
    # 카드 받을 때 좌표
    def card_pop_image(self, card_list):

        self.origin_pos = self.deck_pos
        self.card_count = len(card_list) - 1

        # playerList에 있는 카드에 수에 따라 좌표 계산
        value1 = self.card_count // self.cards_per_row # 몫 0 ~ 2
        y_pos = self.spacing + value1 * self.y_interval + self.background.board_image_size()[1]
        value2 = self.card_count % self.cards_per_row  # 나머지 0 ~ cards_per_row - 1
        x_pos = self.spacing + value2 * self.x_interval

        self.target_pos = [x_pos, y_pos]
        self.position = self.target_pos     # 현재 좌표 설정

        self.image_rect.x, self.image_rect.y = self.position


    # 스왑 카드 받을 때 좌표
    def swap_card_pop_image(self, card_list):

        self.card_count = len(card_list) - 1

        # playerList에 있는 카드에 수에 따라 좌표 계산
        value1 = self.card_count // self.cards_per_row # 몫 0 ~ 2
        y_pos = self.spacing + value1 * self.y_interval + self.background.board_image_size()[1]
        value2 = self.card_count % self.cards_per_row  # 나머지 0 ~ cards_per_row - 1
        x_pos = self.spacing + value2 * self.x_interval

        self.origin_pos = [x_pos, y_pos]
        self.target_pos = [x_pos, y_pos]
        self.position = self.target_pos     # 현재 좌표 설정 
        
        self.image_rect.x, self.image_rect.y = self.position


    # 이미지 애니메이션
    def image_animation(self, surface):

        self.image_rect.x = self.origin_pos[0]
        self.image_rect.y = self.origin_pos[1]

        # 이동할 좌표 간의 거리를 계산
        self.dx = self.target_pos[0] - self.origin_pos[0]
        self.dy = self.target_pos[1] - self.origin_pos[1]
        distance = math.sqrt(self.dx**2 + self.dy**2)  # 두 좌표 사이의 거리

        self.move_x = self.speed * self.dx / distance  # x축 이동 거리
        self.move_y = self.speed * self.dy / distance  # y축 이동 거리

        self.position = self.target_pos # 현재 위치를 target 위치로 설정

        # 부동소수점 때문에 origin_pos가 target_pos가 될 수 없는 문제 해결
        if distance <= self.speed:
            self.origin_pos = self.target_pos
            self.image_rect.x = int(self.origin_pos[0])
            self.image_rect.y = int(self.origin_pos[1])
        else:
            self.origin_pos[0] += self.move_x
            self.origin_pos[1] += self.move_y

            self.image_rect.x = int(self.origin_pos[0])
            self.image_rect.y = int(self.origin_pos[1])

        surface.blit(self.image, self.image_rect)


    # 다 움직이면 더이상 움직이지 않도록 하는 함수
    def animation_control(self, surface) :
        if not self.origin_pos == self.target_pos :
            self.image_animation(surface)
        else :
            self.card_load(surface, self.position)


    # 카드 내는 함수
    def play_card_event(self):
        self.origin_pos = self.position
        self.target_pos = self.current_card_pos
        self.position = self.target_pos


    # deck (unopendeck)의 이미지 좌표 계산
    def deck_image_pos(self):
        x, y = self.background.board_image_size()
        width, height = self.image.get_rect().size
        x_pos = (x  - width) * 0.2
        y_pos = (y - height) * 0.3
        return [x_pos, y_pos]


    # opendeck의 이미지 좌표 계산
    def opendeck_image_pos(self):
        x, y = self.background.board_image_size()
        width, height = self.image.get_rect().size
        return [x // 2 - width // 2, y // 2 - height // 2]


# user (나) 이외의 플레이어 상태를 로드해주는 클래스 (player_num : 플레이어 번호)
class PlayerState:
    def __init__(self, player_num):
        self.player_bg = BackGround()
        self.player_num = player_num
        self.player_name = "컴퓨터 " + str(player_num)
        self.player_pos = [0, 0]
        self.player_pos_change()
        self.player_card_num = 7    # 가지고 있는 카드의 개수
        self.player_cards_per_row = 10    # 한 줄당 카드의 개수
        self.player_spacing = 5
        self.player_image = pygame.image.load("assets/images/cards/card_back_player.png")  
        self.font_path = "assets/fonts/NanumSquare_acB.ttf"
        self.player_name_font = pygame.font.Font(self.font_path, 17)
        self.player_name_text = self.player_name_font.render(self.player_name, True, (0, 0, 0))
        self.player_x_interval = self.player_bg.card_pos(self.player_bg.player_state_image.get_rect().size,
                        self.player_spacing, self.player_image, self.player_cards_per_row) # player_board에서 카드끼리의 수평 간격
        self.player_y_interval = 20
        

    # 플레이어 state 박스의 좌표 구하기 (플레이어 번호에 따라 달라짐)
    def player_pos_change(self):
        x = self.player_bg.x_pos + self.player_bg.state_spacing
        y = self.player_bg.state_spacing
        interval = self.player_bg.player_state_image.get_rect().height + self.player_bg.state_spacing
        self.player_pos = [x, y + (self.player_num - 1) * interval]

    # 플레이어 상태 이미지 로드
    def player_state_draw(self, surface):
        # 플레이어 이름 로드
        text_draw_pos = [self.player_pos[0] + self.player_spacing, self.player_pos[1] + self.player_spacing]
        surface.blit(self.player_name_text, text_draw_pos)    

        # 플레이어의 가장 첫 번째 카드 좌표
        card_draw_pos = [text_draw_pos[0], text_draw_pos[1] + self.player_name_text.get_size()[1] + self.player_spacing]

        # 플레이어 카드 로드
        for i in range (self.player_card_num):
            if (i % self.player_cards_per_row == 0)  & (i > 1):
                card_draw_pos[0] = text_draw_pos[0]
                card_draw_pos[1] += self.player_y_interval
            surface.blit(self.player_image, (card_draw_pos[0] + (i % self.player_cards_per_row) * self.player_x_interval, card_draw_pos[1]))

    # 우노 상태일 때 우노 이미지 로드



# 해상도 값에 따라 게임 배경 이미지를 다르게 설정하는 클래스
class BackGround:
    def __init__(self):
        self.screen_height = resolution()[1]
        self.resolution_type = self.resolution_type()
        self.background_image()
        # 게임 보드 크기
        self.x_pos = self.game_board_image.get_rect().width
        self.y_pos = self.game_board_image.get_rect().height
        self.state_spacing = 10

    # 해상도 타입을 int 타입으로 반환 (이미지 파일 이름 설정 목적)
    def resolution_type(self):
        if resolution()[0] == 640 : 
            return 1
        elif resolution()[0] == 800 :
            return 2
        else : 
            return 3

    def background_image(self):
        self.game_board_image = pygame.image.load(f"assets/images/screens/game_board{self.resolution_type}.png")
        self.my_board_image = pygame.image.load(f"assets/images/screens/my_board{self.resolution_type}.png")
        self.player_board_image = pygame.image.load(f"assets/images/screens/player_board{self.resolution_type}.png")
        self.player_state_image = pygame.image.load(f"assets/images/screens/player_state{self.resolution_type}.png")
    
    # 배경화면 그리기
    def background_draw(self, surface):
        surface.blit(self.game_board_image, (0, 0))
        surface.blit(self.my_board_image, (0, self.y_pos))
        surface.blit(self.player_board_image, (self.x_pos, 0))
        for i in range (5) :
            surface.blit(self.player_state_image,
                (self.x_pos + self.state_spacing, self.state_spacing + i * (self.screen_height - self.state_spacing) // 5))

    # game_board 이미지의 크기를 반환하는 함수
    def board_image_size(self):
        return self.game_board_image.get_rect().size

    # myboard의 크기에 맞춰 안에 들어갈 카드의 좌표를 계산하는 함수
    def card_pos(self, board_size, spacing, card_image, cards_per_row):
        x = board_size[0]
        # first_card_pos = [spacing, y + spacing]
        # last_card_pos = [x - spacing - card_image.get_rect().width, y + spacing]
        dist = x - 2 * spacing - card_image.get_rect().width
        x_interval = dist / (cards_per_row - 1)
        return x_interval


# 해상도 값을 json 파일로부터 불러와 튜플로 반환하는 함수
def resolution():
    with open('display_config.json', 'r') as f:
        config_data = json.load(f)
    return (config_data['resolution']['width'], config_data['resolution']['height'])



# 카드 클릭
def handle_click_card(event, game_init, surface):

    # 카드에 커서를 올렸을 때
    if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
        # for i in range(len(game_init.my_card_list)) :
        #     if game_init.my_card_list[i].image_rect.collidepoint(mouse_pos):
        #         game_init.is_hovered = True
        #         game_init.my_card_list[i].card_select(game_init.is_hovered)
        #     else :
        #         game_init.is_hovered = False
        #         game_init.my_card_list[i].card_select(game_init.is_hovered)
                
    # 카드를 눌렀을 때
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()

        # 카드를 받는 경우
        if game_init.card_back_image.image_rect.collidepoint(mouse_pos):
            game_init.card_back_image.click_sound.play()    # 효과음
            # unopendeck의 카드 객체 생성 후 my_card_list에 추가
            game_init.my_card_list.append(CardLoad(game_init.unopenDeck[-1]))
            game_init.my_card_list[len(game_init.my_card_list)-1].card_pop_image(game_init.my_card_list)    # 좌표 설정
            game_init.isCardPlayed = True
            game_init.PlayedCard = 0

        # 카드를 내는 경우
        else :
            # 겹치는 부분 중복 선택이 되지 않기 위해 가장 위쪽 카드 하나만 선택
            for i in range (len(game_init.my_card_list)-1, -1, -1) :
                if game_init.my_card_list[i].image_rect.collidepoint(mouse_pos):
                    print(str(game_init.my_card_list[i].card_value) + "카드 클릭")
                    for j in range(len(game_init.available)) :
                        if game_init.my_card_list[i].card_value == game_init.available[j] : # 낼 수 있는 카드일 경우
                            game_init.my_card_list[i].click_sound.play()    # 효과음
                            game_init.my_card_list[i].play_card_event()
                            game_init.PlayedCard = j + 1
                            game_init.isCardPlayed = True
                            game_init.open_deck_image_list.append(game_init.my_card_list.pop(i))
                            game_init.current_card_image = game_init.open_deck_image_list[-1]    # current card 이미지에 저장
                            card_pos_change(game_init, surface)  # 뒷 카드 재정렬
                            break  
                    break

# 카드 냈을 때 낸 카드 다음부터 위치 재정렬
def card_pos_change(game_init, surface):
    for i in range(len(game_init.my_card_list)) :
        value1 = i // game_init.my_card_list[i].cards_per_row
        y_pos = game_init.my_card_list[i].spacing + value1 * game_init.my_card_list[i].y_interval + game_init.my_card_list[i].background.board_image_size()[1]
        value2 = i % game_init.my_card_list[i].cards_per_row
        x_pos = game_init.my_card_list[i].spacing + value2 * game_init.my_card_list[i].x_interval

        game_init.my_card_list[i].position = [x_pos, y_pos]
        game_init.my_card_list[i].image_rect.x = x_pos
        game_init.my_card_list[i].image_rect.y = y_pos

        surface.blit(game_init.my_card_list[i].image, game_init.my_card_list[i].position)
        