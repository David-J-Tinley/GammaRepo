import pygame
import pygame_gui
import pygame.freetype
from SnakeEyes.Code.settings import Settings
import socket
import pickle

class GameWinCLIENT:
    def __init__(self, scene_manager, game, Mult):
        self.Mult = Mult
        self.scene_manager = scene_manager
        self.game = game
        self.screen = self.scene_manager.screen
        self.GAME_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.FONT_SIZE)
        self.HEADER_FONT = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", Settings.HEADER_FONT_SIZE)

        self.pNum = 2
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mwin'

        self.ui_manager = pygame_gui.UIManager((Settings.WIDTH, Settings.HEIGHT), "SnakeEyes/Assets/theme.json") #pygame_gui manager
        self.clock = pygame.time.Clock() #Needed for pygame_gui

        self.make_GUI()

    def make_GUI(self):
        self.button_width = 500
        self.button_height = 70

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((Settings.WIDTH/2)-self.button_width/2, (Settings.HEIGHT)-self.button_height), #Position
                (self.button_width, self.button_height)), #Size
            text='CONTINUE',
            manager=self.ui_manager
        )
    
    ### Runs once when this scene is switched to ###
    def on_scene_enter(self):
        self.scene_manager.play_music("SnakeEyes/Assets/Audio/Music/shopLoop.wav")

        self.sorted_players = sorted(self.game.Players, key=lambda Player: Player.score, reverse=True)

    
    def run(self):
        #self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui
        self.update()
        if self.assigned:
            self.clientProcess()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.scene_manager.quit()

            self.ui_manager.process_events(event) #Update pygame_gui

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.statusFlag = False
                    self.scene_manager.switch_scene('menu')
                # Scene Selection
                if event.key == pygame.K_s:
                    self.scene_manager.switch_scene('pause')
            
            if event.type == pygame.USEREVENT:
                #Check if a button was clicked
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Continue Button
                    if event.ui_element == self.continue_button:
                        self.scene_manager.switch_scene('menu')
                        self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
    '''
    START OF CLIENT FUNCTIONS
    '''

    def clientInit(self, pNum, GC1, GC2):
        self.GC1 = GC1
        self.GC2 = GC2
        self.pNum = pNum
        #self.controllerHandling()
        
        while self.connected == False:
            #print("client")
            self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to connect: "+GC1+".tcp.ngrok.io:"+GC2)
            self.c.connect((GC1+".tcp.ngrok.io",int(GC2)))
            check = self.c.recv(1024).decode()
            if check == "WinConnected":
                print(check)
                self.c.send("Hey Serv from WIN".encode())

                self.connected = True
                self.running = True
                self.assigned = True
    '''
    def controllerHandling(self):
        if self.pNum == 2:
            self.controllerAssignment(self.player, Preferences.BLUE_CONTROLS)

        if self.pNum == 3:
            self.controllerAssignment(self.player, Preferences.YELLOW_CONTROLS)

        if self.pNum == 4:
            self.controllerAssignment(self.player, Preferences.RED_CONTROLS)
    '''
    def clientProcess(self):
        if self.running:
            try:
                #print("Running...")
                game_status = {
                    'pNum': self.pNum,
                    'Scene': self.tempScene
                }
                self.c.send(pickle.dumps(game_status))
                game_state = pickle.loads(self.c.recv(1024))
                self.dataImport(game_state)
                self.time_delta = self.clock.tick(60) / 1000.0 #Needed for pygame_gui

            except EOFError:
                print("WIN End of Connection Client")
                print(self.tempScene)
                self.running = False
                self.scene_manager.switch_scene('menu')
                self.scene_manager.play_sound("SnakeEyes/Assets/Audio/SFX/blipSelect.wav")
                self.scene_manager.multiplayer_destroy()

                self.c.close()
                print("WIN EoC Exiting...")

    def closeConnection(self):
        self.connected = False
        self.running = False
        self.assigned = False
        self.GC1 = ''
        self.GC2 = ''
        self.tempScene = 'mwin'

    def dataImport(self, game_state):
        self.pNum = game_state['pNum']
        self.tempScene = game_state['Scene']
    '''
    END OF CLIENT FUNCTIONS
    '''

    def render(self):
        self.screen.fill(Settings.COLOR_BACKGROUND)

        over_text_rect = self.HEADER_FONT.get_rect("GAME OVER")
        over_text_rect.center = ((Settings.WIDTH / 2), Settings.HEADER_FONT_SIZE)
        self.HEADER_FONT.render_to(self.screen, over_text_rect, "GAME OVER", Settings.COLOR_TEXT)

        #Render pygame_gui
        self.ui_manager.update(self.time_delta)
        self.ui_manager.draw_ui(self.screen)  

        verticalShift = 70
        bottom = Settings.HEIGHT-verticalShift
        spaceBetween = 10
        textPadding = 0.2

        wantedTextSize = 60
        titleTextSize = 22
        scoreTextSize = 50
        crimeTextSize = 25

        winnerWidth = 360
        winnerHeight = 450
        secondScale = (5/6)
        thirdScale = (4/6)
        fourthScale = (3/6)

        pCount = len(self.game.Players)

        #1st place
        if pCount >= 1:
            winner_rect = pygame.Rect((Settings.WIDTH/2)-(winnerWidth/2), (bottom/2)-(winnerHeight/2), #x, y
                            winnerWidth, winnerHeight) #width, height
            pygame.draw.rect(self.screen, (200, 200, 200), winner_rect)

            winner_text = "WANTED"
            currentFontSize = wantedTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_wanted_text_rect = currentFont.get_rect(winner_text)
            winner_wanted_text_rect.midtop = (winner_rect.centerx, winner_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_wanted_text_rect, winner_text, (0, 0, 0))
            
            winner_text = f"CRIMINAL MASTERMIND: P{self.sorted_players[0].playerNum}"
            currentFontSize = titleTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_title_text_rect = currentFont.get_rect(winner_text)
            winner_title_text_rect.midtop = (winner_wanted_text_rect.centerx, winner_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_title_text_rect, winner_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[0].character]["profile"])
            image_size = winnerWidth * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (winner_rect.centerx - (image_size/2), winner_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            winner_text = f"${self.sorted_players[0].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_score_rect = currentFont.get_rect(winner_text)
            winner_score_rect.midbottom = (winner_rect.centerx, winner_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_score_rect, winner_text, (0, 0, 0))
            
            winner_text = "For the Theft of"
            currentFontSize = crimeTextSize
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            winner_crime_rect = currentFont.get_rect(winner_text)
            winner_crime_rect.midbottom = (winner_score_rect.centerx, winner_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, winner_crime_rect, winner_text, (0, 0, 0))
        
        #2nd place
        if pCount >= 2:
            second_rect = pygame.Rect(0, 0, winnerWidth*secondScale, winnerHeight*secondScale) #x, y, width, height
            second_rect.bottomright = (winner_rect.left - spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), second_rect)  

            second_text = "WANTED"
            currentFontSize = wantedTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_wanted_text_rect = currentFont.get_rect(second_text)
            second_wanted_text_rect.midtop = (second_rect.centerx, second_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_wanted_text_rect, second_text, (0, 0, 0))

            second_text = f"BURGLAR: P{self.sorted_players[1].playerNum}"
            currentFontSize = titleTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_title_text_rect = currentFont.get_rect(second_text)
            second_title_text_rect.midtop = (second_wanted_text_rect.centerx, second_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_title_text_rect, second_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[1].character]["profile"])
            image_size = winnerWidth * secondScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (second_rect.centerx - (image_size/2), second_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            second_text = f"${self.sorted_players[1].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_score_rect = currentFont.get_rect(second_text)
            second_score_rect.midbottom = (second_rect.centerx, second_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_score_rect, second_text, (0, 0, 0))
            
            second_text = "For the Theft of"
            currentFontSize = crimeTextSize*secondScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            second_crime_rect = currentFont.get_rect(second_text)
            second_crime_rect.midbottom = (second_score_rect.centerx, second_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, second_crime_rect, second_text, (0, 0, 0))
        
        #3rd place
        if pCount >= 3:
            third_rect = pygame.Rect(0, 0, winnerWidth*thirdScale, winnerHeight*thirdScale) #x, y, width, height
            third_rect.bottomleft = (winner_rect.right + spaceBetween, winner_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), third_rect)  

            third_text = "WANTED"
            currentFontSize = wantedTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_wanted_text_rect = currentFont.get_rect(third_text)
            third_wanted_text_rect.midtop = (third_rect.centerx, third_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_wanted_text_rect, third_text, (0, 0, 0))

            third_text = f"THIEF: P{self.sorted_players[2].playerNum}"
            currentFontSize = titleTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_title_text_rect = currentFont.get_rect(third_text)
            third_title_text_rect.midtop = (third_wanted_text_rect.centerx, third_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_title_text_rect, third_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[2].character]["profile"])
            image_size = winnerWidth * thirdScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (third_rect.centerx - (image_size/2), third_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            third_text = f"${self.sorted_players[2].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_score_rect = currentFont.get_rect(third_text)
            third_score_rect.midbottom = (third_rect.centerx, third_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_score_rect, third_text, (0, 0, 0))
            
            third_text = "For the Theft of"
            currentFontSize = crimeTextSize*thirdScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            third_crime_rect = currentFont.get_rect(third_text)
            third_crime_rect.midbottom = (third_score_rect.centerx, third_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, third_crime_rect, third_text, (0, 0, 0))
        
        #4th place
        if pCount >= 4:
            fourth_rect = pygame.Rect(0, 0, winnerWidth*fourthScale, winnerHeight*fourthScale) #x, y, width, height
            fourth_rect.bottomleft = (third_rect.right + spaceBetween, third_rect.bottom)
            pygame.draw.rect(self.screen, (200, 200, 200), fourth_rect)  

            fourth_text = "WANTED"
            currentFontSize = wantedTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_wanted_text_rect = currentFont.get_rect(fourth_text)
            fourth_wanted_text_rect.midtop = (fourth_rect.centerx, fourth_rect.top + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_wanted_text_rect, fourth_text, (0, 0, 0))

            fourth_text = f"PETTY THIEF: P{self.sorted_players[3].playerNum}"
            currentFontSize = titleTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_title_text_rect = currentFont.get_rect(fourth_text)
            fourth_title_text_rect.midtop = (fourth_wanted_text_rect.centerx, fourth_wanted_text_rect.bottom + (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_title_text_rect, fourth_text, (0, 0, 0))

            image = pygame.image.load(self.game.character_sprites[self.sorted_players[3].character]["profile"])
            image_size = winnerWidth * fourthScale * 0.7
            image = pygame.transform.scale(image, (image_size, image_size))
            image_x, image_y = (fourth_rect.centerx - (image_size/2), fourth_rect.centery - (image_size/2))
            image_back = pygame.Rect(image_x, image_y, image_size, image_size) #x, y,width, height
            pygame.draw.rect(self.screen, (150, 150, 150), image_back)
            self.screen.blit(image, (image_x, image_y))

            fourth_text = f"${self.sorted_players[3].score:,.{Settings.ROUNDING_PRECISION}f}"
            currentFontSize = scoreTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_score_rect = currentFont.get_rect(fourth_text)
            fourth_score_rect.midbottom = (fourth_rect.centerx, fourth_rect.bottom - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_score_rect, fourth_text, (0, 0, 0))
            
            fourth_text = "For the Theft of"
            currentFontSize = crimeTextSize*fourthScale
            currentFont = pygame.freetype.Font("Fonts/HighlandGothicFLF-Bold.ttf", currentFontSize)
            fourth_crime_rect = currentFont.get_rect(fourth_text)
            fourth_crime_rect.midbottom = (fourth_score_rect.centerx, fourth_score_rect.top - (currentFontSize*textPadding))
            currentFont.render_to(self.screen, fourth_crime_rect, fourth_text, (0, 0, 0))


        pygame.display.flip()