import pygame
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play
url = "https://www.youtube.com/watch?v=wie68pWg7ss"


youtube = YouTube(url)
audio_stream = youtube.streams.filter(only_audio=True).first()
audio_file = audio_stream.download(output_path='.', filename='aa')

audio = AudioSegment.from_file(audio_file, format="mp4")
audio.export("download", format="mp3")
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("download")


pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing Game")

correct_sound = pygame.mixer.Sound("correct_sound.wav")
correct_sound.set_volume(0.009)

incorrect_sound = pygame.mixer.Sound("incorrect_sound.wav")
incorrect_sound.set_volume(0.1)
word_list = ["python", "programming", "game", "typing", "keyboard"]

def choose_word():
    return random.choice(word_list)

def play_music():
    pygame.mixer.music.play(-1)

def check_input(current_word, input_word):
    if current_word == input_word:
        screen.fill((0, 0, 0))
        return True
    else:
        screen.fill((0, 0, 0))
        return False

def update_score(correct):
    global score
    if correct:
        score += 1
        correct_sound.play()
    else:
        score -= 1
        incorrect_sound.play()

play_music()
last_input_time = time.time()
score = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
input_font = pygame.font.SysFont(None, 24)
game_over = False
last_key_time = pygame.time.get_ticks()
paused = False

while not game_over:
    current_word = choose_word()
    text = font.render(current_word, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 50))
    screen.blit(text, text_rect)

    input_word = ""
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
        
        input_text_surf = input_font.render(input_word, True, (255, 255, 255))
        input_rect = input_text_surf.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.fill((0,0,0), input_rect)
        screen.blit(input_text_surf, input_rect)
        pygame.display.update()

        # Check if it's been more than 2 seconds since the last key press
        if pygame.time.get_ticks() - last_key_time > 2000 and not paused:
            pygame.mixer.music.pause()
            paused = True

    correct = check_input(current_word, input_word)
    update_score(correct)

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()
    
    if not paused:
        pygame.mixer.music.unpause()

pygame.quit()
