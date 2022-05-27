import pygame
from settings import *

pygame.mixer.init()

def soundEffect(game, event):
    if game.sound_type == 'meme':
        if event == 'paddleCollide':
            snd1 = pygame.mixer.Sound('Pong\SoundEffects\Vine Boom.wav')
            snd1.set_volume(.2)
            snd1.play()
        elif event == 'wallCollide':
            snd2 = pygame.mixer.Sound('Pong\SoundEffects\Bruh.wav')
            # snd2.set_volume(.3)
            snd2.play()
        elif event == 'playerScore':
            snd3 = pygame.mixer.Sound('Pong\SoundEffects\YAWN.wav')
            snd3.set_volume(.4)
            snd3.play()
        elif event == 'aiScore':
            snd4 = pygame.mixer.Sound('Pong\SoundEffects\AUGH.wav')
            snd4.set_volume(.3)
            snd4.play()
        elif event == 'aiWin':
            snd5 = pygame.mixer.Sound('Pong\SoundEffects\AUGH.wav')
            snd5.set_volume(.2)
            snd5.play()
        elif event == 'playerWin':
            snd6 = pygame.mixer.Sound('Pong\SoundEffects\Yawn.wav')
            snd6.set_volume(.3)
            snd6.play()
        elif event == 'passHighScore':
            snd7 = pygame.mixer.Sound('Pong\SoundEffects\\AUGH.wav')
            snd7.set_volume(.1)
            snd7.play()

    elif game.sound_type == 'normal':
        if event == 'paddleCollide' or event == 'wallCollide':
            snd1 = pygame.mixer.Sound('Pong\SoundEffects\\reflectSound.wav')
            snd1.set_volume(.2)
            snd1.play()
        elif event == 'playerScore' or event == 'aiScore':
            snd2 = pygame.mixer.Sound('Pong\SoundEffects\\scoreSound.wav')
            snd2.set_volume(.3)
            snd2.play()
        elif event == 'aiWin':
            snd3 = pygame.mixer.Sound('Pong\SoundEffects\\defeatSound.wav')
            snd3.set_volume(.3)
            snd3.play()
        elif event == 'playerWin':
            snd4 = pygame.mixer.Sound('Pong\SoundEffects\\winSound.wav')
            snd4.set_volume(.3)
            snd4.play()
        elif event == 'passHighScore':
            snd5 = pygame.mixer.Sound('Pong\SoundEffects\\passHighScore.wav')
            snd5.set_volume(.3)
            snd5.play()

    else:
        pass