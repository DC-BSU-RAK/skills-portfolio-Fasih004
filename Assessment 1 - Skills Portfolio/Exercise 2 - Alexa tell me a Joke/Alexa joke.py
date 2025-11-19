# --- IMPORTS ---
from tkinter import *                           # GUI framework
from tkinter import messagebox                  # Dialog boxes
from PIL import Image, ImageTk, ImageSequence   # Image processing
import random                                   # Random joke selection
import pygame                                   # Audio library

# --- MAIN WINDOW ---
joke_app = Tk()
joke_app.title("Alexa Tell Me A Joke")
joke_app.geometry("1000x600") 
joke_app.resizable(FALSE, FALSE)
joke_app.config(bg="#1b1b1b")
joke_app.iconbitmap(r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\Smiley.ico")

# --- JOKE DICTIONARY ---
# Global application state tracker
joke = {
    'current_setup': '',            # Current joke setup text
    'current_punchline': '',        # Current joke punchline text
    'setups': [],                   # List of joke setups
    'punchlines': [],               # List of joke punchlines
    'current_index': [0],           # Current joke index in list
    'typewriter_job': None,         # Timer ID for typewriter animation
    'char_index': 0,                # Current character position in typewriter
    'sounds': {},                   # Dictionary storing loaded audio
    'images': {},                   # Dictionary storing loaded images
    'joke_started': False,          # Track if first joke has been told
    'punchline_shown': False,       # Track if punchline is currently displayed
}

# --- ASSET PATHS ---
# Image file paths and dimensions
IMAGE_PATHS = {
    'background': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\main_bg.png", (1000, 600)),
    'alexa_btn': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\alexa_btn.png", (220, 70)),
    'punchline_btn': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\punchline_btn.png", (220, 70)),
    'next_btn': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\next_btn.png", (220, 70)),
    'quit_btn': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\quit_btn.png", (130, 70)),
    'joke_frame': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\ui\joke_frame.png", (555, 415)),
}

# Audio file paths
AUDIO_PATHS = {
    'bg_music': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\audios\main_bg.wav"),
    'btn_click': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\audios\button.wav"),
    'laugh': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\audios\laughing.wav"),
    'drumroll': (r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\assets\audios\drumroll.wav"),
}

# --- AUDIO SETUP ---
# Initialize audio system and prepare sound files
def setup_audio():
    try:
        pygame.mixer.init()
        print("Audio system ready")
        joke['sounds'] = {}
        
        # Load each audio file into the sounds dictionary
        for audio_name, audio_path in AUDIO_PATHS.items():
            try:
                # Background music stored as path string for pygame.mixer.music
                if 'music' in audio_name:
                    joke['sounds'][audio_name] = audio_path
                    print(f"Music file prepared: {audio_name}")
                # Sound effects loaded as Sound objects
                else:
                    joke['sounds'][audio_name] = pygame.mixer.Sound(audio_path)
                    print(f"Sound effect ready: {audio_name}")
            except FileNotFoundError:
                print(f"Audio file missing: {audio_path}")
                joke['sounds'][audio_name] = None
            except Exception as e:
                print(f"Failed to load audio {audio_name}: {e}")
                joke['sounds'][audio_name] = None
    except Exception as e:
        print(f"Audio initialization failed: {e}")


# Wrapper function to play sound when button is activated
def button_click_sound(cmd_function, audio_name):
    def wrapper_func(*args, **kwargs):
        trigger_sound(audio_name)
        return cmd_function(*args, **kwargs)
    return wrapper_func


# Start background music loop
def play_bg_music():
    try:
        bg_music_path = joke['sounds'].get('bg_music')
        if bg_music_path and isinstance(bg_music_path, str):
            pygame.mixer.music.load(bg_music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            print("Background music started")
        else:
            print("Background music unavailable")
    except Exception as e:
        print(f"Music playback error: {e}")


# Stop all background music
def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass


# Trigger a sound effect
def trigger_sound(audio_name):
    audio_obj = joke['sounds'].get(audio_name)
    if isinstance(audio_obj, pygame.mixer.Sound):
        audio_obj.set_volume(0.5)
        audio_obj.play()
        print(f"Sound triggered: {audio_name}")
    else:
        print(f"Sound unavailable: {audio_name}")


# Initialize audio system
setup_audio()
# Start background music
play_bg_music()


# --- JOKE DATA ---
# Load jokes from text file into separate lists
def load_jokes():
    # Initialize empty lists for joke components
    setups = []
    punchlines = []
    
    try:
        # Open and read all lines from file
        with open(r"C:\Users\fasih\Documents\GitHub\skills-portfolio-Fasih004\Assessment 1 - Skills Portfolio\Exercise 2 - Alexa tell me a Joke\randomJokes.txt") as file_handler:
            lines = file_handler.readlines()
        
        # Parse each line for setup and punchline
        for l in lines:
            if "?" in l:
                data = l.strip().split("?", 1)
                setup = data[0] + "?"
                punchline = data[1].strip()
                
                # Only add if both setup and punchline are not empty
                if setup and punchline:
                    setups.append(setup)
                    punchlines.append(punchline)
        
        print(f"Jokes loaded successfully: {len(setups)} jokes")
        
    except FileNotFoundError:
        messagebox.showerror("Error", "randomJokes.txt file not found!")
        joke_app.quit()
        return
    
    # Save jokes to joke dictionary
    joke['setups'] = setups
    joke['punchlines'] = punchlines
    joke['current_index'] = [0]
    
# Load jokes on startup
load_jokes()

# --- IMAGE LOADING ---
# Load all static images into memory
def load_all_images():
    for img_name, (path, size) in IMAGE_PATHS.items():
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            joke['images'][img_name] = ImageTk.PhotoImage(img)
            print(f"Image loaded: {img_name}")
        except:
            joke['images'][img_name] = None
            print(f"Image not found: {img_name}")


# Load all images on startup
load_all_images()


# --- FUNCTIONS ---
# Confirm exit dialog
def confirm_exit():
    result = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if result:
        stop_music()
        joke_app.quit()


# --- UI SETUP ---
# Main frame for background
main_frame = Frame(joke_app)
main_frame.pack(fill=BOTH, expand=True)

# Background image
joke['images'].get('background')
bg_label = Label(main_frame, image=joke['images']['background'])
bg_label.image = joke['images']['background']
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Right side - Joke display frame 
if joke['images'].get('joke_frame'):
    # Display joke frame image
    joke_frame_label = Label(bg_label, image=joke['images']['joke_frame'], bg='#040c21')
    joke_frame_label.place(relx=0.69, rely=0.57, anchor="center")
    
    # Setup label directly on image 
    setup_label = Label(
        joke_frame_label,
        text="",
        wraplength=280,
        font=("Arial", 14, "bold"),
        fg="#000000",
        bg='#6C8DC7',
        justify=CENTER,
        pady=10
    )
    setup_label.place(relx=0.5, rely=0.30, anchor="center", width=300, height=100)
    
    # Punchline label directly on image 
    punchline_label = Label(
        joke_frame_label,
        text="",
        wraplength=280,
        font=("Arial", 16, "bold"),
        fg="#6b4811",
        bg="#6C8DC7",
        justify=CENTER,
        pady=10
    )
    punchline_label.place(relx=0.5, rely=0.70, anchor="center", width=300, height=100)
    
else:    
    joke_display_container = Frame(bg_label, bg='#6C8DC7', bd=5, relief=RIDGE)
    joke_display_container.place(relx=0.65, rely=0.50, anchor="center", width=540, height=440)

    # Joke content area
    joke_content_frame = Frame(joke_display_container, bg='#6C8DC7')
    joke_content_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)


# Store labels in joke dictionary for access
joke['setup_label'] = setup_label
joke['punchline_label'] = punchline_label


# --- JOKE LOGIC ---
# Display random joke setup
def tell_joke():
    # Only work if this is the first time or coming from next_joke
    if not joke['joke_started']:
        if joke['setups']:
            # Select random joke
            joke['current_index'][0] = random.randint(0, len(joke['setups']) - 1)
            joke['setup_label'].config(
                text=joke['setups'][joke['current_index'][0]],
                font=("Arial", 16, "bold"),
                fg="#000000"
            )
            joke['punchline_label'].config(text="")
            joke['punchline_shown'] = False
            joke['joke_started'] = True  # Mark that first joke has been started
    else:
        # If already started, inform user to use next button
        messagebox.showinfo("Info", "Please use 'Next Joke' button for more jokes!")


# Show punchline with typewriter effect
def show_punchline():
    if joke['setup_label'].cget("text") == "":
        messagebox.showwarning("Wait!", "Please click 'Alexa Tell Me a Joke' button first!")
    elif joke['punchline_shown']:
        messagebox.showinfo("Info", "Punchline already shown! Click 'Next Joke' for another joke.")
    elif joke['punchlines']:
        # Prepare for typewriter effect
        joke['current_punchline'] = joke['punchlines'][joke['current_index'][0]]
        joke['char_index'] = 0
        joke['punchline_label'].config(text="")
        
        # Play drumroll sound
        trigger_sound('drumroll')
        
        # Start typewriter effect after drumroll
        joke_app.after(2000, type_character)
        joke['punchline_shown'] = True


# Type one character at a time (typewriter effect)
def type_character():
    if joke['char_index'] < len(joke['current_punchline']):
        current_text = joke['punchline_label'].cget("text")
        current_text += joke['current_punchline'][joke['char_index']]
        joke['punchline_label'].config(text=current_text)
        joke['char_index'] += 1
        joke['typewriter_job'] = joke_app.after(50, type_character)
    else:
        # Typewriter complete - play laugh sound
        trigger_sound('laugh')


# Load next joke
def next_joke():
    if not joke['joke_started']:
        messagebox.showwarning("Wait!", "Please click 'Alexa Tell Me a Joke' button first!")
        return
    
    if joke['setups']:
        # Get a new random joke that's different from current
        new_index = random.randint(0, len(joke['setups']) - 1)
        
        # Ensure to get a different joke i
        attempts = 0
        while new_index == joke['current_index'][0] and len(joke['setups']) > 1 and attempts < 10:
            new_index = random.randint(0, len(joke['setups']) - 1)
            attempts += 1
        
        joke['current_index'][0] = new_index
        
        # Update setup label
        joke['setup_label'].config(
            text=joke['setups'][joke['current_index'][0]],
            font=("Arial", 16, "bold"),
            fg="#000000"
        )
        
        # Clear punchline
        joke['punchline_label'].config(text="")
        joke['punchline_shown'] = False


# --- BUTTON CREATION ---
# Tell Joke Button
if joke['images'].get('alexa_btn'):
    tell_btn = Button(
        image=joke['images']['alexa_btn'],
        command=button_click_sound(tell_joke, 'btn_click'),
        borderwidth=0,
        cursor="hand2",
        bg='#040c21',
        activebackground='#040c21'
    )
    tell_btn.place(relx=0.24, rely=0.42, anchor="center")

# Show Punchline Button
if joke['images'].get('punchline_btn'):
    punchline_btn = Button(
        image=joke['images']['punchline_btn'],
        command=button_click_sound(show_punchline, 'btn_click'),
        borderwidth=0,
        cursor="hand2",
        bg='#040c21',
        activebackground='#040c21'
    )
    punchline_btn.place(relx=0.15, rely=0.57, anchor="center")

# Next Joke Button
if joke['images'].get('next_btn'):
    next_btn = Button(
        image=joke['images']['next_btn'],
        command=button_click_sound(next_joke, 'btn_click'),
        borderwidth=0,
        cursor="hand2",
        bg='#040c21',
        activebackground='#040c21'
    )
    next_btn.place(relx=0.24, rely=0.71, anchor="center")

# Quit Button
if joke['images'].get('quit_btn'):
    quit_btn = Button(
        image=joke['images']['quit_btn'],
        command=button_click_sound(confirm_exit, 'btn_click'),
        borderwidth=0,
        cursor="hand2",
        bg='#040c21',
        activebackground='#040c21'
    )
    quit_btn.place(relx=0.32, rely=0.86, anchor="center")

# Start the application
joke_app.mainloop()
