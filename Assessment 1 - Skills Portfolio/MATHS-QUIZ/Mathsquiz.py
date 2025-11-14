from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame
import sys
import os

# --- THEME ---
NEON_COLORS = {
    'background_dark': '#1a0033',
    'neon_magenta': '#FF00FF',
    'neon_cyan': '#00FFFF',
    'neon_yellow': '#FFBA1E',
    'accent_red': '#FF44AA',
    'text_light': '#ecf0f1',
}

# --- GAME DICTIONARY ---
game = { 
    'level': None, 
    'question_num': 0, 
    'score': 0,
    'streak_bonus': 0,  # NEW: separate streak bonus tracking
    'chances': 0, 
    'num1': 0, 
    'num2': 0, 
    'operator': '', 
    'ans': 0, 
    'root': None, 
    'entry': None, 
    'streak': 0, 
    'lives': 3, 
    'countdown': 30, 
    'timer_running': False, 
    'time_taken': [], 
    'question_start_time': 0, 
    'answered_questions': 0,
    'time_limit': 0, 
    'bg_path': '',   
    'combo_multiplier': 1.0, 
    'shield_active': False,  
    'sounds': {},
    'images': {},
    'timer_id': None  # NEW: for proper timer cancellation
}

# --- ASSET PATHS ---
IMAGE_ASSET_LIST = {
    'play_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\play_btn.png", (100, 50)),
    'instructions_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\instructions_btn.png", (40, 40)),
    'quit_button_home': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\quit_btn.png", (40, 40)),
    'easy_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\easy_btn.png", (100, 80)),
    'medium_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\medium_btn.png", (100, 80)),
    'hard_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\hard_btn.png", (100, 80)),
    'submit_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\submit_btn.png", (120, 50)),
    'quit_button_q': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\quit_btn.png", (40, 40)),
    'return_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\return_btn.png", (40, 40)),
    'play_again_button': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\buttons\replay_btn.png", (40, 40)),
    'home_title_img': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\title.png", (400, 80)),
    'menu_title': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\menu_title.png", (400, 80)),
    'card_frame': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\card_frame.png", (400, 300)),
    'record_frame': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\record_frame.png", (400, 300)),
    'result_box': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\card_box.png", (450, 550)),
    'easy_bg': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\easy_bg.jpg", (800, 750)),
    'medium_bg': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\medium_bg.jpg", (800, 750)),
    'hard_bg': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\hard_bg.jpg", (800, 750)),
}

AUDIO_ASSET_PATHS = {
    'home_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\home_music.wav",
    'easy_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\easy_music.wav",
    'medium_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\medium_music.wav",
    'hard_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\hard_music.wav",
    'victory_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\victory.wav",
    'defeat_music': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\defeat.wav",
    'correct': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\correct.wav",
    'wrong': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\wrong.wav",
    'button_click': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\sounds\button_click.wav"
}

BACKGROUND_PATHS = {
    'home': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\home_bg.gif", 
    'menu': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\menu_bg.jpg", 
    'win': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\win_bg.gif",
    'fail': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\fail_bg.gif"
}

# --- MAIN WINDOW ---
def main():
    game['root'] = Tk()
    game['root'].title("MATH QUIZ // MATH MADNESS")
    game['root'].geometry("800x750")
    game['root'].resizable(False, False)
    game['root'].configure(bg=NEON_COLORS['background_dark'])

    setup_audio()
    load_all_images()
    play_music('home_music')
    start_screen()
    game['root'].mainloop()

# --- IMAGE LOADING ---
def load_all_images():
    print("Loading images...")
    for name, (path, size) in IMAGE_ASSET_LIST.items():
        try:
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize(size)
                game['images'][name] = ImageTk.PhotoImage(img)
                print(f"✓ Loaded: {path}")
            else:
                print(f"✗ Not found: {path}")
                placeholder = Image.new('RGB', size, color=NEON_COLORS['neon_magenta'])
                game['images'][name] = ImageTk.PhotoImage(placeholder)
        except Exception as e:
            print(f"✗ Error loading {path}: {e}")
            placeholder = Image.new('RGB', size, color=NEON_COLORS['neon_magenta'])
            game['images'][name] = ImageTk.PhotoImage(placeholder)
    
    for name, path in BACKGROUND_PATHS.items():
        try:
            if os.path.exists(path):
                gif = Image.open(path)
                game['images'][f'{name}_frames'] = [
                    ImageTk.PhotoImage(frame.copy().resize((800, 750))) 
                    for frame in ImageSequence.Iterator(gif)
                ]
                print(f"✓ Loaded GIF: {path} ({len(game['images'][f'{name}_frames'])} frames)")
            else:
                print(f"✗ GIF not found: {path}")
                static_img = Image.new('RGB', (800, 750), color=NEON_COLORS['background_dark'])
                game['images'][f'{name}_frames'] = [ImageTk.PhotoImage(static_img)]
        except Exception as e:
            print(f"✗ Error loading GIF {path}: {e}")
            static_img = Image.new('RGB', (800, 750), color=NEON_COLORS['background_dark'])
            game['images'][f'{name}_frames'] = [ImageTk.PhotoImage(static_img)]

