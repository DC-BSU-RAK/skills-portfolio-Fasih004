# --- IMPORTS ---
from tkinter import *                           # GUI framework for creating the application window and widgets
from tkinter import messagebox                  # Dialog boxes for user confirmations and alerts
from PIL import Image, ImageTk, ImageSequence   # Image processing library for loading and manipulating images/GIFs
import random                                   # Generate random numbers for quiz questions
import time                                     # Track elapsed time for questions and timer functionality
import pygame                                   # Audio library for playing background music and sound effects


# --- THEME ---
# Color palette for neon-themed UI
NEON_COLORS = {
    'background_dark': '#1a0033',   # Dark purple background
    'neon_magenta': '#FF00FF',      # Bright magenta accent
    'neon_cyan': '#00FFFF',         # Bright cyan accent
    'neon_yellow': '#FFBA1E',       # Bright yellow accent
    'accent_red': '#FF44AA',        # Accent red color
    'text_light': "#e1e5e6",        # Light text color for readability
}

# --- GAME DICTIONARY ---
# Global game state tracker
game = { 
    'level': None,        # Current difficulty level (1=Easy, 2=Medium, 3=Hard)
    'question_num': 0,    # Current question number (0-10)
    'score': 0,           # Total score/credits earned
    'streak_bonus': 0,    # Bonus points from consecutive correct answers
    'chances': 0,         # Remaining attempts for current question (0-2)
    'num1': 0,            # First operand in the equation
    'num2': 0,            # Second operand in the equation
    'operator': '',       # Mathematical operator ('+' or '-')
    'ans': 0,             # Correct answer to current question
    'root': None,         # Main Tkinter window object
    'entry': None,        # User input entry widget reference
    'streak': 0,          # Count of consecutive correct answers
    'lives': 3,           # Remaining lives (hearts)
    'countdown': 30,      # Remaining time in seconds for current question
    'timer_running': False,  # Flag to control timer execution
    'time_taken': [],        # List of time durations for each answered question
    'question_start_time': 0,   # Timestamp when question was displayed
    'answered_questions': 0,    # Total number of questions correctly answered
    'time_limit': 0,            # Time limit in seconds (based on difficulty)
    'bg_path': '',              # Current background image path
    'combo_multiplier': 1.0,    # Multiplier for hard mode streaks
    'shield_active': False,     # Protection shield status for medium mode
    'sounds': {},               # Dictionary storing loaded audio objects
    'images': {},               # Dictionary storing loaded image objects
    'timer_id': None            # ID of scheduled timer callback for cancellation
}

# --- ASSET PATHS ---
# Image file paths and dimensions
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

# Audio file paths
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

# Background animation paths
BACKGROUND_PATHS = {
    'home': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\home_bg.gif", 
    'menu': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\menu_bg.jpg", 
    'win': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\win_bg.gif",
    'fail': r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\backgrounds\fail_bg.gif"
}

