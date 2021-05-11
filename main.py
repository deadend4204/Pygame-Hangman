import sys
import pygame
from pygame import mixer
import random
import math
pygame.init()

# basic data - window size,background etc
height = 768
width = 1024
FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
# change title,logo and background
icon = pygame.image.load('icon.png')
background = pygame.image.load('background.jpg')
pygame.display.set_caption("Hangman")
pygame.display.set_icon(icon)

# sounds
click = mixer.Sound('click.wav')
correct = mixer.Sound('correct.mp3')
oops = mixer.Sound('oops.wav')
game_over = mixer.Sound('game_over.wav')
click.set_volume(0.6)
oops.set_volume(0.6)
correct.set_volume(0.6)
game_over.set_volume(0.6)

# colors
white = (255, 255, 255)
black = (0, 0, 0)

# fonts
font = 'money.ttf'
title = pygame.font.Font(font, 80)
show_title = title.render("Hangman ! ", True, black)
detail = pygame.font.Font(font, 40)
show_detail = detail.render("Guess The Word", True, black)
won = pygame.font.Font(font, 50)
show_won = won.render("Congrats, You won ! ", True, black)
lost = pygame.font.Font(font, 50)
show_lost = won.render("Oops, You lost ! ", True, black)
word_font = pygame.font.Font(font, 40)


# hangman images
hangman = []
for i in range(7):
    image = pygame.image.load("hangman_"+str(i+1)+".png")
    hangman.append(image)

# variables
won = False
lost = False
wrong = 0
words = ['tree', 'mango', 'coding', 'human', 'python', 'java',
         'hangman', 'amazon', 'help', 'cricket', 'dress', 'apology', 'driver', 'ship', 'pilot']
word = words[random.randint(0, len(words)-1)].upper()
display = []
for x in word:
    display.append("_")  # to display _ equal to no of words size
guessed = []

# buttons var
radius = 30
gap = 25
letters = []
startx = round((width-(radius*2 + gap)*9)/2)
starty = 500
A = 65
visible = True
for i in range(26):
    x = startx + gap*2 + ((radius*2 + gap)*(i % 9))
    y = starty + ((i // 9) * (gap + radius * 2))
    letters.append([x, y, chr(A+i), visible])
# font for letter
letter_font = pygame.font.Font(font, 40)

# functions


def show_word(display):
    display_word = []
    for val in display:
        show_word = word_font.render(val, True, black)
        display_word.append(show_word)
    return display_word


def check_word(word, guess):
    if guess in word:
        correct.play()
        for i in range(len(word)):
            if word[i] == guess:
                display[i] = guess
        return True
    else:
        guessed.append(guess)


def show_buttons():
    # draw buttons
    for letter in letters:
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(screen, black, (x, y), radius)
            text = letter_font.render(char, 1, white)
            screen.blit(text, (x - text.get_width()/2, y-text.get_height()/2))


def show_texts(word_list):
    screen.blit(show_title, (width/2-show_title.get_width()/2, 20))
    screen.blit(show_detail, (width/2-50, 180))
    x = 50
    for val in word_list:
        screen.blit(val, (width/2+x, 300))
        x += 50


def display_won():
    for letter in letters:
        letter[3] = False
    screen.blit(show_won, (width/2-show_won.get_width()/2, 500))


def display_lost():
    for letter in letters:
        letter[3] = False
    for i in range(len(word)):
        display[i] = word[i]
    screen.blit(show_lost, (width/2-show_lost.get_width()/2, 500))


print(word)
# main pygame loop
while 1:
    clock.tick(FPS)
    # make screen black
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(hangman[wrong], (width/2-350, height/2-200))
    # all events are here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if visible:
                    distance = math.sqrt((mouseX-x)**2 + (mouseY-y)**2)
                    if distance < radius:
                        letter[3] = False
                        click.play()
                        if not check_word(word, char):  # if wrong guesss
                            wrong += 1
                            oops.play()
                            if wrong == 6:
                                lost = True
                                game_over.play()
                        if "_" not in display:
                            won = True

    if won == True:
        display_won()
    elif lost == True:
        display_lost()
    display_word = show_word(display)
    show_texts(display_word)
    show_buttons()
    pygame.display.update()