def clear_screen():
    # Cancel timer properly
    if game.get('timer_id'):
        try:
            game['root'].after_cancel(game['timer_id'])
        except:
            pass
    game['timer_running'] = False
    for widget in game['root'].winfo_children():
        widget.destroy()

# --- AUDIO SETUP ---
def setup_audio():
    try:
        pygame.mixer.init()
        game['sounds'] = {}
        for sound_name, sound_path in AUDIO_ASSET_PATHS.items():
            try:
                if os.path.exists(sound_path):
                    if 'music' in sound_name:
                        game['sounds'][sound_name] = sound_path
                    else:
                        game['sounds'][sound_name] = pygame.mixer.Sound(sound_path)
                    print(f"✓ Loaded audio: {sound_path}")
                else:
                    print(f"✗ Audio not found: {sound_path}")
            except Exception as e:
                print(f"✗ Error loading audio {sound_path}: {e}")
    except Exception as e:
        print(f"✗ Pygame mixer error: {e}")

def button_click_sound(command):
    def wrapper(*args, **kwargs):
        play_sound_effect('button_click')
        return command(*args, **kwargs)
    return wrapper

def play_music(music_name):
    stop_music()
    if music_name in game.get('sounds', {}) and isinstance(game['sounds'][music_name], str):
        try:
            pygame.mixer.music.load(game['sounds'][music_name])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except:
            pass

def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

def play_sound_effect(sound_name):
    sound = game.get('sounds', {}).get(sound_name)
    if isinstance(sound, pygame.mixer.Sound):
        sound.play()

def confirm_exit():
    answer = messagebox.askyesno("TERMINATE", "End Session? All progress will be lost!")
    if answer:
        game['root'].quit()

