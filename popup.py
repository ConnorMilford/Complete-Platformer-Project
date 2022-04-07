import random
from tkinter import *
from level import Level
import pygame
from settings import *

screen = pygame.display.set_mode((screen_width, screen_height))
level = Level(level1_map, screen)

def getQuestions():
    # -- random choice from line in text file --
    questionsFile = open("questions.txt").read().splitlines()
    question = random.choice(questionsFile)
    # -- Split line at ',' separate answer from question --
    questions = question.split(',')
    questions = [i.strip() for i in questions]
    return questions

questionL = getQuestions()


class Window():

    def __init__(self, root, title, geometry, message):
        self.score = 0
        self.yay = pygame.mixer.Sound('Grunt Birthday Party Sound.wav')
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        Label(self.root, text=message).pack()
        self.entry1 = Entry(self.root)
        self.entry1.pack()
        self.button1 = Button(self.root, text='Submit', command=self.getScore).pack()
        self.root.mainloop()



    def getScore(self):
        score = self.score
        # -- if input == answer increase score
        if str(self.entry1.get()).lower() == str(questionL[1]).lower():
            self.yay.play()
            self.score += 50
            self.root.destroy()
            highscore = random.randint(1,3)
            if highscore == '1':
                return 1

            return self.score
        else:
            # -- open file and append score and name to it after death
            file = open('highscores.txt', 'a')
            file.write(f' {self.entry1.get()}')
            file.close()
            self.updateHighscores()
            self.displayHighscores()


    def returnScore(self):
        score = self.score
        print(self.score)
        return score

    def updateHighscores(self):
        # -- open, read, and sort highscores from largest to smallest --
        highscores = open("highscores.txt").read().splitlines()
        highscores = [i for i in highscores]
        highscores.sort()
        highscores.reverse()
        print(highscores)
        return highscores

    def displayHighscores(self):
        # -- iterate through highscores and add a label representing each to gui --
        highscores = self.updateHighscores()
        for score in highscores:
            Label(self.root, text=score).pack()


