# --- MAIN WINDOW ---
# Initialize main window and load resources
def main():
    game['root'] = Tk()                                          # Initialize main Tk window
    game['root'].title("MATH MADNESS")              # Set window title
    game['root'].geometry("800x750")                             # Set fixed window size
    game['root'].resizable(False, False)                         # Disable resizing
    game['root'].configure(bg=NEON_COLORS['background_dark'])    # Set background color
    game['root'].iconbitmap(r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\MATHS-QUIZ\assets\ui\icon.ico")  # Set window icon
    setup_audio()                                                # Initialize audio subsystem and load sounds
    load_all_images()                                            # Load images and GIF frames
    play_music('home_music')                                     # Start background music for home
    start_screen()                                               # Show the start screen UI
    game['root'].mainloop()                                      # Enter Tkinter main loop

# --- IMAGE LOADING ---
# Load all static and animated images
def load_all_images():
    for name, (path, size) in IMAGE_ASSET_LIST.items():
        try:
            img = Image.open(path)
            img = img.resize(size)
            game['images'][name] = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading {name}: {e}")
    
    # Load GIF animations as frame sequences
    for name, path in BACKGROUND_PATHS.items():
        try:
            gif = Image.open(path)
            game['images'][f'{name}_frames'] = [
                ImageTk.PhotoImage(frame.copy().resize((800, 750))) 
                for frame in ImageSequence.Iterator(gif)
            ]
        except Exception as e:
            print(f"Error loading GIF {name}: {e}")

# Clear screen and reset widgets
def clear_screen():
    if game.get('timer_id'):
        try:
            game['root'].after_cancel(game['timer_id'])
        except:
            pass
    game['timer_running'] = False
    for widget in game['root'].winfo_children():
        widget.destroy()

# --- AUDIO SETUP ---
# Initialize pygame mixer and load sounds
def setup_audio():
    try:
        pygame.mixer.init()
        game['sounds'] = {}
        for sound_name, sound_path in AUDIO_ASSET_PATHS.items():
            try:
                if 'music' in sound_name:
                    game['sounds'][sound_name] = sound_path
                else:
                    game['sounds'][sound_name] = pygame.mixer.Sound(sound_path)
            except Exception as e:
                print(f"Error loading audio {sound_name}: {e}")
    except Exception as e:
        print(f"Pygame mixer error: {e}")

# Wrapper to play sound when button is clicked
def button_click_sound(command):
    def wrapper(*args, **kwargs):
        play_sound_effect('button_click')
        return command(*args, **kwargs)
    return wrapper

# Play background music on loop
def play_music(music_name):
    stop_music()
    if music_name in game.get('sounds', {}) and isinstance(game['sounds'][music_name], str):
        try:
            pygame.mixer.music.load(game['sounds'][music_name])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except:
            pass

# Stop current music
def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

# Play sound effect once
def play_sound_effect(sound_name):
    sound = game.get('sounds', {}).get(sound_name)
    if isinstance(sound, pygame.mixer.Sound):
        sound.play()

# Confirm exit with dialog
def confirm_exit():
    answer = messagebox.askyesno("TERMINATE", "End Quiz? All progress will be lost!")
    if answer:
        game['root'].quit()

# --- START SCREEN ---
# Display home screen with animated background
def start_screen():
    clear_screen()
    start_frame = Frame(game['root'])
    start_frame.pack(fill=BOTH, expand=True)

    # Animate background GIF
    frames = game['images'].get('home_frames', [])
    bg_label = Label(start_frame)
    bg_label.pack(fill="both", expand=True)

    def animate(index=0):
        if frames:
            bg_label.config(image=frames[index])
            game['root'].after(25, animate, (index + 1) % len(frames))
    animate(0)

    # Title image
    if 'home_title_img' in game['images']:
        title_label = Label(start_frame, image=game['images']['home_title_img'], 
                            bg=NEON_COLORS['background_dark'], borderwidth=0)
        title_label.place(relx=0.5, rely=0.30, anchor="center")

    # Play button
    start_button = Button(start_frame, image=game['images']['play_button'], 
                         bg=NEON_COLORS['background_dark'], 
                         activebackground=NEON_COLORS['background_dark'],
                         borderwidth=0, highlightthickness=0, cursor="hand2", 
                         command=button_click_sound(menu))
    start_button.place(relx=0.74, rely=0.72, anchor="center")

    # Instructions popup window
    def show_instructions():
        instruction_window = Toplevel(game['root'])
        instruction_window.title("📖 MATH QUIZ INSTRUCTION")
        instruction_window.geometry("700x750")
        instruction_window.resizable(False, False)
        instruction_window.configure(bg=NEON_COLORS['background_dark'])

        main_container = Frame(instruction_window, bg=NEON_COLORS['background_dark'], 
                              highlightbackground=NEON_COLORS['neon_cyan'], 
                              highlightthickness=3)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Header
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
        
        # Instructions content
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
        
        Button(close_frame, text="✖ CLOSE INSTRUCTIONS", 
               command=instruction_window.destroy,
               font=('Courier', 14, 'bold'), 
               bg=NEON_COLORS['neon_magenta'], 
               fg=NEON_COLORS['background_dark'],
               activebackground=NEON_COLORS['neon_cyan'],
               cursor='hand2', 
               padx=30, pady=15,
               relief=RAISED,
               bd=3).pack(pady=15)

    # Instructions button
    instruction_button = Button(start_frame, 
                               image=game['images']['instructions_button'], 
                               bg=NEON_COLORS['background_dark'], 
                               activebackground=NEON_COLORS['background_dark'],
                               borderwidth=0, highlightthickness=0, cursor="hand2",
                               command=button_click_sound(show_instructions))
    instruction_button.place(relx=0.07, rely=0.07, anchor="center")

    # Exit button
    exit_button = Button(start_frame, image=game['images']['quit_button_home'], 
                        bg=NEON_COLORS['background_dark'], 
                        activebackground=NEON_COLORS['background_dark'],
                        borderwidth=0, highlightthickness=0, cursor="hand2",
                        command=button_click_sound(confirm_exit))
    exit_button.place(relx=0.93, rely=0.07, anchor="center")

# --- MENU SCREEN ---
# Display difficulty selection menu
def menu():
    stop_music()
    play_music('home_music')
    clear_screen()

    main_frame = Frame(game['root'], bg=NEON_COLORS['background_dark'])
    main_frame.pack(fill=BOTH, expand=True)

    # Animate menu background
    frames = game['images'].get('menu_frames', [])
    label = Label(main_frame)
    label.pack(fill="both", expand=True)
    
    def animate(index=0):
        if frames:
            label.config(image=frames[index])
            game['root'].after(50, animate, (index + 1) % len(frames))
    animate()

    # Title box
    box = Frame(main_frame, bg=NEON_COLORS['background_dark'], bd=3, relief=RIDGE, 
                highlightbackground=NEON_COLORS['neon_magenta'])
    box.place(relx=0.5, rely=0.3, anchor="center")
    
    if 'menu_title' in game['images']:
        l1 = Label(box, image=game['images']['menu_title'], 
                  bg=NEON_COLORS['background_dark'])
        l1.pack()
    
    # Easy difficulty button
    button1 = Frame(main_frame, bg='#9C86D5', width=200, height=250)
    button1.place(relx=0.35, rely=0.83, anchor="center")

    easy_button = Button(button1, image=game['images']['easy_button'], 
                        bg='#9C86D5', 
                        activebackground='#2C1F4A',
                        borderwidth=0, highlightthickness=0, cursor="hand2", 
                        command=button_click_sound(lambda: start_quiz(1)))
    easy_button.pack(pady=5)

    # Medium difficulty button
    button2 = Frame(main_frame, bg='#9C86D5', width=200, height=250)
    button2.place(relx=0.5, rely=0.83, anchor="center")
    
    medium_button = Button(button2, image=game['images']['medium_button'], 
                          bg='#9C86D5', 
                          activebackground='#2C1F4A',
                          borderwidth=0, highlightthickness=0, cursor="hand2", 
                          command=button_click_sound(lambda: start_quiz(2)))
    medium_button.pack(pady=5)
    
    # Hard difficulty button
    button3 = Frame(main_frame, bg='#9C86D5', width=200, height=250)
    button3.place(relx=0.65, rely=0.83, anchor="center")
    
    hard_button = Button(button3, image=game['images']['hard_button'], 
                        bg='#9C86D5', 
                        activebackground='#2C1F4A',
                        borderwidth=0, highlightthickness=0, cursor="hand2", 
                        command=button_click_sound(lambda: start_quiz(3)))
    hard_button.pack(pady=5)
    
    # Exit and return buttons
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
# Generate random numbers based on difficulty level
def random_nums():
    level = game['level']
    if level == 1:
        return random.randint(1, 9), random.randint(1, 9)
    if level == 2:
        return random.randint(10, 99), random.randint(10, 99)
    return random.randint(1000, 9999), random.randint(1000, 9999)

# Initialize quiz with selected difficulty
def start_quiz(level):
    stop_music()
    game.update({
        'level': level, 'question_num': 0, 'score': 0, 'streak': 0, 'streak_bonus': 0,
        'chances': 2, 'time_taken': [], 'question_start_time': 0,
        'answered_questions': 0, 'combo_multiplier': 1.0, 'shield_active': False
    })

    # Set difficulty parameters
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

# Load next question or end game
def next_question():
    if game['question_num'] >= 10 or game['lives'] <= 0:
        results()
        return

    game['question_num'] += 1
    game['chances'] = 2
    game['countdown'] = game['time_limit']
    game['timer_running'] = True
    game['num1'], game['num2'] = random_nums()
    game['operator'] = random.choice(['+', '-'])
    game['ans'] = game['num1'] + game['num2'] if game['operator'] == '+' else game['num1'] - game['num2']
    game['question_start_time'] = time.time()
    show_q()

# --- QUESTION SCREEN ---
# Display question UI with timer and input field
def show_q():
    clear_screen()
    f = Frame(game['root'], bg=NEON_COLORS['background_dark'])
    f.pack(fill="both", expand=True)

    # Background image for difficulty
    bg_key = game.get('bg_image', 'easy_bg')
    if bg_key in game['images']:
        bg_label = Label(f, image=game['images'][bg_key])
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Top bar with score and timer
    top = Frame(f, bg='#2C1F4A', height=50)
    top.pack(fill=X, side=TOP)
    top.pack_propagate(False)
    
    Label(top, text=f"💰 {game['score']}/100", font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_yellow'], bg='#2C1F4A').pack(side=LEFT, padx=20, pady=10)
    
    game['timer_label'] = Label(top, text=f"⏱ {game['countdown']}s", 
                               font=('Courier', 18, 'bold'), 
                               fg=NEON_COLORS['neon_cyan'], bg='#2C1F4A')
    game['timer_label'].pack(side=LEFT, padx=150, pady=10)
    
    # Lives display
    max_lives = 3 if game['level'] < 3 else 2
    lives_display = "💖" * game['lives'] + "🖤" * (max_lives - game['lives'])
    Label(top, text=lives_display, font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg='#2C1F4A').pack(side=RIGHT, padx=20, pady=10)

    # Countdown timer function
    def tick_timer():
        if not game['timer_running']:
            return
        
        if game['countdown'] <= 0:
            game['timer_running'] = False
            handle_timeout()
            return
        
        game['countdown'] -= 1
        
        try:
            color = NEON_COLORS['neon_yellow'] if game['countdown'] <= 5 else NEON_COLORS['neon_cyan']
            game['timer_label'].config(text=f"⏱ {game['countdown']}s", fg=color)
        except:
            return
        
        game['timer_id'] = game['root'].after(1000, tick_timer)
    
    tick_timer()
    
    # Question display area
    question_frame = Frame(f, bg=NEON_COLORS['background_dark'])
    question_frame.pack(pady=60)
    
    Label(question_frame, text=f"QUESTION {game['question_num']}/10", 
          font=("Courier", 14, "bold"), fg=NEON_COLORS['neon_cyan'], 
          bg=NEON_COLORS['background_dark']).pack(pady=(0, 10))
    
    question_display = Frame(question_frame, bg=NEON_COLORS['background_dark'], bd=5, 
                            relief=SOLID, highlightbackground=NEON_COLORS['neon_cyan'], 
                            highlightthickness=2)
    question_display.pack(padx=20, pady=10)
    
    # Color operator based on type
    op_col = NEON_COLORS['neon_cyan'] if game['operator'] == '+' else NEON_COLORS['neon_magenta']
    
    # Equation display
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

    # Input area
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

    # Submit button
    submit_frame = Frame(f, bg=NEON_COLORS['background_dark'])
    submit_frame.pack(pady=10)
    
    Button(submit_frame, image=game['images']['submit_button'], 
           bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(check)).pack()

    # Display attempt status
    if game['chances'] == 1:
        Label(f, text="⚠️ Second Attempt: 5 Credits", font=("Courier", 12, "bold"), 
              fg=NEON_COLORS['neon_yellow'], bg=NEON_COLORS['background_dark']).pack(pady=5)
    
    # Display streak/combo status
    if game['streak'] >= 3:
        streak_text = f"🔥 {game['streak']} Streak!"
        if game['level'] == 3:
            streak_text = f"COMBO x{game['combo_multiplier']:.1f}!"
        Label(f, text=streak_text, font=("Courier", 12, "bold"), 
              fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).pack(pady=5)
        
    # Quit and return buttons
    Button(f, image=game['images']['quit_button_q'], 
           bg=NEON_COLORS['background_dark'],
           activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(confirm_exit)).place(relx=0.95, rely=0.95, anchor="center")

    Button(f, image=game['images']['return_button'], 
           bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(lambda: confirm_return())).place(relx=0.055, rely=0.95, anchor="center")

# Handle timeout when timer reaches zero
def handle_timeout():
    game['timer_running'] = False
    elapsed = time.time() - game['question_start_time']
    game['time_taken'].append(round(elapsed, 2))
    reset_streak()
    lose_life(is_timeout=True)

# Confirm return to menu
def confirm_return():
    game['timer_running'] = False
    answer = messagebox.askyesno("ABORT", "Return to menu? Progress will be lost!")
    if answer:
        menu()
    else:
        game['timer_running'] = True

# Validate and check user answer
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

# Reset streak counter
def reset_streak():
    game['streak'] = 0
    game['combo_multiplier'] = 1.0

# Deduct life from player
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

# Check if user answer is correct
def check_ans(user):
    elapsed = time.time() - game['question_start_time']
    
    if user == game['ans']:
        play_sound_effect('correct')
        game['answered_questions'] += 1
        game['time_taken'].append(round(elapsed, 2))
        game['streak'] += 1
        
        # Award points based on attempt number
        points = 10 if game['chances'] == 2 else 5
        
        # Calculate streak bonus
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
        
        # Allow second attempt or lose life
        if game['chances'] > 0:
            messagebox.showwarning("Wrong", "❌ One more try (5 credits)")
            game['timer_running'] = True
            show_q()
        else:
            game['time_taken'].append(round(elapsed, 2))
            lose_life(is_timeout=False)

# --- RESULTS SCREEN ---
# Display final score and stats
def results():
    game['timer_running'] = False
    clear_screen()

    score = game['score']
    
    # Determine grade based on score
    if score >= 90: grade, msgg = "S", "PHENOMENAL!"
    elif score >= 80: grade, msgg = "A+", "EXCELLENT!"
    elif score >= 70: grade, msgg = "A", "GREAT JOB!"
    elif score >= 60: grade, msgg = "B", "GOOD WORK!"
    elif score >= 50: grade, msgg = "C", "KEEP TRYING!"
    else: grade, msgg = "F", "TRY AGAIN!"

    # Play victory or defeat music based on score
    if score >= 60:
        stop_music()
        play_music('victory_music')
        frames_key = 'win_frames'
    else:
        stop_music()
        play_music('defeat_music')
        frames_key = 'fail_frames'

    # Main frame
    f = Frame(game['root'], bg=NEON_COLORS['background_dark'], width=800, height=750)
    f.place(x=0, y=0)

    # Animate background
    frames = game['images'].get(frames_key, [])
    bg_label = Label(f)
    bg_label.place(x=0, y=0, width=800, height=750)
    
    def animate_bg(index=0):
        if frames:
            bg_label.config(image=frames[index])
            bg_label.lower()
            game['root'].after(80, animate_bg, (index + 1) % len(frames))
    animate_bg()
    
    # Results display box
    mini_frame = Frame(f, width=450, height=550, bg=NEON_COLORS['background_dark'], 
                      highlightbackground=NEON_COLORS['neon_cyan'], highlightthickness=2)
    mini_frame.place(relx=0.5, rely=0.5, anchor="center")
    mini_frame.pack_propagate(False)

    if 'result_box' in game['images']:
        box_bg = Label(mini_frame, image=game['images']['result_box'])
        box_bg.place(x=0, y=0, relwidth=1, relheight=1)

    if 'card_frame' in game['images']:
        card = Label(mini_frame, image=game['images']['card_frame'], 
                    bg='#8C1345', bd=0)
        card.place(relx=0.5, rely=0.47, anchor="center")

    # Score display
    Label(mini_frame, text="FINAL CREDITS", font=("Courier", 16, "bold"), 
          fg=NEON_COLORS['neon_cyan'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.20, anchor="center")
    
    score_display = Frame(mini_frame, bg=NEON_COLORS['background_dark'], relief=SUNKEN, bd=2, 
                         width=180, height=90, highlightbackground=NEON_COLORS['neon_yellow'], 
                         highlightthickness=3)
    score_display.place(relx=0.5, rely=0.32, anchor="center")
    score_display.pack_propagate(False)
    
    Label(score_display, text=str(score), font=("Courier", 42, "bold"), 
          fg=NEON_COLORS['neon_yellow'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.44, anchor="center")

    Label(score_display, text="/ 100 Credits", font=("Courier", 11), 
          fg=NEON_COLORS['text_light'], bg='#181338').place(relx=0.5, rely=0.88, anchor="center")

    # Streak bonus display
    Label(mini_frame, text="STREAK BONUS", font=("Courier", 12, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.45, anchor="center")
    
    bonus_display = Frame(mini_frame, bg=NEON_COLORS['background_dark'], relief=SUNKEN, bd=2, 
                         width=120, height=50, highlightbackground=NEON_COLORS['neon_magenta'], 
                         highlightthickness=2)
    bonus_display.place(relx=0.5, rely=0.52, anchor="center")
    bonus_display.pack_propagate(False)
    
    Label(bonus_display, text=f"+{game['streak_bonus']}", font=("Courier", 24, "bold"), 
          fg=NEON_COLORS['neon_magenta'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.5, anchor="center")

    # Grade display
    grade_box = Frame(mini_frame, bg=NEON_COLORS['neon_magenta'], relief=RAISED, bd=3, 
                     width=100, height=60)
    grade_box.place(relx=0.5, rely=0.62, anchor="center")
    grade_box.pack_propagate(False)
    
    Label(grade_box, text=grade, font=("Courier", 30, "bold"), 
          fg=NEON_COLORS['background_dark'], bg=NEON_COLORS['neon_magenta']).place(relx=0.5, rely=0.51, anchor="center")

    # Message display
    Label(mini_frame, text=msgg, font=("Courier", 12, "bold"), 
          fg=NEON_COLORS['neon_cyan'], bg=NEON_COLORS['background_dark']).place(relx=0.5, rely=0.72, anchor="center")

    # Statistics display
    record_frame = Frame(mini_frame, width=400, height=100)
    record_frame.place(relx=0.5, rely=0.87, anchor="center")
    record_frame.pack_propagate(False)

    if 'record_frame' in game['images']:
        Label(record_frame, image=game['images']['record_frame'], 
              bg='#8C1345', bd=0).place(x=0, y=0, relwidth=1, relheight=1)

    # Calculate statistics
    questions_answered = game.get('answered_questions', 0)
    lives_remaining = game.get('lives', 0)
    missed_questions = 10 - questions_answered
    average_time = round(sum(game['time_taken']) / len(game['time_taken']), 2) if game['time_taken'] else 0

    max_lives = 3 if game['level'] < 3 else 2
    stats_text = f"Questions: {questions_answered}/10\nMissed: {missed_questions}\nLives: {lives_remaining}/{max_lives}\nAvg Time: {average_time}s"
    
    Label(record_frame, text=stats_text, font=("Courier", 10, "bold"), 
          fg=NEON_COLORS['text_light'], bg=NEON_COLORS['background_dark'], 
          justify="center").place(relx=0.5, rely=0.5, anchor="center")

    # Buttons: Play again and quit
    Button(f, image=game['images']['play_again_button'], 
           bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(menu)).place(relx=0.43, rely=0.93, anchor="center")

    Button(f, image=game['images']['quit_button_home'], 
           bg=NEON_COLORS['background_dark'], 
           activebackground=NEON_COLORS['background_dark'], 
           borderwidth=0, highlightthickness=0, cursor="hand2", 
           command=button_click_sound(game['root'].quit)).place(relx=0.57, rely=0.93, anchor="center")


if __name__ == "__main__":
    main()