# --- START SCREEN ---
def start_screen():
    clear_screen()
    start_frame = Frame(game['root'])
    start_frame.pack(fill=BOTH, expand=True)

    frames = game['images'].get('home_frames', [])
    bg_label = Label(start_frame)
    bg_label.pack(fill="both", expand=True)

    def animate(index=0):
        if frames:
            bg_label.config(image=frames[index])
            game['root'].after(25, animate, (index + 1) % len(frames))
    animate(0)

    if 'home_title_img' in game['images']:
        title_label = Label(start_frame, image=game['images']['home_title_img'], 
                            bg=NEON_COLORS['background_dark'], borderwidth=0)
        title_label.place(relx=0.5, rely=0.30, anchor="center")

    start_button = Button(start_frame, image=game['images']['play_button'], 
                         bg=NEON_COLORS['background_dark'], 
                         activebackground=NEON_COLORS['background_dark'],
                         borderwidth=0, highlightthickness=0, cursor="hand2", 
                         command=button_click_sound(menu))
    start_button.place(relx=0.74, rely=0.72, anchor="center")

    def show_instructions():
        instruction_window = Toplevel(game['root'])
        instruction_window.title("📖 MATH QUIZ PROTOCOL // SYSTEM GUIDE")
        instruction_window.geometry("700x750")
        instruction_window.resizable(False, False)
        instruction_window.configure(bg=NEON_COLORS['background_dark'])

        # Main container with border
        main_container = Frame(instruction_window, bg=NEON_COLORS['background_dark'], 
                              highlightbackground=NEON_COLORS['neon_cyan'], 
                              highlightthickness=3)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        title_frame = Frame(main_container, bg=NEON_COLORS['neon_magenta'], height=80)
        title_frame.pack(fill=X)
        title_frame.pack_propagate(False)
        
        Label(title_frame, text="👾 MATH QUIZ PROTOCOL 👾", 
              font=('Courier', 20, 'bold'), 
              fg=NEON_COLORS['background_dark'], 
              bg=NEON_COLORS['neon_magenta']).pack(pady=25)
        
        # Scrollable content
        canvas = Canvas(main_container, bg=NEON_COLORS['background_dark'], 
                       highlightthickness=0)
        scrollbar = Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=NEON_COLORS['background_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content = [
            ("🎯 OBJECTIVE", "Complete 10 mathematical diagnostics to test your computational skills. Survive all questions with your lives intact to achieve maximum credits!", NEON_COLORS['neon_yellow']),
            
            ("🎮 DIFFICULTY MODES", "", NEON_COLORS['neon_cyan']),
            ("  🌱 EASY MODE", "• Numbers: 1-9 (Single Digit)\n• Time Limit: 30 seconds per question\n• Lives: 3 hearts\n• Perfect for beginners!", NEON_COLORS['text_light']),
            ("  🍂 MODERATE MODE", "• Numbers: 10-99 (Double Digit)\n• Time Limit: 20 seconds per question\n• Lives: 3 hearts\n• Challenge your speed!", NEON_COLORS['text_light']),
            ("  🔥 ADVANCED MODE", "• Numbers: 1000-9999 (Four Digits)\n• Time Limit: 15 seconds per question\n• Lives: 2 hearts\n• COMBO multiplier for streaks!\n• Only for math masters!", NEON_COLORS['text_light']),
            
            ("⚡ HOW TO PLAY", "", NEON_COLORS['neon_cyan']),
            ("", "1. Select your difficulty level\n2. Solve 10 math problems (+ or -)\n3. Type your answer and press ENTER or click SUBMIT\n4. Beat the timer for each question!", NEON_COLORS['text_light']),
            
            ("💎 SCORING SYSTEM", "", NEON_COLORS['neon_cyan']),
            ("", "✓ First Attempt Correct: +10 Credits\n✓ Second Attempt Correct: +5 Credits\n✗ Both Wrong or Timeout: Lose 1 Life\n\n🔥 STREAK BONUS:\n• Get 3+ correct in a row for bonus points!\n• Advanced mode has COMBO multiplier!", NEON_COLORS['text_light']),
            
            ("❤️ LIVES SYSTEM", "", NEON_COLORS['neon_cyan']),
            ("", "• Start with 2-3 lives (depends on difficulty)\n• Lose a life when:\n  - Both attempts are wrong\n  - Timer runs out\n• Game Over when all lives are lost!", NEON_COLORS['text_light']),
            
            ("🏆 RANKING", "", NEON_COLORS['neon_cyan']),
            ("", "S Rank: 90-100 points (PHENOMENAL!)\nA+ Rank: 80-89 points (EXCELLENT!)\nA Rank: 70-79 points (GREAT JOB!)\nB Rank: 60-69 points (GOOD WORK!)\nC Rank: 50-59 points (KEEP TRYING!)\nF Rank: Below 50 (TRY AGAIN!)", NEON_COLORS['text_light']),
            
            ("💡 PRO TIPS", "", NEON_COLORS['neon_yellow']),
            ("", "• Use mental math for speed\n• Don't panic when timer goes yellow!\n• Build streaks for bonus points\n• Practice makes perfect!", NEON_COLORS['text_light']),
        ]
        
        for title, text, color in content:
            if title:
                Label(scrollable_frame, text=title, font=('Courier', 14, 'bold'), 
                      fg=color, bg=NEON_COLORS['background_dark'], 
                      anchor='w', justify='left').pack(fill=X, padx=20, pady=(15, 5))
            if text:
                Label(scrollable_frame, text=text, font=('Courier', 11), 
                      fg=color, bg=NEON_COLORS['background_dark'], 
                      anchor='w', justify='left', wraplength=620).pack(fill=X, padx=30, pady=(0, 5))
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)
        
        # Close button
        close_frame = Frame(main_container, bg=NEON_COLORS['background_dark'], height=70)
        close_frame.pack(fill=X)
        close_frame.pack_propagate(False)
        
        Button(close_frame, text="✖ CLOSE PROTOCOL", 
               command=instruction_window.destroy,
               font=('Courier', 14, 'bold'), 
               bg=NEON_COLORS['neon_magenta'], 
               fg=NEON_COLORS['background_dark'],
               activebackground=NEON_COLORS['neon_cyan'],
               cursor='hand2', 
               padx=30, pady=15,
               relief=RAISED,
               bd=3).pack(pady=15)

    instruction_button = Button(start_frame, 
                               image=game['images']['instructions_button'], 
                               bg=NEON_COLORS['background_dark'], 
                               activebackground=NEON_COLORS['background_dark'],
                               borderwidth=0, highlightthickness=0, cursor="hand2",
                               command=button_click_sound(show_instructions))
    instruction_button.place(relx=0.07, rely=0.07, anchor="center")

    exit_button = Button(start_frame, image=game['images']['quit_button_home'], 
                        bg=NEON_COLORS['background_dark'], 
                        activebackground=NEON_COLORS['background_dark'],
                        borderwidth=0, highlightthickness=0, cursor="hand2",
                        command=button_click_sound(confirm_exit))
    exit_button.place(relx=0.93, rely=0.07, anchor="center")

