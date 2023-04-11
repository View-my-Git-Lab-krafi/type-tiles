#pip install pygame pytube pydub


ytlink = "https://www.youtube.com/watch?v=MhQKe-aERsU"
screen_width = 1280
screen_height = 720

remove_special_chars = True


#################################################################################################################
from youtube_transcript_api import YouTubeTranscriptApi
import re
import pygame
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play
import time


pygame.init()
pygame.mixer.init()

correct_sound = pygame.mixer.Sound("correct_sound.wav")
correct_sound.set_volume(0.009)
incorrect_sound = pygame.mixer.Sound("incorrect_sound.wav")
incorrect_sound.set_volume(0.1)
font = pygame.font.SysFont(None, 52)
input_font = pygame.font.SysFont(None, 48)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing Game")
link = ytlink
video_id = re.findall(r'watch\?v=(\S+)', link)[0]
try:
    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
except:
    srt = YouTubeTranscriptApi.get_transcript(video_id)
subtitles_list = []
for line in srt:
    subtitles_list.append(line["text"])
subtitles_text = ", ".join(subtitles_list)
with open('sub.txt', 'w') as file:
    file.write(subtitles_text.strip())

word_list = [subtitles_text]
word_list = subtitles_text.split(", ")
print("a")
print("as")

if remove_special_chars:
    word_list = [re.sub(r'[^\w\s]', "", word) for word in word_list]
print("a")
print("as")
print(word_list)
lp = 0
clock = pygame.time.Clock()
last_key_time = pygame.time.get_ticks()
start_time = None
def calculate_wpm(time_elapsed, text_length):
    minutes = time_elapsed / 60
    wpm = text_length / 5 / minutes
    return int(wpm)

def choose_word():
    global lp
    tt=(word_list[lp])
    lp += 1
    if lp >= len(word_list):
       lp = 0
    return tt


def play_music():
    youtube = YouTube(ytlink)
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(output_path='.', filename='aa')
    audio = AudioSegment.from_file(audio_file, format="mp4")
    audio.export("download", format="mp3")
    pygame.mixer.music.load("download")
    pygame.mixer.music.play(-1)
def check_input(current_word, input_word):
    correct = True
    surface = font.render(current_word, True, (80, 250, 123))
    for i, char in enumerate(current_word):
        if i >= len(input_word) or char != input_word[i]:
            correct = False
            if i < len(input_word):
                surface.blit(input_font.render(input_word[i], True,(255, 85, 85)), (font.size(current_word[:i])[0], 0))
        else:
            surface.blit(input_font.render(char, True, (80, 250, 123)), (font.size(current_word[:i])[0], 0))
    screen.blit(surface, (screen_width/2 - surface.get_width()/2, screen_height/2 - 50))
    return correct


def update_score(correct):
    global score
    if correct:
        score += 1
        correct_sound.play()
        screen.fill((68, 71, 90))
    else:
        score -= 1
        incorrect_sound.play()
        screen.fill((68, 71, 90), input_font)
play_music()
last_input_time = time.time()
score = 0
game_over = False
clock = pygame.time.Clock()
last_key_time = pygame.time.get_ticks()
paused = False
incorrect_input = False
first_time = True
while not game_over:
    if first_time == True:
        screen.fill((68, 71, 90))
        font = pygame.font.SysFont(None, 48)
        first_print = font.render("Welcome to Run-Type-Tiles,", True, (255, 255, 255))
        screen.blit(first_print, (screen_width / 2 - first_print.get_width() / 1, screen_height / 8 - first_print.get_height() / 2))
        first_printt = font.render("Visit Krafi.info to Learn more", True, (255, 255, 255))
        screen.blit(first_printt, (screen_width / 2 - first_printt.get_width() / 4, screen_height / 5 - first_printt.get_height() / 2))
        first_time = False
    current_word = choose_word()
    text = font.render(current_word, True, (80, 250, 123))
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
                screen.fill((255, 184, 108), input_rect)
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
        input_text_surf = input_font.render(input_word, True, (255, 85, 85) if incorrect_input else (80, 250, 123))
        input_rect = input_text_surf.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.fill((81, 84, 111), input_rect)
        screen.blit(input_text_surf, input_rect)
        pygame.display.update()
        if input_word == current_word:
            correct_sound.play()
            score += 1
            break

    time_elapsed = time.time() - last_input_time
    wpm = int(len(input_word) / 5 / (time_elapsed / 60))
    wpm_text = font.render("WPM: " + str(wpm), True, (255, 255, 255))
    
    score_text = font.render("Score: " + str(score), True, (255, 184, 108))
    screen.fill((68, 71, 90))
    screen.blit(score_text, (10, 10))
    screen.blit(wpm_text, (850, 10))
    pygame.display.update()
    if score < 0:
        game_over = True
        break
    
    if not paused:
        pygame.mixer.music.unpause()
    last_input_time = time.time()
pygame.quit()
 
