import pygame
import sys



# -- Global Variables --
WHITE = (255,255,255)


# -- Button Class --

class Button:
    def __init__(self, x, y, image, display):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.display = display
        self.clicked = False

    def draw(self):
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def collision(self):
        # -- Get Mouse Pos and check if button clicked --
        pos = pygame.mouse.get_pos()

        # -- Check Clicked Condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


# -- Draw Text Method --

def drawText(text, font, colour, surface, x, y):
    textObj = font.render(text, 1, colour)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


# -- Settings method to be used in main game loop --
def settings(display):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -- Overwrite last screen by setting it to light blue, then update with new display --
        display.fill('lightblue')
        drawText('Settings',pygame.font.SysFont('arial.ttf', 40), WHITE, display, 500, 100)

        # -- Settings Buttons --
        backButton = Button(500, 200, 'startButton.png', display)
        backButton.draw()

        # -- Button Logic --
        if backButton.collision():
            sys.exit()

        pygame.display.update()