# --- MENU SCREEN ---
def menu():
    stop_music()
    play_music('home_music')
    clear_screen()

    main_frame = Frame(game['root'], bg=NEON_COLORS['background_dark'])
    main_frame.pack(fill=BOTH, expand=True)

    frames = game['images'].get('menu_frames', [])
    label = Label(main_frame)
    label.pack(fill="both", expand=True)
    
    def animate(index=0):
        if frames:
            label.config(image=frames[index])
            game['root'].after(50, animate, (index + 1) % len(frames))
    animate()

    box = Frame(main_frame, bg=NEON_COLORS['background_dark'], bd=3,relief=RIDGE, highlightbackground=NEON_COLORS['neon_magenta'])
    box.place(relx=0.5, rely=0.3, anchor="center")
    
    if 'menu_title' in game['images']:
        l1 = Label(box, image=game['images']['menu_title'], 
                  bg=NEON_COLORS['background_dark'])
        l1.pack()
    
    button1 = Frame(main_frame, bg="#9C86D5", width=200, height=250)
    button1.place(relx=0.35, rely=0.83, anchor="center")

    easy_button = Button(button1, image=game['images']['easy_button'], 
                        bg='#9C86D5', 
                        activebackground=NEON_COLORS['background_dark'],
                        borderwidth=0, highlightthickness=0, cursor="hand2", 
                        command=button_click_sound(lambda: start_quiz(1)))
    easy_button.pack(pady=5)

    button2 = Frame(main_frame, bg='#9C86D5', width=200, height=250)
    button2.place(relx=0.5, rely=0.83, anchor="center")
    medium_button = Button(button2, image=game['images']['medium_button'], 
                          bg='#9C86D5', 
                          activebackground=NEON_COLORS['background_dark'],
                          borderwidth=0, highlightthickness=0, cursor="hand2", 
                          command=button_click_sound(lambda: start_quiz(2)))
    medium_button.pack(pady=5)
    
    button3 = Frame(main_frame, bg='#9C86D5', width=200, height=250)
    button3.place(relx=0.65, rely=0.83, anchor="center")
    hard_button = Button(button3, image=game['images']['hard_button'], 
                        bg='#9C86D5', 
                        activebackground=NEON_COLORS['background_dark'],
                        borderwidth=0, cursor="hand2", 
                        command=button_click_sound(lambda: start_quiz(3)))
    hard_button.pack(pady=5)
    
    exit_button = Button(main_frame, image=game['images']['quit_button_home'], 
                        bg=NEON_COLORS['background_dark'], 
                        activebackground=NEON_COLORS['background_dark'],
                        borderwidth=0, highlightthickness=0, cursor="hand2", 
                        command=button_click_sound(confirm_exit))
    exit_button.place(relx=0.93, rely=0.07, anchor="center")
    
    return_button = Button(main_frame, image=game['images']['return_button'], 
                          bg=NEON_COLORS['background_dark'], 
                          activebackground=NEON_COLORS['background_dark'],
                          borderwidth=0, highlightthickness=0, cursor="hand2", 
                          command=button_click_sound(start_screen))
    return_button.place(relx=0.07, rely=0.07, anchor="center")

# --- GAME LOGIC ---
def random_nums():
    level = game['level']
    if level == 1:
        return random.randint(1, 9), random.randint(1, 9)
    if level == 2:
        return random.randint(10, 99), random.randint(10, 99)
    return random.randint(1000, 9999), random.randint(1000, 9999)

