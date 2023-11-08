import sys
import pygame
import pygame_gui
import os
import json

import pygame.freetype

from pygame.surface import Surface
from pygame.event import Event

from client.networking import Networking
from screens.abc_screen import Screen
# from screens.main_screen import MainScreen
from screens.start_screen import StartScreen
from screens.main_screen import MainScreen
from screens.volume_screen import VolumeScreen
from screens.lobby_screen import LobbyScreen
from screens.setting_screen import SettingScreen
from screens.keysetting_screen import KeyScreen
from screens.map_screen import MapScreen
from screens.client_lobby import ClientLobby
from tmp_game_screen import GameScreen
from network_client import Client
from network_server import Server
from screens.achievement_screen import Achievement
from screens.achievement_screen2 import AchieveScreen2
from screens.character_screen import CharacterScreen
# from chatgpt import CharacterScreen


from utilities.image_utility import load_image
from utilities.text_utility import truncate

# from button import *


# pygame 초기화
pygame.init()

# json 파일이 존재하지 않을 경우 디폴트 화면 크기 지정
if os.path.isfile('display_config.json'):
    with open('display_config.json', 'r') as f:
        config_data = json.load(f)
    screen_width = config_data['resolution']['width']
    screen_height = config_data['resolution']['height']
else:
    screen_width = 800
    screen_height = 600
    data = {"resolution": {"width": screen_width, "height": screen_height}}
    data["resolution"]["width"] = screen_width
    data["resolution"]["height"] = screen_height
    with open('display_config.json', 'w') as f:
        json.dump(data, f)

# 윈도우 사이즈 지정
WINDOW_SIZE = (screen_width, screen_height)

# 화면 생성
screen = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.Surface(WINDOW_SIZE)

volume_file = 'volume_setting.json'

if os.path.isfile(volume_file):
    with open(volume_file, 'r') as f:
        volume_data = json.load(f)

bgm_volume = (volume_data["slider1_value"] *
              volume_data["slider2_value"] / 100.0)

# 배경음악 생성
pygame.mixer.init()
pygame.mixer.music.load("assets/musics/SellBuyMusic - 뒤뚱뒤뚱.mp3")
pygame.mixer.music.set_volume(bgm_volume)
pygame.mixer.music.play()

# UI manager 생성
manager = pygame_gui.UIManager(WINDOW_SIZE)

FETCH_RATE = 30  # : Networking 객체로부터 게임 상태를 가져오는 주기를 정의하는 변수 선언
SERVER_IP = '127.0.0.1'  # 서버의 IP 주소를 설정 (localhost)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    networking = Networking()  # SERVER_IP 인자 제외

    pygame.display.set_caption('PyUnoGame')

    running = True
    fps = 120
    clock = pygame.time.Clock()

    current_screen = StartScreen(screen, manager, networking)

    # 인증 부분
    '''
    if start_auth:
        networking.login(*start_auth) # Networking 객체를 이용하여 사용자 인증을 진행한다.
        current_screen.is_running = False
    '''

    # fetched_ticks = 0 #  networking.fetch() 함수가 호출될 때마다 카운트를 올리고, FETCH_RATE 만큼 되면 networking.fetch() 함수를 호출
    while running:
        '''
        if fetched_ticks == FETCH_RATE:
            fetched_ticks = 0
            networking.fetch()
        fetched_ticks += 1
        '''
        time_delta = clock.tick(fps) / 1000.0  # 시간 경과를 계산합니다.
        events = []

        for event in pygame.event.get():  # 발생한 모든 이벤트를 가져와서 처리합니다.
            if event.type == pygame.QUIT:  # 창을 닫기 버튼을 눌렀을 경우, 게임을 종료합니다.
                running = False
            else:  # 이외의 이벤트가 발생한 경우, events 리스트에 추가합니다.
                events.append(event)
            manager.process_events(event)

        manager.update(time_delta)
        # 현재 화면에 'run' 메서드가 있다면, current_screen.run(events) 함수를 호출하여 화면을 업데이트합니다.
        if hasattr(current_screen, 'run'):
            # run' 메서드가 False를 반환한다면, 다음 화면으로 전환합니다.
            if not current_screen.run(events):
                manager.clear_and_reset()   # 이부분 위로 올림 (스크린 객체생성보다 아래로 가면 버튼 객체 지워버림)
                # 현재 화면의 다음 화면을 가져옵니다.
                current_screen = current_screen.next_screen(
                    screen, manager, networking)

        else:
            terminate()

        manager.draw_ui(screen)
        pygame.display.flip()

    terminate()


if __name__ == '__main__':  # 스크립트가 직접 실행될 때, main() 함수를 실행합니다.
    if len(sys.argv) > 1:  # 스크립트가 실행될 때 전달된 인자가 있는지 확인합니다.
        # 전달된 인자가 있다면, main() 함수를 인자와 함께 실행합니다.
        main((sys.argv[1], sys.argv[2]))
    else:  # 전달된 인자가 없다면, main() 함수를 인자 없이 실행합니다.
        main()
