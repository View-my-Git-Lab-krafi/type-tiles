import tkinter as tk
from tkinter import ttk

# Define the Dracula color scheme
dracula_colors = {
    "background": "#434659",
    "foreground": "#f8f8f2",
    "text": "#282a36",
    "button_bg": "#44475a",
    "button_fg": "#f8f8f2",
    "entry_bg": "#44475a",
    "entry_fg": "#000000",
    "label_bg": "#f1fa8c",
    "label_fg": "#282a36",
    "checkbox_bg": "#282a36",
    "checkbox_fg": "#f8f8f2",
    "checkbox_highlight": "#44475a",
}

  #  "text": "#f8f8f2",
 #   "comment": "#6272a4",
 #   "cyan": "#8be9fd",
 #   "green": "#50fa7b",
 #   "orange": "#ffb86c",
  #  "pink": "#ff79c6",
  #  "purple": "#bd93f9",
  #  "red": "#ff5555",
  #  "yellow": "#f1fa8c",

# Create the root window
root = tk.Tk()
root.geometry("700x550")
root.configure(bg=dracula_colors["background"])

# Set the Dracula theme for the widgets
ttk_style = ttk.Style()

# Set the colors for the various elements
ttk_style.theme_create("dracula", parent="default")
ttk_style.theme_settings("dracula", {
    "TLabel": {"configure": {"background": dracula_colors["label_bg"], "foreground": dracula_colors["label_fg"]}},
    "TButton": {"configure": {"background": dracula_colors["button_bg"], "foreground": dracula_colors["button_fg"]}},
    "TEntry": {"configure": {"background": dracula_colors["entry_bg"], "foreground": dracula_colors["entry_fg"]}},
    "TCheckbutton": {"configure": {"background": dracula_colors["checkbox_bg"], "foreground": dracula_colors["checkbox_fg"], "highlightbackground": dracula_colors["checkbox_highlight"]}},
})
ttk_style.theme_use("dracula")

# Define the input fields and widgets
ytlink = "https://www.youtube.com/watch?v=bq7caidfUts"

####################################
label1 = tk.Label(root, text="Welcome to Run-Type-Tiles", fg="white", bg="#44475a")
label1.pack()
label1 = tk.Label(root, text="Visit Krafi.info to Learn more", fg="white", bg="#44475a")
label1.pack()
###################################

ytlink_label = ttk.Label(root, text="YouTube Link", font=("Helvetica", 24), anchor="center")
ytlink_label.pack(fill="x", padx=200, pady=10)

ytlink_entry = ttk.Entry(root, width=40)
ytlink_entry.insert(0, ytlink)
ytlink_entry.pack()



screen_width_label = ttk.Label(root, text="Screen Width", anchor="center")
screen_width_entry = ttk.Entry(root)
screen_width_entry.insert(0, "1280")

screen_width_label.pack(fill="x", padx=300, pady=5)
screen_width_entry.pack(fill="x", padx=330, pady=5)

screen_height_label = ttk.Label(root, text="Screen Height", anchor="center")
screen_height_label.pack( fill="x", padx=300, pady=5)

screen_height_entry = ttk.Entry(root)
screen_height_entry.insert(0, "720")
screen_height_entry.pack(fill="x", padx=330, pady=5)


level_label = ttk.Label(root, text="Level", anchor="center")
level_label.pack(fill="x", padx=300, pady=5)

level_entry = ttk.Entry(root)
level_entry.insert(0, "0")
level_entry.pack(fill="x", padx=340, pady=5, anchor="center")

remove_special_chars = True
remove_special_chars_var = tk.BooleanVar(value=True)

remove_special_chars_label = ttk.Label(root, text="Remove Special Characters", anchor="center")
remove_special_chars_label.pack(fill="x", padx=250, pady=5)
remove_special_chars_var = tk.BooleanVar(value=remove_special_chars)
remove_special_chars_checkbox = tk.Checkbutton(root, variable=remove_special_chars_var)
remove_special_chars_checkbox.pack()