def start_quiz(level):
    stop_music()
    game.update({
        'level': level, 'question_num': 0, 'score': 0, 'streak': 0, 'streak_bonus': 0,
        'chances': 2, 'time_taken': [], 'question_start_time': 0,
        'answered_questions': 0, 'combo_multiplier': 1.0, 'shield_active': False
    })

    if level == 1:
        game['bg_image'] = 'easy_bg'
        game['time_limit'] = 30
        game['lives'] = 3
        play_music('easy_music')
    elif level == 2:
        game['bg_image'] = 'medium_bg'
        game['time_limit'] = 20
        game['lives'] = 3
        play_music('medium_music')
    elif level == 3:
        game['bg_image'] = 'hard_bg'
        game['time_limit'] = 15
        game['lives'] = 2
        play_music('hard_music')
    next_question()

def next_question():
    if game['question_num'] >= 10 or game['lives'] <= 0:
        results()
        return

    game['question_num'] += 1
    game['chances'] = 2
    game['countdown'] = game['time_limit']
    game['timer_running'] = True  # CRITICAL: Set to True BEFORE show_q()
    game['num1'], game['num2'] = random_nums()
    game['operator'] = random.choice(['+', '-'])
    game['ans'] = game['num1'] + game['num2'] if game['operator'] == '+' else game['num1'] - game['num2']
    game['question_start_time'] = time.time()
    print(f"DEBUG: Timer starting - countdown={game['countdown']}, timer_running={game['timer_running']}")  # DEBUG
    show_q()  # FIXED: Added this back!
    print(f"DEBUG: Timer starting - countdown={game['countdown']}, timer_running={game['timer_running']}")  # DEBUG
    show_q()

