#!/usr/local/bin/python3

from tkinter import *

import pygame as pygame
import random

from button import *
from level import Level
from settings import *
from popup import Window, questionL
# -- Assests from https://kenney.nl/ --

# Pygame setup
pygame.init()

pygame.mixer.music.load('ZachsGameSoundtrack.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.05)

deathNoise = pygame.mixer.Sound('LEGO® Breaking Sound Effect.wav')


screen = pygame.display.set_mode((screen_width, screen_height))
menuScreen = pygame.display.set_mode((screen_width, screen_height))
settingsScreen = pygame.display.set_mode((screen_width, screen_height))
endScreen = pygame.display.set_mode((screen_width, screen_height))
tutorialScreen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level1_map, screen)
running = True
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
cloud = pygame.image.load('background_cloudA.png')
score = 0
player = level.returnPlayer().sprite


def openChest(score):
    global win
    powerup = [1,2,3]
    chests = level.returnChests().sprites()
    player = level.returnPlayer().sprite
    keys = pygame.key.get_pressed()

    # -- Iterate through chests and check conditions --

    for chest in chests:

        if chest.rect.colliderect(player.rect) and keys[pygame.K_e]:
            root = Tk()
            win = Window(root, 'Answer Window', '300x200', questionL[0])
            score += win.returnScore()
            # -- Choose random powerup --
            randomPowerup = random.choice(powerup)
            if randomPowerup == 1:
                player.health += 10
            elif randomPowerup == 2:
                score += 10
            elif randomPowerup == 3:
                score += random.randint(1,100)

    return score



def writehighScore():
    file = open('highscores.txt', 'a')
    file.write(f'\n {str(score)},')


def highScore():
    writehighScore()
    root = Tk()
    win = Window(root, 'Highscore', '200x400', 'Enter Name:')



def updatePlayerHealth():
    if player.health <= 0:
        pygame.mixer.music.stop()
        deathNoise.play()
        deathScreen()
        if deathScreen():
            player.health = 20
    if player.rect.y >= 1000:
        player.health = 0
    else:
        return player.health


def mainGame():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        level.run()


        drawText(f"Health:  {updatePlayerHealth()}", pygame.font.SysFont('arial.ttf', 40), BLACK, screen, 10, 10)
        global score
        score = openChest(score)
        drawText(f'Score:  {score}', pygame.font.SysFont('arial.ttf', 40), BLACK, screen, 250, 10)

        pygame.display.update()
        clock.tick(70)


def tutorial():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

         # -- Screen Setup --
        pygame.display.set_caption("Marcel's Maths Adventure")

        # -- Screen Gui--
        endScreen.fill('lightblue')
        tutorial = pygame.image.load('tutorial.png')
        endScreen.blit(tutorial, (0,0))

        # -- Button --
        startButton = Button(500, 700, 'startButton.png', menuScreen)
        startButton.draw()

        # -- Button collision --
        if startButton.collision():
            mainGame()


        pygame.display.update()


def menu():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -- Screen Setup --
        pygame.display.set_caption("Marcel's Maths Adventure")

        # -- Main Menu Gui--
        menuScreen.fill('lightblue')
        drawText("Marcel's Maths Adventure", pygame.font.SysFont('arial.ttf', 40), WHITE, menuScreen, 450, 100)
        drawText("Start", pygame.font.SysFont('arial.ttf', 20), WHITE, menuScreen, 500, 200)
        startButton = Button(500, 200, 'startButton.png', menuScreen)
        startButton.draw()
        settingsButton = Button(500, 300, 'settingsButton.png', menuScreen)
        settingsButton.draw()
        quitButton = Button(500, 500, 'quitButton.png', menuScreen)
        quitButton.draw()
        tutorialButton = Button(500, 400, 'tutorialButton.png', menuScreen)
        tutorialButton.draw()


        # -- Mouse Collision --
        if startButton.collision():
            mainGame()

        elif quitButton.collision():
            pygame.quit()
            sys.exit()

        elif settingsButton.collision():
            settings(settingsScreen)

        elif tutorialButton.collision():
            tutorial()


        pygame.display.update()
        clock.tick(60)


def deathScreen():

    while True:
        player = level.returnPlayer().sprite
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -- Screen Setup --
        pygame.display.set_caption("Marcel's Maths Adventure")

        # -- End Screen Gui--
        endScreen.fill('lightblue')

        # -- Post Death Text --
        drawText("You died.", pygame.font.SysFont('arial.ttf', 40), WHITE, endScreen, 530, 100)
        exitButton = Button(500, 300, 'quitButton.png', endScreen)
        exitButton.draw()
        highScoreButton = Button(500, 200, 'highScoreButton.png', endScreen)
        highScoreButton.draw()

        if highScoreButton.collision():
            highScore()

        elif exitButton.collision():
            sys.exit()

        pygame.display.update()
        clock.tick(60)



if __name__ == '__main__':
    menu()