auto_pause_no_type_label = ttk.Label(root, text="Auto Pause No Type", anchor="center")
auto_pause_no_type_label.pack(fill="x", padx=250, pady=5)
auto_pause_no_type_entry = ttk.Entry(root)
auto_pause_no_type_entry.insert(0, "2000")
auto_pause_no_type_entry.pack(fill="x", padx=330, pady=5, anchor="center")

def save_settings():
    global ytlink, screen_width, screen_height, level, remove_special_chars, AUTO_PAUSE_NO_TYPE
    
    ytlink = ytlink_entry.get()
    screen_width = int(screen_width_entry.get())
    screen_height = int(screen_height_entry.get())
    level = int(level_entry.get())
    remove_special_chars = remove_special_chars_var.get()
    AUTO_PAUSE_NO_TYPE = int(auto_pause_no_type_entry.get())
    
    print("Remove Special Characters:", remove_special_chars)
    
    root.destroy()

save_button = tk.Button(root, text="Run game", command=save_settings)
ytlink_label.pack()
ytlink_entry.pack()
screen_width_label.pack()
screen_width_entry.pack()
screen_height_label.pack()
screen_height_entry.pack()
level_label.pack()
level_entry.pack()
remove_special_chars_label.pack()
remove_special_chars_checkbox.pack()
auto_pause_no_type_label.pack()
auto_pause_no_type_entry.pack()
save_button.pack()
root.mainloop()




###################################################

from youtube_transcript_api import YouTubeTranscriptApi
import re
import pygame
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from pydub.playback import play
import time
import os

########################################################

correct_sound_video = "https://youtu.be/JQSwIFuqsyM"
file_path = "correct_sound.wav"

if not os.path.exists(file_path):
    from pytube import YouTube
    yt = YouTube(correct_sound_video)
    yt.streams.filter(only_audio=True).first().download()
    mp4_file = yt.title + ".mp4"
    sound = AudioSegment.from_file(mp4_file, format="mp4")
    sound.export(file_path, format="wav")
sound = AudioSegment.from_wav(file_path)

###########################################################

incorrect_sound_video = "https://youtu.be/P60PQE-4Lg8"
file_path = "incorrect_sound.wav"

if not os.path.exists(file_path):
    from pytube import YouTube
    yt = YouTube(incorrect_sound_video)
    yt.streams.filter(only_audio=True).first().download()
    mp4_file = yt.title + ".mp4"
    sound = AudioSegment.from_file(mp4_file, format="mp4")
    sound.export(file_path, format="wav")
sound = AudioSegment.from_wav(file_path)

###########################################################################

def play_music():
    youtube = YouTube(ytlink)
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(output_path='.', filename='aa')
    audio = AudioSegment.from_file(audio_file, format="mp4")
    audio.export("download", format="mp3")
    pygame.mixer.music.load("download")
    pygame.mixer.music.play(-1)

############################################################################

pygame.init()
pygame.mixer.init()
play_music()
correct_sound = pygame.mixer.Sound("correct_sound.wav")
correct_sound.set_volume(0.009)
incorrect_sound = pygame.mixer.Sound("incorrect_sound.wav")
incorrect_sound.set_volume(0.1)
#############################################################################

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

###############################################################################

if remove_special_chars:
    word_list = [re.sub(r'[^a-zA-Z0-9\s]', "", word) for word in word_list]
    word_list = [re.sub(r'\s+', " ", word).strip() for word in word_list]
print(word_list)
lp = 0
clock = pygame.time.Clock()
last_key_time = pygame.time.get_ticks()
start_time = None

################################################################################

font = pygame.font.SysFont(None, 52)
input_font = pygame.font.SysFont(None, 48)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Typing Game")
def choose_word():
    global lp
    tt=(word_list[lp])
    lp += 1
    if lp >= len(word_list):
       lp = 0
    return tt