# --- QUESTION SCREEN ---
def show_q():
    clear_screen()
    f = Frame(game['root'], bg=NEON_COLORS['background_dark'])
    f.pack(fill="both", expand=True)

    # CHANGED: Use static background image
    bg_key = game.get('bg_image', 'easy_bg')
    if bg_key in game['images']:
        bg_label = Label(f, image=game['images'][bg_key])
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # CHANGED: Redesigned top bar
    top = Frame(f, bg='#2C1F4A', height=50)
    top.pack(fill=X, side=TOP)
    top.pack_propagate(False)
    
    # Score on left
    Label(top, text=f"💰 {game['score']}/100", font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_yellow'], bg='#2C1F4A').pack(side=LEFT, padx=20, pady=10)
    
    # Timer in center - FIXED
    game['timer_label'] = Label(top, text=f"⏱ {game['countdown']}s", 
                               font=('Courier', 18, 'bold'), 
                               fg=NEON_COLORS['neon_cyan'], bg='#2C1F4A')
    game['timer_label'].pack(side=LEFT, padx=150, pady=10)
    
    # Lives on right
    max_lives = 3 if game['level'] < 3 else 2
    lives_display = "💖" * game['lives'] + "🖤" * (max_lives - game['lives'])
    Label(top, text=lives_display, font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg='#2C1F4A').pack(side=RIGHT, padx=20, pady=10)

    # FIXED: Completely rewritten timer
    def tick_timer():
        print(f"DEBUG: tick_timer called - countdown={game['countdown']}, timer_running={game['timer_running']}")  # DEBUG
        
        if not game['timer_running']:
            print("DEBUG: Timer not running, stopping")  # DEBUG
            return
        
        if game['countdown'] <= 0:
            print("DEBUG: Time's up!")  # DEBUG
            game['timer_running'] = False
            handle_timeout()
            return
        
        # Decrease countdown
        game['countdown'] -= 1
        print(f"DEBUG: Countdown decreased to {game['countdown']}")  # DEBUG
        
        # Update label
        try:
            color = NEON_COLORS['neon_yellow'] if game['countdown'] <= 5 else NEON_COLORS['neon_cyan']
            game['timer_label'].config(text=f"⏱ {game['countdown']}s", fg=color)
            print(f"DEBUG: Label updated")  # DEBUG
        except Exception as e:
            print(f"DEBUG: Error updating label: {e}")  # DEBUG
            return
        
        # Schedule next tick
        game['timer_id'] = game['root'].after(1000, tick_timer)
        print(f"DEBUG: Next tick scheduled")  # DEBUG
    
    # Start timer immediately
    print(f"DEBUG: Starting timer with countdown={game['countdown']}")  # DEBUG
    tick_timer()
    
    # CHANGED: Question number moved next to question
    question_frame = Frame(f, bg=NEON_COLORS['background_dark'])
    question_frame.pack(pady=60)
    
    # Question number above question
    Label(question_frame, text=f"QUESTION {game['question_num']}/10", 
          font=("Courier", 14, "bold"), fg=NEON_COLORS['neon_cyan'], 
          bg=NEON_COLORS['background_dark']).pack(pady=(0, 10))
    
    question_display = Frame(question_frame, bg=NEON_COLORS['background_dark'], bd=5, 
                            relief=SOLID, highlightbackground=NEON_COLORS['neon_cyan'], 
                            highlightthickness=2)
    question_display.pack(padx=20, pady=10)
    
    op_col = NEON_COLORS['neon_cyan'] if game['operator'] == '+' else NEON_COLORS['neon_magenta']
    
    q_content = Frame(question_display, bg=NEON_COLORS['background_dark'])
    q_content.pack(padx=30, pady=20)
    
    Label(q_content, text=f"{game['num1']}", font=("Courier", 56, "bold"), 
          fg=NEON_COLORS['text_light'], bg=NEON_COLORS['background_dark']).pack(side=LEFT, padx=15)
    Label(q_content, text=game['operator'], font=("Courier", 56, "bold"), 
          fg=op_col, bg=NEON_COLORS['background_dark']).pack(side=LEFT, padx=15)
    Label(q_content, text=f"{game['num2']}", font=("Courier", 56, "bold"), 
          fg=NEON_COLORS['text_light'], bg=NEON_COLORS['background_dark']).pack(side=LEFT, padx=15)
    Label(q_content, text="=", font=("Courier", 56, "bold"), 
          fg=NEON_COLORS['text_light'], bg=NEON_COLORS['background_dark']).pack(side=LEFT, padx=15)

    entry_frame = Frame(f, bg=NEON_COLORS['background_dark'])
    entry_frame.pack(pady=20)
    
    Label(entry_frame, text="Input Answer:", font=("Courier", 14, "bold"), 
          fg=NEON_COLORS['neon_cyan'], bg=NEON_COLORS['background_dark']).pack(pady=5)
    
    game['entry'] = Entry(entry_frame, font=("Courier", 32, "bold"), width=12, justify='center', 
                         bg=NEON_COLORS['background_dark'], fg=NEON_COLORS['neon_yellow'],
                         insertbackground=NEON_COLORS['neon_cyan'], relief=SOLID, bd=3,
                         highlightbackground=NEON_COLORS['neon_cyan'], highlightthickness=2)
    game['entry'].pack(pady=10)
    game['entry'].focus()
    game['entry'].bind('<Return>', lambda e: check())

    submit_frame = Frame(f, bg=NEON_COLORS['background_dark'])
    submit_frame.pack(pady=10)
    
    Button(submit_frame, image=game['images']['submit_button'], 
           bg=NEON_COLORS['background_dark'], activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(check)).pack()

    if game['chances'] == 1:
        Label(f, text="⚠️ Second Attempt: 5 Credits", font=("Courier", 12, "bold"), 
              fg=NEON_COLORS['neon_yellow'], bg=NEON_COLORS['background_dark']).pack(pady=5)
    
    if game['streak'] >= 3:
        streak_text = f"🔥 {game['streak']} Streak!"
        if game['level'] == 3:
            streak_text = f"COMBO x{game['combo_multiplier']:.1f}!"
        Label(f, text=streak_text, font=("Courier", 12, "bold"), 
              fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).pack(pady=5)
        
    Button(f, image=game['images']['quit_button_q'], bg=NEON_COLORS['background_dark'],
           activebackground=NEON_COLORS['background_dark'], borderwidth=0, 
           highlightthickness=0, cursor="hand2", 
           command=button_click_sound(confirm_exit)).place(relx=0.95, rely=0.95, anchor="center")

    Button(f, image=game['images']['return_button'], bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], borderwidth=0, 
           highlightthickness=0, cursor="hand2", 
           command=button_click_sound(lambda: confirm_return())).place(relx=0.055, rely=0.95, anchor="center")

def handle_timeout():
    game['timer_running'] = False
    elapsed = time.time() - game['question_start_time']
    game['time_taken'].append(round(elapsed, 2))
    reset_streak()
    lose_life(is_timeout=True)

