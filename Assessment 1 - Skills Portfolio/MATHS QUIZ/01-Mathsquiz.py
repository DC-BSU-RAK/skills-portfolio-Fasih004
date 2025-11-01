from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageSequence
import pygame
import time

class SpaceQuizGame:
    def __init__(app, main_window):
        """Initialize game window and load all assets"""
        app.main_window = main_window
        app.main_window.title("Quiz Pixel Spaceship")
        app.main_window.geometry("800x600")
        app.main_window.resizable(False, False)
        
        # Game State Variables
        app.difficulty = None           
        app.current_question = 0        
        app.total_questions = 10        
        app.player_score = 0            
        app.lives_remaining = 3         
        app.attempts_used = 0           
        app.correct_streak = 0          
        app.time_remaining = 30         
        app.timer_id = None             
        app.game_start_time = None      
        
        # Question Variables
        app.number_one = 0              
        app.number_two = 0              
        app.operation = ""              
        app.correct_answer = 0          
        
        # Power-up Variables (Moderate Mode)
        app.shield_active = False       
        app.time_freeze_active = False  
        app.hint_available = False      
        app.powerup_counter = 0         
        
        # Multiplier Variables (Advanced Mode)
        app.combo_multiplier = 1.0      
        
        # UI Widget References
        app.bg_label = None             
        app.timer_label = None          
        app.lives_label = None          
        app.score_label = None          
        app.streak_label = None         
        app.answer_entry = None         
        
        # Asset Storage
        app.bg_frames = {}              
        app.button_images = {}          
        app.ui_images = {}              
        app.grade_images = {}           
        app.badge_images = {}           
        app.powerup_images = {}         
        app.sounds = {}                 
        app.current_bg_name = None      
        app.animation_id = None         
        
        # Achievement Tracking
        app.achievements_unlocked = []  
        app.mistakes_made = 0           
        
        # Background setup
        app.bg_label = Label(main_window)
        app.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Load all assets
        app.load_backgrounds()
        app.load_button_images()
        app.load_ui_elements()
        app.load_grade_images()
        app.load_achievement_badges()
        app.load_powerup_images()
        app.setup_audio()
        
        # Start game
        app.show_home_screen()