# Player 클래스 분리 아직 안한 버전

import pygame


class GameInit(object):
    def __init__(self):
        # 모든 플레이어의 보유 카드 정보 (최대 6명)
        self.playerList = [[], [], [], [], [], []]
        self.unopenDeck = list()                                # 카드 더미
        self.openDeck = list()                                  # 오픈된 카드 더미
        self.currentCard = tuple()                              # openDeck의 가장 위 카드
        self.cardColor = ['Blue', 'Red', 'Green', 'Yellow']     # 카드 색깔 종류
        self.available = []     # 가지고 있는 덱에서 낼 수 있는 카드 집합

        # 이미지 관련 변수
        self.my_card_list = []              # 내 카드 이미지 리스트
        self.card_back_image = object       # 카드덱
        self.current_card_image = object
        self.open_deck_image_list = []           # 오픈덱 이미지 리스트
        self.is_ani_complete = False
        self.player_deck_image_list = []         # 플레이어 이미지 객체 리스트

        self.numPlayers = 0     # 플레이어의 수
        self.playerName = ""    # 유저 이름
        self.playerTurn = 0     # 현재 턴은 몇번째 턴?
        self.myTurn = 0         # 내턴은 몇번째인지 저장
        self.nextTurn = 0       # 다음턴은 몇번째 플레이어인가?
        self.doubleWild = 0     # Wild가 중복으로 나오는 경우 방지 이전 색깔 저장 변수
        self.isUNO = False      # 우노 플래그
        
        self.playDirection = 1          # 게임 진행 방향
        self.currentPlayerIndex = -1    # 현재 턴인 플레이어의 인덱스

        self.isCardDrawn = False        # 카드 뽑았는지 여부
        self.isCardPlayed = False       # 카드 냈는지 여부
        self.PlayedCard = 0             # 몇 번째 카드를 냈는가?
        self.isUnChecked0 = True        # 다음 코드를 확인하였는가? (한 번만 실행되어야 하는 코드)
        self.isUnChecked = True         
        self.isUnChecked2 = True
        self.isUnChecked3 = True

        self.alertDelay = 0             # 팝업 몇초간 띄우기
        self.alertType = None           # 팝업 종류
        self.colorDelay = False         # AI가 색깔을 선택하는데 기다리는 시간 설정
        self.isAIPlayed = False

        # 콘솔 출력용
        self.A = 0

        self.delay = 0
        self.isPaused = False           # 게임 중단 (세팅 버튼)

        self.currentPopup = None
        self.selectedColor = None       # 어떤 색깔을 선택하였는가?
        self.isColorChanged = False     # 색깔 선택을 해서 바뀌었는가? (이미지 로드용)
        self.IsChallenge = None         # 챌린지를 했는가? (0 : 챌린지, 1 : 포기)
        self.IsSwap = None              # 스왑을 하는가? (T/F)
        self.swapNumber = None          # 스왑 할 번호

        self.Draw2Attack = False        # Draw2 공격이 진행중인가?
        self.Draw2Count = 0             # Draw2 공격이 몇번 중첩되었는가?
        self.turnCount = 1              # 게임이 시작된 이래로 몇번씩 주고받았는가?

        self.isGameEnd = False  # 게임이 끝났는가?
        self.winner = 0         #승리자 저장 변수
        self.score = []         #점수 저장 변수
        
        self.smartAi = False    #지역A의 똑똑한 AI인가?

        self.achievements = []
        self.teckCount = 0
        
        self.achievements = []  #업적 저장 변수
        self.techCount = 0      #기술 카드가 몇번 사용되었는가? (업적)


        self.running = True
        
        # 업적 부분




        
'''class Player:
    def __init__(self, name):
        self.deck = []
        self.name = name
        '''