def confirm_return():
    game['timer_running'] = False
    answer = messagebox.askyesno("ABORT", "Return to menu? Progress will be lost!")
    if answer:
        menu()
    else:
        game['timer_running'] = True

def check():
    try:
        ans = int(game['entry'].get())
        game['timer_running'] = False
        if game.get('timer_id'):
            game['root'].after_cancel(game['timer_id'])
        check_ans(ans)
    except ValueError:
        messagebox.showerror("Invalid", "Enter a valid number!")
        game['entry'].delete(0, END)
        game['entry'].focus()

def reset_streak():
    game['streak'] = 0
    game['combo_multiplier'] = 1.0

def lose_life(is_timeout=False):
    if game['level'] == 2 and game['shield_active']:
        game['shield_active'] = False
        messagebox.showinfo("SHIELD", "🛡️ Life protected!")
        next_question()
        return

    game['lives'] -= 1
    
    if game['lives'] <= 0:
        msg = f"💀 No lives left!\nFinal Credits: {game['score']}/100"
        messagebox.showerror("Game Over", msg)
        results()
    else:
        msg = f"{'⏰ Time expired!' if is_timeout else '❌ Wrong!'}\nAnswer: {game['ans']}\n💔 Lives: {game['lives']}"
        messagebox.showwarning("Life Lost", msg)
        next_question()

def update_streak_display():
    pass

def check_ans(user):
    elapsed = time.time() - game['question_start_time']
    
    if user == game['ans']:
        play_sound_effect('correct')
        game['answered_questions'] += 1
        game['time_taken'].append(round(elapsed, 2))
        game['streak'] += 1
        
        points = 10 if game['chances'] == 2 else 5
        
        # CHANGED: Calculate streak bonus separately
        streak_bonus = 0
        if game['chances'] == 2 and game['level'] == 3 and game['streak'] >= 3:
            game['combo_multiplier'] = 1.0 + (game['streak'] - 2) * 0.5
            bonus_points = int(points * (game['combo_multiplier'] - 1.0))
            streak_bonus = bonus_points
        elif game['chances'] == 2 and game['streak'] >= 3:
            streak_bonus = game['streak'] * 2
        
        if game['chances'] == 1:
            game['streak'] = 0
        
        game['score'] += points
        game['streak_bonus'] += streak_bonus
        
        messagebox.showinfo("Correct!", f"✅ +{points} Credits!" + (f"\n🔥 +{streak_bonus} Streak Bonus!" if streak_bonus > 0 else ""))
        next_question()
    else:
        play_sound_effect('wrong')
        game['chances'] -= 1
        reset_streak()
        
        if game['chances'] > 0:
            messagebox.showwarning("Wrong", "❌ One more try (5 credits)")
            game['timer_running'] = True
            show_q()
        else:
            game['time_taken'].append(round(elapsed, 2))
            lose_life(is_timeout=False)