#################################################################################

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

#################################################################################
def update_game(level):
    global game_over
    global input_word

    wpm = 0
    if len(input_word) > 0:
        time_elapsed = time.time() - last_input_time
        wpm = int(len(input_word) / 5 / (time_elapsed / 60))
    if wpm < (level * 10):
        game_over = True
######################################################################################
def render_game():
    global input_word

    wpm_text = font.render("Last WPM: " + str(wpm), True, (241, 250, 140))
    screen.blit(wpm_text, (10, 10))

    input_text = font.render(input_word, True, (241, 250, 140))
    screen.blit(input_text, (10, 50))

    pygame.display.update()
#################################################################
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
#############################################################
last_input_time = time.time()
score = 0
game_over = False
clock = pygame.time.Clock()
last_key_time = pygame.time.get_ticks()
paused = False
incorrect_input = False
first_time = True
#wpm = 0

##############################################################

while not game_over:

    #############################

    if first_time == True:
        screen.fill((68, 71, 90))
        font = pygame.font.SysFont(None, 48)
        first_print = font.render("Welcome to Run-Type-Tiles,", True, (255, 255, 255))
        screen.blit(first_print, (screen_width / 2 - first_print.get_width() / 1, screen_height / 8 - first_print.get_height() / 2))
        #first_printt = font.render("Visit Krafi.info to Learn more", True, (255, 255, 255))
        #screen.blit(first_printt, (screen_width / 2 - first_printt.get_width() / 4, screen_height / 5 - first_printt.get_height() / 2))
        first_time = False

    ########################################################

    current_word = choose_word()
    text = font.render(current_word, True, (80, 250, 123))
    text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 50))
    screen.blit(text, text_rect)
    input_word = ""
    incorrect_input = False  

    ##########################################################

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

        #########################################################

        for i in range(len(input_word)):
            if i >= len(current_word) or input_word[i] != current_word[i]:
                incorrect_input = True
                break
        ##########################################################

        if pygame.time.get_ticks() - last_key_time > AUTO_PAUSE_NO_TYPE and not paused:
            pygame.mixer.music.pause()
            paused = True
        
        #################################################################


        time_elapsed = time.time() - last_input_time
        if time_elapsed > 0:
            wpm = int(len(input_word) / 5 / (time_elapsed / 60))
        else:
            wpm = 1
        #wpm = int(len(input_word) / 5 / (time_elapsed / 60))
        wpm_text = font.render("WPM: " + str(wpm), True, (85, 255, 255))
        wpm_rect = wpm_text.get_rect(topleft=(screen_width - 150, 10))
        pygame.draw.rect(screen, (68, 71, 90), wpm_rect)
        screen.blit(wpm_text, (screen_width - 150, 10))
        pygame.display.update()

        ##################################################################


        input_text_surf = input_font.render(input_word, True, (255, 85, 85) if incorrect_input else (80, 250, 123))
        input_rect = input_text_surf.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.fill((81, 84, 111), input_rect)
        screen.blit(input_text_surf, input_rect)
        pygame.display.update()
        ####################################################
        if input_word == current_word:
            correct_sound.play()
            score += 1
            break
#####################################################################

    time_elapsed = time.time() - last_input_time
    wpm = int(len(input_word) / 5 / (time_elapsed / 60))
    wpm_text = font.render("WPM: " + str(wpm), True, (241, 250, 140))
    update_game(level)
    render_game()
#####################################################################
    score_text = font.render("Score: " + str(score), True, (255, 184, 108))
    screen.fill((68, 71, 90))
    screen.blit(score_text, (10, 10))
    screen.blit(wpm_text, (screen_width - 150, 50)) 
    pygame.display.update()
########################################################################
    if score < 0:
        game_over = True
        break
    ##################################################################
    if not paused:
        pygame.mixer.music.unpause()
    last_input_time = time.time()
    ####################################################################
pygame.quit()
 
