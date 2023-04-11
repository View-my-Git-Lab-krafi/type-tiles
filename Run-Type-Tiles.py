#pip install pygame pytube pydub

import pygame
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play
pygame.init()
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("correct_sound.wav")
correct_sound.set_volume(0.009)
incorrect_sound = pygame.mixer.Sound("incorrect_sound.wav")
incorrect_sound.set_volume(0.1)
font = pygame.font.SysFont(None, 48)
input_font = pygame.font.SysFont(None, 24)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing Game")
word_list = ["python", "programming", "game", "typing", "keyboard"]
def choose_word():
    return random.choice(word_list)
def play_music():
    youtube = YouTube("https://www.youtube.com/watch?v=wie68pWg7ss")
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(output_path='.', filename='aa')
    audio = AudioSegment.from_file(audio_file, format="mp4")
    audio.export("download", format="mp3")
    pygame.mixer.music.load("download")
    pygame.mixer.music.play(-1)
def check_input(current_word, input_word):
    correct = True
    surface = font.render(current_word, True, (255, 255, 255))
    for i, char in enumerate(current_word):
        if i >= len(input_word) or char != input_word[i]:
            correct = False
            if i < len(input_word):
                surface.blit(input_font.render(input_word[i], True, (255, 0, 0)), (font.size(current_word[:i])[0], 0))
        else:
            surface.blit(input_font.render(char, True, (255, 255, 255)), (font.size(current_word[:i])[0], 0))
    screen.blit(surface, (screen_width/2 - surface.get_width()/2, screen_height/2 - 50))
    return correct


def update_score(correct):
    global score
    if correct:
        score += 1
        correct_sound.play()
        screen.fill((0, 0, 0))
    else:
        score -= 1
        incorrect_sound.play()
        screen.fill((0, 0, 0), input_font)
play_music()
last_input_time = time.time()
score = 0
game_over = False
clock = pygame.time.Clock()
last_key_time = pygame.time.get_ticks()
paused = False
incorrect_input = False
while not game_over:
    current_word = choose_word()
    text = font.render(current_word, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 50))
    screen.blit(text, text_rect)
    input_word = ""
    incorrect_input = False  
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            last_key_time = pygame.time.get_ticks()
            paused = False
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_BACKSPACE:
                input_word = input_word[:-1]
                screen.fill((0,0,0), input_rect)
                pygame.display.update()
            else:
                input_word += event.unicode
        elif event.type == pygame.QUIT:
            game_over = True
            break
        incorrect_input = False  

        for i in range(len(input_word)):
            if i >= len(current_word) or input_word[i] != current_word[i]:
                incorrect_input = True
                break
        if pygame.time.get_ticks() - last_key_time > 2000 and not paused:
            pygame.mixer.music.pause()
            paused = True
        input_text_surf = input_font.render(input_word, True, (255, 0, 0) if incorrect_input else (255, 255, 255))
        input_rect = input_text_surf.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.fill((0,0,0), input_rect)
        screen.blit(input_text_surf, input_rect)
        pygame.display.update()
        if input_word == current_word:
            correct_sound.play()
            score += 1
            break

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    if score < 0:
        game_over = True
        break
    
    if not paused:
        pygame.mixer.music.unpause()

pygame.quit()