# --- RESULTS SCREEN ---
def results():
    game['timer_running'] = False
    clear_screen()

    score = game['score']
    
    if score >= 90: grade, msgg = "S", "PHENOMENAL!"
    elif score >= 80: grade, msgg = "A+", "EXCELLENT!"
    elif score >= 70: grade, msgg = "A", "GREAT JOB!"
    elif score >= 60: grade, msgg = "B", "GOOD WORK!"
    elif score >= 50: grade, msgg = "C", "KEEP TRYING!"
    else: grade, msgg = "F", "TRY AGAIN!"

    if score >= 60:
        stop_music()
        play_music('victory_music')
        frames_key = 'win_frames'
    else:
        stop_music()
        play_music('defeat_music')
        frames_key = 'fail_frames'

    f = Frame(game['root'], bg=NEON_COLORS['background_dark'], width=800, height=750)
    f.place(x=0, y=0)

    frames = game['images'].get(frames_key, [])
    bg_label = Label(f)
    bg_label.place(x=0, y=0, width=800, height=750)
    
    def animate_bg(index=0):
        if frames:
            bg_label.config(image=frames[index])
            bg_label.lower()
            game['root'].after(80, animate_bg, (index + 1) % len(frames))
    animate_bg()
    
    mini_frame = Frame(f, width=450, height=550, bg=NEON_COLORS['background_dark'], 
                      highlightbackground=NEON_COLORS['neon_cyan'], highlightthickness=2)
    mini_frame.place(relx=0.5, rely=0.5, anchor="center")
    mini_frame.pack_propagate(False)

    if 'result_box' in game['images']:
        box_bg = Label(mini_frame, image=game['images']['result_box'])
        box_bg.place(x=0, y=0, relwidth=1, relheight=1)
    else:
        mini_frame.config(bg=NEON_COLORS['background_dark'])

    if 'card_frame' in game['images']:
        card = Label(mini_frame, image=game['images']['card_frame'], 
                    bg='#8C1345', bd=0)
        card.place(relx=0.5, rely=0.47, anchor="center")

    Label(mini_frame, text="FINAL CREDITS", font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_cyan'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.20, anchor="center")
    
    # CHANGED: Display score directly without animation
    score_display = Frame(mini_frame, bg=NEON_COLORS['background_dark'], relief=SUNKEN, bd=2, 
                         width=180, height=90, highlightbackground=NEON_COLORS['neon_yellow'], 
                         highlightthickness=3)
    score_display.place(relx=0.5, rely=0.32, anchor="center")
    score_display.pack_propagate(False)
    
    Label(score_display, text=str(score), font=("Courier", 42, "bold"), 
          fg=NEON_COLORS['neon_yellow'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.44, anchor="center")

    Label(score_display, text="/ 100 Credits", font=("Courier", 11), 
          fg=NEON_COLORS['text_light'], bg='#181338').place(relx=0.5, rely=0.88, anchor="center")

    # CHANGED: Add separate streak bonus display
    Label(mini_frame, text="STREAK BONUS", font=("Courier", 12, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.45, anchor="center")
    
    bonus_display = Frame(mini_frame, bg=NEON_COLORS['background_dark'], relief=SUNKEN, bd=2, 
                         width=120, height=50, highlightbackground=NEON_COLORS['neon_magenta'], 
                         highlightthickness=2)
    bonus_display.place(relx=0.5, rely=0.52, anchor="center")
    bonus_display.pack_propagate(False)
    
    Label(bonus_display, text=f"+{game['streak_bonus']}", font=("Courier", 24, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.5, anchor="center")

    # Grade Section
    grade_box = Frame(mini_frame, bg=NEON_COLORS['neon_magenta'], relief=RAISED, bd=3, 
                     width=100, height=60)
    grade_box.place(relx=0.5, rely=0.62, anchor="center")
    grade_box.pack_propagate(False)
    
    Label(grade_box, text=grade, font=("Courier", 30, "bold"), 
          fg=NEON_COLORS['background_dark'], bg=NEON_COLORS['neon_magenta']).place(relx=0.5, rely=0.51, anchor="center")

    Label(mini_frame, text=msgg, font=("Courier", 12, "bold"), 
          fg=NEON_COLORS['neon_cyan'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.72, anchor="center")

    record_frame = Frame(mini_frame, width=400, height=100)
    record_frame.place(relx=0.5, rely=0.87, anchor="center")
    record_frame.pack_propagate(False)

    if 'record_frame' in game['images']:
        Label(record_frame, image=game['images']['record_frame'], bg='#8C1345', bd=0).place(x=0, y=0, relwidth=1, relheight=1)

    questions_answered = game.get('answered_questions', 0)
    lives_remaining = game.get('lives', 0)
    missed_questions = 10 - questions_answered
    average_time = round(sum(game['time_taken']) / len(game['time_taken']), 2) if game['time_taken'] else 0

    max_lives = 3 if game['level'] < 3 else 2
    stats_text = f"Questions: {questions_answered}/10\nMissed: {missed_questions}\nLives: {lives_remaining}/{max_lives}\nAvg Time: {average_time}s"
    
    Label(record_frame, text=stats_text, font=("Courier", 10, "bold"), 
          fg=NEON_COLORS['text_light'], bg=NEON_COLORS['background_dark'], 
          justify="center").place(relx=0.5, rely=0.5, anchor="center")

    Button(f, image=game['images']['play_again_button'], bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], borderwidth=0, 
           highlightthickness=0, cursor="hand2", 
           command=button_click_sound(menu)).place(relx=0.43, rely=0.93, anchor="center")

    Button(f, image=game['images']['quit_button_home'], bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], borderwidth=0, 
           highlightthickness=0, cursor="hand2", 
           command=button_click_sound(game['root'].quit)).place(relx=0.57, rely=0.93, anchor="center")


if __name__ == "__main__":
    main()