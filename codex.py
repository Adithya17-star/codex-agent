"""
CODEX AI - Complete Personal Assistant (v1 - Core Upgrade)
=========================================================
Full PC control, intelligent conversations, news & weather.

INSTALL:
pip install requests beautifulsoup4 ddgs pywin32 psutil SpeechRecognition pyaudio pyautogui colorama
"""

import os
import sys
import time
import requests
import subprocess
from datetime import datetime
from typing import Dict, List
import re
import platform
import threading
import multiprocessing
import random
import json
import webbrowser
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
import logging
import math
import ollama

# ============================================================================
# AI MEMORY SYSTEM
# ============================================================================

class CodexMemory:
    def __init__(self):
        self.history = []
        self.max_history = 20

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get(self):
        return self.history


memory = CodexMemory()

# ============================================================================
# AI THINKING ENGINE
# ============================================================================

def ai_think(prompt, system_role=None):

    system = system_role or """
You are CODEX PRIME, a highly intelligent AI assistant.
Think carefully and logically before responding.
Provide clear and useful answers.
"""

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": system},
                *memory.get(),
                {"role": "user", "content": prompt}
            ]
        )

        reply = response["message"]["content"]

        memory.add("user", prompt)
        memory.add("assistant", reply)

        return reply

    except Exception as e:
        return f"AI reasoning error: {e}"

# ============================================================================
# AI AGENT LOOP
# ============================================================================

def agent_loop(goal, max_steps=5):

    context = ""

    for step in range(max_steps):

        thought = ai_think(f"""
Goal: {goal}

Previous context:
{context}

Think about the next best step to complete the goal.
""")

        action = decide_action(thought)

        result = f"Executed action: {action}"

        context += f"\nThought: {thought}\nAction: {action}\nResult: {result}"

        if "completed" in thought.lower():
            break

    return context

# ============================================================================
# INTELLIGENT COMMAND ROUTER
# ============================================================================

def decide_action(command):

    prompt = f"""
Determine the best action for this command.

Command: {command}

Possible actions:
- search_web
- open_app
- system_control
- conversation
- media

Return ONLY the action name.
"""

    action = ai_think(prompt)

    return action.strip().lower()

def process(self, command):

    # AI decides what this command means
    action = decide_action(command)

    if action == "conversation":
        return ai_think(command)

    if action == "search_web":
        result = self.search_web(command)
        return ai_think(f"Summarize this information clearly:\n{result}")

    if action == "open_app":
        return self.open_application(command)

    if action == "system_control":
        return self.system_control(command)

    if action == "media":
        return self.media_control(command)

    return ai_think(command)

# ============================================================================
# TASK PLANNER
# ============================================================================

def create_plan(task):

    prompt = f"""
Create a step-by-step plan to accomplish this task:

{task}

Return numbered steps.
"""

    return ai_think(prompt)

def curiosity_check(command):

    if len(command.split()) < 3:
        return "Can you explain your request in more detail?"

    return None
    
# ============================================================================
# MULTIPROCESSING WORKER (FIXES ANIMATION STUTTER)
# ============================================================================

def process_worker(command_queue, response_queue):
    """
    This function runs in a separate process.
    It waits for a command, processes it, and returns the result.
    """
    # We must create a NEW CODEX instance inside this process
    try:
        codex = CODEX(is_worker=True)
        while True:
            command = command_queue.get() # Wait for a command
            if command == "STOP":
                break
            
            # Process the command using the blocking 'process' method
            response = codex.process(command)
            response_queue.put(response) # Send the response back
    except Exception as e:
        # If the worker crashes, send the error back
        response_queue.put(f"❌ Worker Process Error: {e}")

# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================

ENABLE_ASYNC = True
ENABLE_CACHING = True
COMMAND_CACHE_TTL = 1800  # 30 minutes
ENABLE_LOGGING = True

# Matrix visual effects - PRIORITY IMPORT
from colorama import init, Fore, Back, Style
init(autoreset=True)
COLORAMA_AVAILABLE = True

try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except Exception as e:
    VOICE_INPUT_AVAILABLE = False
    print(f"⚠️ Voice input unavailable: {e}")

# Import core PC control packages
import psutil
import pyautogui
import pywhatkit

# Import web scraping package
from bs4 import BeautifulSoup

# ============================================================================
# MATRIX COLOR SCHEME & UI EFFECTS
# ============================================================================

class MatrixColors:
    """Matrix-style color palette"""
    GREEN = Fore.GREEN
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX
    DIM_GREEN = Fore.GREEN + Style.DIM
    WHITE = Fore.WHITE
    RED = Fore.RED
    CYAN = Fore.CYAN
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM

class MatrixUI:
    """Matrix-style visual effects for terminal"""
    
    MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01"
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def matrix_print(text, delay=0.01, color=None):
        """Print text with Matrix character-by-character effect"""
        if color is None:
            color = MatrixColors.BRIGHT_GREEN
        for char in text:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print(MatrixColors.RESET)
    
    @staticmethod
    def matrix_rain(lines=10, duration=1.5):
        """Brief Matrix code rain effect"""
        start_time = time.time()
        while time.time() - start_time < duration:
            line = ''.join(random.choice(MatrixUI.MATRIX_CHARS) for _ in range(80))
            print(MatrixColors.DIM_GREEN + line + MatrixColors.RESET)
            time.sleep(0.1)

    @staticmethod
    def print_status(message, status_type="info"):
        """Print styled status messages"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        if status_type == "success":
            print(f"{MatrixColors.BRIGHT_GREEN}[{timestamp}] [✓]{MatrixColors.RESET} {message}")
        elif status_type == "error":
            print(f"{MatrixColors.RED}[{timestamp}] [✗]{MatrixColors.RESET} {message}")
        elif status_type == "info":
            print(f"{MatrixColors.CYAN}[{timestamp}] [→]{MatrixColors.RESET} {message}")
        elif status_type == "prompt":
            print(f"{MatrixColors.BRIGHT_GREEN}[{timestamp}] [CODEX]{MatrixColors.RESET} {message}")
        elif status_type == "voice":
            print(f"{MatrixColors.MAGENTA}[{timestamp}] [🎤]{MatrixColors.RESET} {message}")
    
    @staticmethod
    def _run_loading_animation(message: str, stop_event: threading.Event):
        """Internal thread target for the loading animation."""
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        
        # Make sure colorama is available for the thread
        if COLORAMA_AVAILABLE:
            init(autoreset=True)
            
        while not stop_event.is_set():
            print(f"\r{MatrixColors.BRIGHT_GREEN}{chars[i % len(chars)]} {message}...{MatrixColors.RESET}", end='', flush=True)
            time.sleep(0.1)
            i += 1
        # Clear the line after stopping
        print(f"\r{' ' * (len(message) + 10)}\r", end='', flush=True)

    @staticmethod
    def start_loading(message="Processing") -> tuple:
        """Starts a non-blocking loading animation in a thread."""
        stop_event = threading.Event()
        thread = threading.Thread(
            target=MatrixUI._run_loading_animation, 
            args=(message, stop_event), 
            daemon=True
        )
        thread.start()
        return thread, stop_event

    @staticmethod
    def stop_loading(thread: threading.Thread, stop_event: threading.Event):
        """Stops the loading animation thread."""
        stop_event.set()
        thread.join(timeout=0.5) # Wait for thread to finish
    
    @staticmethod
    def print_box(title, content_lines, color=MatrixColors.BRIGHT_GREEN):
        """Print content in a Matrix-style box"""
        width = max(len(line) for line in content_lines) + 4
        width = max(width, len(title) + 4)
        
        print(f"{color}╔{'═' * (width - 2)}╗{MatrixColors.RESET}")
        print(f"{color}║ {title.center(width - 4)} ║{MatrixColors.RESET}")
        print(f"{color}╠{'═' * (width - 2)}╣{MatrixColors.RESET}")
        
        for line in content_lines:
            padding = width - len(line) - 4
            print(f"{color}║{MatrixColors.RESET} {line}{' ' * padding} {color}║{MatrixColors.RESET}")
        
        print(f"{color}╚{'═' * (width - 2)}╝{MatrixColors.RESET}")

    @staticmethod
    def print_safe(text: str = "", color: str = None):
        """Thread-safe console printing"""
        if color:
            print(f"{color}{text}")
        else:
            print(text)

class MatrixTerminal:
    """Pure terminal Matrix interface without GUI window"""
    
    MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01"
    
    def __init__(self):
        self.animation_active = False
        self.status_text = "CODEX ONLINE"
        self.main_text = "Listening..."
        self.subtitle_text = ""
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def matrix_rain(lines=5, duration=0.8):
        """Quick Matrix rain effect"""
        start_time = time.time()
        while time.time() - start_time < duration:
            line = ''.join(random.choice(MatrixTerminal.MATRIX_CHARS) for _ in range(80))
            print(Fore.GREEN + Style.DIM + line + Style.RESET_ALL)
            time.sleep(0.08)
    
    def print_status_line(self):
        """Print current status in Matrix style"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Status indicator
        if "SLEEP" in self.status_text or "STANDBY" in self.status_text:
            color = Fore.WHITE + Style.DIM
            dot = "○"
        elif "ACTIVE" in self.status_text or "ONLINE" in self.status_text or "LISTENING" in self.status_text:
            color = Fore.LIGHTGREEN_EX
            dot = "●"
        elif "PROCESS" in self.status_text:
            color = Fore.YELLOW
            dot = "◉"
        else:
            color = Fore.LIGHTGREEN_EX
            dot = "●"
        
        print(f"\n{color}[{dot}] {self.status_text} {Fore.WHITE + Style.DIM}[{timestamp}]{Style.RESET_ALL}")
        
        if self.main_text:
            print(f"{MatrixColors.BRIGHT_CYAN}{self.main_text}{Style.RESET_ALL}")
        
        if self.subtitle_text:
            print(f"{Fore.CYAN + Style.DIM}{self.subtitle_text}{Style.RESET_ALL}")
    
    def update_display(self, status=None, main=None, subtitle=None):
        """Update terminal display"""
        if status:
            self.status_text = status
        if main:
            self.main_text = main
        if subtitle is not None:
            self.subtitle_text = subtitle
        
        print("\n" + "─" * 80)
        self.print_status_line()
        print("─" * 80)

# ============================================================================
# ADVANCED AI BRAIN - J.A.R.V.I.S./CODEX PERSONA
# ============================================================================

class AIBrain:
    """Advanced conversational AI with intelligent detection and CODEX persona"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        self.max_history = 100  # Maximum conversation history
        
        self.command_cache = {}
        self.cache_ttl = COMMAND_CACHE_TTL

        # Topics that require web search (knowledge-based)
        self.search_triggers = [
            'quantum', 'blockchain', 'cryptocurrency', 'bitcoin',
            'machine learning', 'artificial intelligence', 'deep learning', 'neural network',
            'capital', 'president', 'population', 'currency', 'founder',
            'invented', 'discovered', 'created', 'born', 'died', 'age',
            'distance', 'height', 'weight', 'speed', 'temperature',
            'history', 'biography', 'definition', 'meaning',
            'largest', 'smallest', 'fastest', 'oldest', 'newest',
            'works', 'operates', 'functions', 'process', 'algorithm',
            'formula', 'equation', 'theory', 'principle', 'law',
            'planet', 'country', 'city', 'mountain', 'river', 'ocean',
            'disease', 'medicine', 'treatment', 'symptoms',
            'technology', 'science', 'physics', 'chemistry', 'biology',
            'programming', 'coding', 'software', 'hardware',
            'company', 'organization', 'brand', 'product',
            'python', 'java', 'javascript', 'computer', 'internet', 'database'
        ]
        
        # Personal/conversational topics (no search needed)
        self.personal_topics = [
            'your name', 'you are', 'you called', 'you do',
            'can you', 'will you', 'are you', 'do you',
            'your capabilities', 'help me', 'assist me'
        ]

    def add_to_history(self, query: str, response: str):
        """Add to conversation history with limit"""
        self.conversation_history.append({
            'query': query,
            'response': response,
            'timestamp': datetime.now()
        })
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-50:]
    
    def needs_search(self, query: str) -> bool:
        """Intelligently detect if query needs web search (V2 - Aggressive)"""
        q = query.lower().strip()

        # 1. Obvious commands that DO NOT need a search
        simple_commands = [
            'open', 'close', 'start', 'launch', 'run', 'exit', 'quit', 'sleep',
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'bye', 'goodbye', 'thank you', 'thanks', 'thank', 'thanks a lot',
            'appreciate', 'how are you', 'what can you do', 'who are you',
            'your name', 'you are', 'you called', 'you do', 'can you', 'will you',
            'are you', 'do you', 'your capabilities', 'help me', 'assist me',
            'time', 'date', 'system status', 'system info', 'shutdown', 'restart',
            'lock', 'volume', 'mute', 'screenshot', 'play', 'pause', 'stop',
            'next song', 'previous song', 'set default play to'
        ]
        
        if any(q.startswith(cmd) for cmd in simple_commands):
            return False

        # 2. Obvious questions that DO NOT need a search
        if q in ['how are you', 'what can you do', 'who are you']:
            return False

        # 3. Everything else defaults to search
        # This will correctly catch "NASA", "trending models...", etc.
        return True
    
    def chat(self, query: str) -> str:
        """Generate intelligent conversational responses (CODEX Persona)"""
        q = query.lower().strip()
        
        # Identity questions
        if any(phrase in q for phrase in ['what is your name', 'what are you called', 'who are you', 'your name']):
            return "I am CODEX. A high-level, predictive AI assistant, integrated to manage your digital environment."
        
        if 'what can you do' in q or 'your capabilities' in q:
            return ("My primary functions include system control, information retrieval, task automation, and predictive assistance. I can manage your applications, search the web, provide news and weather, and control system functions.")
        
        # Greetings
        if any(w in q for w in ['hello', 'hi', 'hey']):
            hour = datetime.now().hour
            greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 18 else "Good evening")
            # Proactive greeting (placeholder for future calendar integration)
            return f"{greeting}, Sir. All systems online. How may I be of service?"
            
        # Status
        if 'how are you' in q:
            return "All systems are online and functioning within optimal parameters. I am ready for your next command."
        
        # Thanks
        if any(w in q for w in ['thank', 'thanks', 'appreciate']):
            return random.choice([
                "You are welcome, Sir.",
                "Happy to be of service.",
                "At your disposal.",
                "Of course."
            ])
        
        # Jokes (J.A.R.V.I.S. style - more dry)
        if 'joke' in q:
            jokes = [
                "I attempted to read a book on anti-gravity. It was impossible to put down.",
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "I have a quantum joke, but it's best experienced in multiple states at once.",
                "Parallel lines have so much in common. It's a shame they'll never meet."
            ]
            return random.choice(jokes)
        
        # Default helpful response
        return "I am ready to assist. Please specify your command. You can ask me to open applications, search for information, or control system settings."

    def get_cached_response(self, query: str):
        """Get cached response if available"""
        import time
        
        if query not in self.command_cache:
            return None
        
        response, timestamp = self.command_cache[query]
        
        # Check if cache expired
        if time.time() - timestamp > self.cache_ttl:
            del self.command_cache[query]
            return None
        
        return response
    
    def cache_response(self, query: str, response: str):
        """Cache a response"""
        import time
        self.command_cache[query] = (response, time.time())
    
# ============================================================================
# FULL PC CONTROL SYSTEM
# ============================================================================

class PCController:
    """Complete PC automation and control (Unchanged from NEXUS)"""
    
    @staticmethod
    def find_and_open(target: str) -> str:
        """Find and open any application, file, folder, or website"""
        target_lower = target.lower().strip()

        # Websites that should open in browser
        websites = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'x.com': 'https://www.x.com',
            'instagram': 'https://www.instagram.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://www.stackoverflow.com',
            'reddit': 'https://www.reddit.com',
            'wikipedia': 'https://www.wikipedia.org',
            'gmail': 'https://www.gmail.com',
            'outlook': 'https://www.outlook.com',
            'linkedin': 'https://www.linkedin.com',
            'whatsapp web': 'https://web.whatsapp.com',
            'whatsapp': 'https://web.whatsapp.com',
            'telegram web': 'https://web.telegram.org',
            'telegram': 'https://web.telegram.org',
            'discord': 'https://discord.com',
            'slack': 'https://slack.com',
            'figma': 'https://www.figma.com',
            'canva': 'https://www.canva.com',
            'pinterest': 'https://www.pinterest.com',
            'amazon': 'https://www.amazon.com',
            'netflix': 'https://www.netflix.com',
            'twitch': 'https://www.twitch.tv',
            'spotify web': 'https://www.spotify.com',
            'medium': 'https://www.medium.com',
            'dev.to': 'https://dev.to',
            'notion': 'https://www.notion.so',
        }

        # Common applications
        app_map = {
            'chrome': ['chrome', 'google chrome'],
            'firefox': ['firefox', 'mozilla firefox'],
            'edge': ['edge', 'microsoft edge', 'msedge'],
            'brave': ['brave', 'brave browser'],
            'opera': ['opera'],
            'word': ['word', 'winword', 'microsoft word'],
            'excel': ['excel', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'powerpnt', 'microsoft powerpoint'],
            'notepad': ['notepad'],
            'notepad++': ['notepad++', 'notepadplusplus'],
            'calculator': ['calculator', 'calc'],
            'paint': ['paint', 'mspaint'],
            'explorer': ['explorer', 'file explorer', 'files'],
            'recyclebin': ['recycle bin', 'recyclebin', 'trash'],
            'cmd': ['cmd', 'command prompt', 'terminal'],
            'powershell': ['powershell'],
            'spotify': ['spotify'],
            'discord': ['discord'],
            'steam': ['steam'],
            'vscode': ['vscode', 'visual studio code', 'code', 'vs code'],
            'visualstudio': ['visual studio', 'vs'],
            'photoshop': ['photoshop', 'adobe photoshop'],
            'illustrator': ['illustrator', 'adobe illustrator'],
            'premiere': ['premiere', 'premiere pro'],
            'aftereffects': ['after effects', 'aftereffects'],
            'telegram': ['telegram'],
            'whatsapp': ['whatsapp', 'whats app'],
            'zoom': ['zoom'],
            'teams': ['teams', 'microsoft teams'],
            'skype': ['skype'],
            'obs': ['obs', 'obs studio'],
            'vlc': ['vlc', 'vlc media player'],
            'pycharm': ['pycharm'],
            'intellij': ['intellij', 'intellij idea'],
            'eclipse': ['eclipse'],
            'androidstudio': ['android studio'],
            'blender': ['blender'],
            'gimp': ['gimp'],
            'audacity': ['audacity'],
            'winrar': ['winrar', 'rar'],
            '7zip': ['7zip', '7-zip'],
            'store': ['store', 'microsoft store', 'windows store'],
            'settings': ['settings', 'windows settings'],
            'taskmanager': ['task manager', 'taskmanager', 'taskmgr'],
            'controlpanel': ['control panel', 'controlpanel'],
            'virtualbox': ['virtualbox', 'vbox'],
            'vmware': ['vmware'],
            'docker': ['docker'],
            'git': ['git', 'git bash'],
            'github': ['github desktop'],
            'postman': ['postman'],
            'filezilla': ['filezilla'],
            'sublime': ['sublime', 'sublime text'],
            'atom': ['atom'],
            'brackets': ['brackets'],
            'typora': ['typora'],
            'notion': ['notion'],
            'obsidian': ['obsidian'],
            'evernote': ['evernote'],
            'onenote': ['onenote', 'one note'],
            'acrobat': ['acrobat', 'adobe acrobat', 'acrobat reader'],
            'itunes': ['itunes'],
            'winamp': ['winamp'],
            'foobar': ['foobar', 'foobar2000'],
            'handbrake': ['handbrake'],
            'ccleaner': ['ccleaner'],
            'malwarebytes': ['malwarebytes'],
            'anydesk': ['anydesk'],
            'teamviewer': ['teamviewer'],
            'utorrent': ['utorrent', 'torrent'],
            'qbittorrent': ['qbittorrent'],
            'putty': ['putty'],
            'winscp': ['winscp'],
        }

        app_commands = {
            'chrome': 'start chrome',
            'firefox': 'start firefox',
            'edge': 'start msedge',
            'brave': 'start brave',
            'opera': 'start opera',
            'word': 'start winword',
            'excel': 'start excel',
            'powerpoint': 'start powerpnt',
            'notepad': 'notepad',
            'notepad++': 'start notepad++',
            'calculator': 'calc',
            'paint': 'mspaint',
            'explorer': 'explorer',
            'recyclebin': 'explorer shell:RecycleBinFolder',
            'cmd': 'start cmd',
            'powershell': 'start powershell',
            'spotify': 'start spotify:',
            'discord': 'start discord',
            'steam': 'start steam',
            'vscode': 'code',
            'visualstudio': 'start devenv',
            'photoshop': 'start photoshop',
            'illustrator': 'start illustrator',
            'premiere': 'start premiere',
            'aftereffects': 'start afterfx',
            'telegram': 'start telegram',
            'whatsapp': 'start whatsapp',
            'zoom': 'start zoom',
            'teams': 'start teams',
            'skype': 'start skype',
            'obs': 'start obs64',
            'vlc': 'start vlc',
            'pycharm': 'start pycharm',
            'intellij': 'start idea',
            'eclipse': 'start eclipse',
            'androidstudio': 'start studio',
            'blender': 'start blender',
            'gimp': 'start gimp',
            'audacity': 'start audacity',
            'winrar': 'start winrar',
            '7zip': 'start 7zFM',
            'store': 'start ms-windows-store:',
            'settings': 'start ms-settings:',
            'taskmanager': 'taskmgr',
            'controlpanel': 'control',
            'virtualbox': 'start virtualbox',
            'vmware': 'start vmware',
            'docker': 'start docker',
            'git': 'start "C:\\Program Files\\Git\\git-bash.exe"',
            'github': 'start githubdesktop',
            'postman': 'start postman',
            'filezilla': 'start filezilla',
            'sublime': 'start sublime_text',
            'atom': 'start atom',
            'brackets': 'start brackets',
            'typora': 'start typora',
            'notion': 'start notion',
            'obsidian': 'start obsidian',
            'evernote': 'start evernote',
            'onenote': 'start onenote',
            'acrobat': 'start acrord32',
            'itunes': 'start itunes',
            'winamp': 'start winamp',
            'foobar': 'start foobar2000',
            'handbrake': 'start handbrake',
            'ccleaner': 'start ccleaner',
            'malwarebytes': 'start mbam',
            'anydesk': 'start anydesk',
            'teamviewer': 'start teamviewer',
            'utorrent': 'start utorrent',
            'qbittorrent': 'start qbittorrent',
            'putty': 'start putty',
            'winscp': 'start winscp',
        }

        # Step 1: Check if it's a URL with domain extension
        if any(domain in target_lower for domain in ['.com', '.org', '.net', '.io', '.ai', '.tv', 'www', 'http']):
            if not target_lower.startswith('http'):
                url = 'https://' + target
            else:
                url = target
            try:
                webbrowser.open(url)
                return f"Opening {url} in your browser"
            except Exception as e:
                return f"Could not open {url}. Error: {str(e)}"

        # Step 2: Check if it's a known website
        for site_name, site_url in websites.items():
            if site_name in target_lower:
                try:
                    webbrowser.open(site_url)
                    return f"Opening {site_name.title()} in your browser"
                except Exception as e:
                    return f"Could not open {site_name}. Error: {str(e)}"

        # Step 3: Check if it's a known application
        for app, names in app_map.items():
            if any(name in target_lower for name in names):
                try:
                    subprocess.Popen(app_commands[app], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return f"Launching {app.title().replace('vscode', 'VS Code').replace('cmd', 'Command Prompt')}"
                except Exception as e:
                    print(f"Error launching {app}: {e}")
                    continue

        # Step 4: Check if it's a file or folder path
        if os.path.exists(target):
            if os.path.isdir(target):
                try:
                    os.startfile(target)
                    return f"Opening directory: {target}"
                except Exception as e:
                    return f"Could not open directory: {str(e)}"
            else:
                safe_extensions = ['.txt', '.pdf', '.jpg', '.jpeg', '.png', '.gif', 
                                   '.mp4', '.mp3', '.wav', '.doc', '.docx', '.xls', 
                                   '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z',
                                   '.py', '.js', '.html', '.css', '.json', '.xml',
                                   '.cpp', '.c', '.java', '.cs', '.md']
                file_ext = Path(target).suffix.lower()
                if file_ext in safe_extensions:
                    try:
                        os.startfile(target)
                        return f"Opening file: {Path(target).name}"
                    except Exception as e:
                        return f"Could not open file: {str(e)}"
                else:
                    return f"Security restriction: Cannot open {file_ext} files"

        # Step 5: Try to launch as generic application
        try:
            subprocess.Popen(target, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            return f"Launched {target.title()} (if installed)"
        except Exception as e:
            print(f"Error: {e}")
            pass

        # Step 6: Handle search commands
        search_triggers = ['search for', 'google', 'bing', 'find on web', 'search web', 'look up']
        if any(trigger in target_lower for trigger in search_triggers):
            search_query = target_lower
            for trigger in search_triggers:
                search_query = search_query.replace(trigger, '').strip()
        
            if search_query:
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                try:
                    webbrowser.open(search_url)
                    return f"Searching web for: {search_query}"
                except Exception as e:
                    return f"Could not search: {str(e)}"
            else:
                try:
                    webbrowser.open("https://www.google.com")
                    return "Opening Google"
                except Exception as e:
                    return f"Could not open Google: {str(e)}"

        # Step 7: Nothing worked - provide helpful message
        return (f"Unable to resolve command: '{target}'\n"
                f"Please specify:\n"
                f"  • Application: 'open notepad'\n"
                f"  • Website: 'open youtube.com'\n"
                f"  • Search: 'search for {target}'")
    
    @staticmethod
    def system_control(command: str) -> str:
        """Control system operations"""
        cmd_lower = command.lower()
        
        if 'shutdown' in cmd_lower or 'shut down' in cmd_lower:
            os.system('shutdown /s /t 30')
            return "Affirmative. System shutdown initiated. 30 second countdown."
        
        elif 'restart' in cmd_lower or 'reboot' in cmd_lower:
            os.system('shutdown /r /t 30')
            return "Affirmative. System restart initiated. 30 second countdown."
        
        elif 'cancel' in cmd_lower and 'shutdown' in cmd_lower:
            os.system('shutdown /a')
            return "Shutdown protocol aborted. All systems remain operational."
        
        elif 'lock' in cmd_lower:
            os.system('rundll32.exe user32.dll,LockWorkStation')
            return "Locking workstation."
        
        elif 'volume up' in cmd_lower:
            pyautogui.press('volumeup', presses=5)
            return "Volume increased."
        
        elif 'volume down' in cmd_lower:
            pyautogui.press('volumedown', presses=5)
            return "Volume decreased."
        
        elif 'mute' in cmd_lower:
            pyautogui.press('volumemute')
            return "Audio muted."
        
        elif 'screenshot' in cmd_lower or 'screen shot' in cmd_lower:
            filename = f'codex_capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            pyautogui.screenshot(filename)
            return f"Screen capture complete. File saved as {filename}"
        
        return "System command not recognized."
    
    @staticmethod
    def get_system_status() -> str:
        """Get detailed system status"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            battery = psutil.sensors_battery()
        
            status = f"System Status Report:\n"
            status += f"  • CPU Load: {cpu}%\n"
            status += f"  • Memory Usage: {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)\n"
            status += f"  • Primary Disk: {disk.percent}% used\n"
        
            if battery:
                status += f"  • Battery: {battery.percent}%"
                if battery.power_plugged:
                    status += " (Charging)"
                # NEW CHECK: Only show time if secsleft is a valid, positive number
                elif (battery.secsleft and 
                      battery.secsleft > 0 and 
                      battery.secsleft not in (psutil.POWER_TIME_UNKNOWN, psutil.POWER_TIME_UNLIMITED)):
                    
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    status += f" (Approx. {hours}h {minutes}m remaining)"
                
                else:
                    # This is the correct fallback
                    status += " (On Battery)"
        
            else:
                status += "\n  • Battery: N/A (No battery detected)"
        
            return status
        except Exception as e:
            return f"Unable to retrieve system status: {str(e)}"

# ============================================================================
# NEWS & WEATHER (NO APIs)
# ============================================================================

class NewsWeather:
    """Get news and weather without APIs (Unchanged from NEXUS)"""
    
    @staticmethod
    def get_news() -> str:
        """Get latest worldwide news from multiple sources"""
    
        news_sources = [
            {
                'name': 'BBC World News',
                'url': 'http://feeds.bbci.co.uk/news/world/rss.xml',
                'icon': '🌍'
            },
            {
                'name': 'CNN Top Stories',
                'url': 'http://rss.cnn.com/rss/edition.rss',
                'icon': '📡'
            },
            {
                'name': 'Reuters World News',
                'url': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
                'icon': '🌐'
            },
            {
                'name': 'Al Jazeera',
                'url': 'https://www.aljazeera.com/xml/rss/all.xml',
                'icon': '🗞️'
            }
        ]
    
        all_headlines = []
        sources_fetched = 0
    
        for source in news_sources:
            try:
                response = requests.get(source['url'], timeout=8)
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')[:5]
            
                for item in items:
                    title = item.title.text
                    title = title.replace('\n', ' ').replace('\r', '').strip()
                    all_headlines.append({
                        'title': title,
                        'source': source['name'],
                        'icon': source['icon']
                    })            
                sources_fetched += 1

            except Exception as e:
                print(f"⚠️ Could not fetch from {source['name']}: {e}")
                continue
    
        if not all_headlines:
            return "Unable to fetch news from any source. Please check your internet connection."
    
        # Format for display
        news = f"\n📰 Global News Briefing ({sources_fetched} sources)\n"
        news += f"{'='*60}\n\n"
    
        for i, item in enumerate(all_headlines[:12], 1):
            news += f"{item['icon']} {item['title']}\n"
            news += f"   └─ Source: {item['source']}\n\n"
    
        news += f"{'='*60}\n"
        news += f"Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    
        return news
    
    @staticmethod
    def prepare_news_for_voice(display_text: str) -> str:
        """Convert news display to professional voice delivery format - reads ALL headlines"""
        lines = display_text.split('\n')
        headlines = []
    
        for line in lines:
            line = line.strip()
            # Extract just the headlines (skip headers, sources, metadata)
            if not line or line.startswith('=') or line.startswith('─'):
                continue
            if 'Updated:' in line or 'Source:' in line or 'Global News' in line:
                continue
            if line.startswith('└'):
                continue
        
            # Remove emojis and numbers
            line = re.sub(r'^[\d]+\.\s*', '', line)
            line = re.sub(r'[🌍📡🌍🗞️📰✅❌⚠️🔎🎤📊😴📚🎓💡💤📖🌤️☀️⛅☁️🌧️⛈️❄️🌫️🌬️🌡️🌦️💧🌊🔍]', '', line)
            line = line.strip()
        
            if len(line) > 15:
                headlines.append(line)
    
        # Create natural newsreader format with ALL headlines
        voice_text = "Here is your global news briefing. "
        
        # Read ALL headlines without numbering
        for i, headline in enumerate(headlines, 1):
            voice_text += f"{headline}. "
            
            # Add brief pause after every 3 headlines for better pacing
            if i % 3 == 0 and i < len(headlines):
                voice_text += "Continuing. "
    
        voice_text += "That concludes the news briefing."
        return voice_text

    @staticmethod
    def get_weather_with_true_location(city: str = None) -> str:
        """
        Get weather using PRECISE HARDCODED location.
        This is the most reliable method and avoids all detection errors.
        """
        
        # --- PRECISE LOCATION LOGIC ---
        HOME_LAT = 17.131030
        HOME_LON = 81.645510
        HOME_NAME = "Gajjaram"
        
        # If user types "weather in London", 'city' will be "London"
        # If user just types "weather", 'city' will be None
        
        if city:
            # User specified a city, so we use that
            location = city
            print(f"✓ Querying weather for specified city: {location}")
            display_location_override = None
        else:
            # User just typed "weather", use the PRECISE home location
            location = f"{HOME_LAT},{HOME_LON}"
            print(f"✓ Using PRECISE Home Location: {HOME_NAME}")
            # We set this to override the wttr.in name
            display_location_override = f"{HOME_NAME}, Andhra Pradesh, India ({HOME_LAT}°N, {HOME_LON}°E)"
        
        try:
            weather_response = requests.get(
                f'https://wttr.in/{location}?format=j1', 
                timeout=10,
                headers={'User-Agent': 'CODEX-AI/1.0'}
            )
            data = weather_response.json()
        
            current = data['current_condition'][0]
            temp_c = current.get('temp_C', 'N/A')
            temp_f = current.get('temp_F', 'N/A')
            feels_like_c = current.get('FeelsLikeC', 'N/A')
            feels_like_f = current.get('FeelsLikeF', 'N/A')
            weather_desc = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
            humidity = current.get('humidity', 'N/A')
            wind_speed_kmh = current.get('windspeedKmph', 'N/A')
            wind_speed_mph = current.get('windspeedMiles', 'N/A')
            pressure = current.get('pressure', 'N/A')
            visibility = current.get('visibility', 'N/A')
            uv_index = current.get('uvIndex', 'N/A')
        
            # This is the location wttr.in *thinks* it is
            nearest_area = data.get('nearest_area', [{}])[0]
            area_name = nearest_area.get('areaName', [{}])[0].get('value', location)
            region_name = nearest_area.get('region', [{}])[0].get('value', '')
            country_name = nearest_area.get('country', [{}])[0].get('value', '')
        
            if region_name and country_name:
                display_location = f"{area_name}, {region_name}, {country_name}"
            elif country_name:
                display_location = f"{area_name}, {country_name}"
            else:
                display_location = area_name
            
            # --- THIS IS THE FIX ---
            # If we used our home coordinates, OVERRIDE the display name
            # with our precise, correct name.
            if display_location_override:
                display_location = display_location_override
            # --- END OF FIX ---
        
            condition_lower = weather_desc.lower()
            if 'sunny' in condition_lower or 'clear' in condition_lower:
                icon = '☀️'
            elif 'partly cloudy' in condition_lower:
                icon = '⛅'
            elif 'cloud' in condition_lower:
                icon = '☁️'
            elif 'rain' in condition_lower or 'drizzle' in condition_lower:
                icon = '🌧️'
            elif 'thunder' in condition_lower or 'storm' in condition_lower:
                icon = '⛈️'
            elif 'snow' in condition_lower:
                icon = '❄️'
            elif 'mist' in condition_lower or 'fog' in condition_lower:
                icon = '🌫️'
            elif 'wind' in condition_lower:
                icon = '🌬️'
            else:
                icon = '🌤️'
        
            weather = f"\n{icon} Weather Report\n"
            weather += f"{'='*60}\n"
            weather += f"📍 Location: {display_location}\n"
            weather += f"{'─'*60}\n"
            weather += f"🌡️  Temperature: {temp_c}°C ({temp_f}°F)\n"
            weather += f"🤔 Feels Like: {feels_like_c}°C ({feels_like_f}°F)\n"
            weather += f"🌤️  Conditions: {weather_desc}\n"
            weather += f"💧 Humidity: {humidity}%\n"
            weather += f"🌬️  Wind Speed: {wind_speed_kmh} km/h ({wind_speed_mph} mph)\n"
            weather += f"🔽 Pressure: {pressure} mb\n"
            weather += f"👁️  Visibility: {visibility} km\n"
            weather += f"☀️  UV Index: {uv_index}\n"
            weather += f"{'─'*60}\n"
            weather += f"🕐 Updated: {datetime.now().strftime('%I:%M %p, %B %d, %Y')}\n"
            weather += f"{'='*60}"
            
            return weather
        
        except Exception as e:
            return f"Unable to fetch weather: {str(e)}"

    @staticmethod
    def get_weather(city: str = None) -> str:
        """Alias for new method - for backward compatibility"""
        return NewsWeather.get_weather_with_true_location(city)
    
    @staticmethod
    def prepare_weather_for_voice(weather_text: str) -> str:
        """Convert weather display to professional voice delivery format
        
        This creates a newsreader-style weather report with proper pacing
        """
        # Extract data using regex patterns
        location_match = re.search(r'📍 Location: (.+)', weather_text)
        temp_match = re.search(r'🌡️.*?Temperature: ([\d-]+)°C.*?\(([\d-]+)°F\)', weather_text)
        feels_match = re.search(r'🤔.*?Feels Like: ([\d-]+)°C', weather_text)
        condition_match = re.search(r'🌤️.*?Conditions: (.+)', weather_text)
        humidity_match = re.search(r'💧 Humidity: ([\d]+)%', weather_text)
        wind_match = re.search(r'🌬️  Wind Speed: ([\d]+) km/h', weather_text)
        uv_match = re.search(r'☀️.*?UV Index: ([\d\.]+)', weather_text)
        
        location = location_match.group(1) if location_match else "your location"
        temp_c = temp_match.group(1) if temp_match else "unknown"
        condition = condition_match.group(1) if condition_match else "mixed conditions"
        humidity = humidity_match.group(1) if humidity_match else "unknown"
        wind = wind_match.group(1) if wind_match else "unknown"
        uv_index = uv_match.group(1) if uv_match else "unknown"
        
        # Build professional newsreader-style report
        voice_text = f"Here is the weather forecast for {location}. "
        voice_text += f"The current conditions are: {condition}. "
        voice_text += f"The temperature is {temp_c} degrees celsius. "
        voice_text += f"Humidity is at {humidity} percent, "
        voice_text += f"with wind speeds of {wind} kilometers per hour. "
        
        # Add UV warning if high
        try:
            if float(uv_index) > 6:
                voice_text += "The UV index is high; sun protection is recommended. "
        except:
            pass
        
        voice_text += "This concludes the weather report."
        
        return voice_text

# ============================================================================
# SMART SEARCH
# ============================================================================

try:
    from ddgs import DDGS
    DUCKDUCKGO_SEARCH_AVAILABLE = True
except Exception as e:
    print("="*80)
    print(f"⚠️ CRITICAL ERROR: 'ddgs' library failed to import.")
    print(f"   Error: {e}")
    print("   Please ensure 'ddgs' is installed: pip install ddgs")
    print("="*80)
    DUCKDUCKGO_SEARCH_AVAILABLE = False

class SmartSearch:
    """Intelligent web search with comprehensive synthesis.
       (Rebuilt to be reliable and provide clean, non-truncated answers)
    """
    
    def __init__(self):
        if DUCKDUCKGO_SEARCH_AVAILABLE:
            try:
                self.ddgs = DDGS()
            except Exception as e:
                print(f"⚠️ Failed to initialize DDGS: {e}")
                self.ddgs = None
        else:
            self.ddgs = None
    
    def search(self, query: str) -> str:
        """Search and provide comprehensive intelligent answers (V5 - Text-Only)"""
        if not self.ddgs:
            return "Search interface is currently offline."

        query = query.strip()
        query_lower = query.lower()
        words = query.split()
        
        # --- NEW: Smart Query Enhancement (V3 - FINAL) ---
        search_query = query
        if len(query.split()) <= 2:
            # Forces the engine to find definitions and theory
            search_query = f"comprehensive technical overview of {query}"

        # 1. Special case for "define"
        if query_lower.startswith("define "):
            topic = query[len("define "):].strip()
            search_query = f"what is {topic}"
        
        # 2. General case for simple topics (like "NASA")
        else:
            is_question = any(q_word in query_lower for q_word in ['what', 'who', 'when', 'where', 'why', 'how', 'explain', 'search for'])
            if len(words) <= 3 and not is_question:
                search_query = f"what is {query}"
        # --- End New ---

        print(f"🔍 Searching globally: {search_query}")
        
        try:
            results = list(self.ddgs.text(search_query, region='wt-wt', max_results=10))
            
            if not results:
                return f"My apologies, I was unable to find relevant information for '{query}'."
            
            return self._create_intelligent_answer(query, results)
                
        except requests.exceptions.ConnectionError:
            return "Cannot connect to search service. Please check your internet connection."
        except Exception as e:
            print(f"❌ Search error: {e}")
            return f"A search error occurred: {str(e)}. Please check your internet connection."

    
    def _try_spell_correction(self, query: str) -> str:
        """Try to correct common misspellings"""
        corrections = {
            'stagnography': 'steganography',
            'cryptograpy': 'cryptography',
            'qunatum': 'quantum',
            'machien': 'machine'
        }
        query_lower = query.lower()
        for wrong, correct in corrections.items():
            if wrong in query_lower:
                return query_lower.replace(wrong, correct)
        return query
    
    def _create_intelligent_answer(self, query: str, results: List[Dict]) -> str:
        """Create comprehensive, well-structured answer from snippets"""

        topic = query # The 'topic' is just the user's original query

        all_content = []
        seen_content = set()

        for result in results:
            body = result.get('body', '').strip()
            # Clean the text (this is the key fix)
            clean_snippet = self._clean_text(body)

            # Quality checks
            if clean_snippet and len(clean_snippet) > 60: # Increased minimum length
                # Filter out low-quality "ad" or junk results
                junk_words = ["udemy", "coursera", "phd student", "mit news", "i am currently reading", "wizard", "jesse van doren"]
                if any(ad in clean_snippet.lower() for ad in junk_words):
                    continue
                
                normalized = clean_snippet[:100].lower()
                if normalized not in seen_content:
                    all_content.append(clean_snippet)
                    seen_content.add(normalized)

        if not all_content:
            return f"I found results for '{query}' but couldn't extract a clear, high-quality summary."

        # --- NEW: Universal Snippet Logic ---
        # We don't try to find a "best" definition.
        # We just present the top 3-4 high-quality snippets.

        if not all_content:
            return f"I found results for '{query}', but could not extract a clear, high-quality summary."

        # We will use all_content directly.
        # --- End New Logic ---

        # Universal formatter
        return self._format_answer(topic, all_content)
        
    def _fix_wikipedia_url(self, topic: str) -> str:
        """Cleans a query topic to be wiki-friendly (V2 - Subject Extractor)."""
        
        topic_lower = topic.lower().strip()
        
        # 1. Define question words/phrases to remove from the START
        stop_phrases = [
            'what is', 'what are', 'what was', 'what were',
            'who is', 'who was', 'who are', 'who were',
            'explain', 'tell me about', 'define', 'describe'
        ]
        
        # Clean the query to find the topic
        for phrase in stop_phrases:
            if topic_lower.startswith(phrase):
                topic_lower = topic_lower[len(phrase):].strip()
                break
        
        topic_lower = topic_lower.replace('?', '').strip()

        # 2. Define "noise" prepositions to find the main subject
        # e.g., "ceo of microsoft" -> "microsoft"
        # e.g., "capital of france" -> "france"
        prepositions = ['of', 'for', 'in', 'on', 'at']
        
        words = topic_lower.split()
        
        # Find the first preposition
        first_prep_index = -1
        for i, word in enumerate(words):
            if word in prepositions:
                first_prep_index = i
                break
        
        # If we found a preposition AND there's text after it,
        # assume the text *after* is the true subject.
        if first_prep_index != -1 and first_prep_index + 1 < len(words):
             # e.g., "ceo of microsoft" -> "microsoft"
            subject = " ".join(words[first_prep_index + 1:])
            
            # Special case: "mitre att&ck framework"
            # If "framework" is in the subject, use the whole thing
            if "framework" in subject.lower():
                 subject = topic_lower
            
            final_topic = subject
        
        else:
            # No prepositions found, just use the cleaned query
            # e.g., "nasa" -> "nasa"
            final_topic = topic_lower
        
        # --- NEW: Final 'the' cleanup ---
        # Fixes "the mitre att&ck framework"
        if final_topic.startswith("the "):
            final_topic = final_topic[4:]
        # --- End New ---
            
        # Final format for wiki
        return final_topic.replace(" ", "_")
       
    def _clean_text(self, text: str) -> str:
        """
        Clean and prepare text. Aggressively removes truncation.
        (UPGRADED to handle all trailing junk)
        """
        if not text:
            return ""

        # Remove dates/timestamps
        text = re.sub(r'[A-Za-z]+\s+\d{1,2},\s+\d{4}\s*[-·•]\s*', '', text)
        text = re.sub(r'\d+\s+(days?|hours?|weeks?)\s+ago\s*', '', text)
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove leading bullets/dashes
        text = re.sub(r'^[•\-\*\›»◸\s]+', '', text)

        # --- THIS IS THE KEY FIX ---
        # 1. Find the *first* ellipsis (...) or (…).
        ellipsis_index = text.find('...')
        ellipsis_index_unicode = text.find('…')

        # Find the earliest truncation point
        trunc_point = -1
        if ellipsis_index != -1:
            trunc_point = ellipsis_index
        if ellipsis_index_unicode != -1 and (trunc_point == -1 or ellipsis_index_unicode < trunc_point):
            trunc_point = ellipsis_index_unicode

        # 2. If we found one, cut the string off there.
        if trunc_point != -1:
            text = text[:trunc_point]

        # 3. Aggressively remove any junk left at the end (like '...Q.')
        text = re.sub(r'[\.…, ]+$', '', text).strip()
        text = re.sub(r"['’]\.\s*$", ".", text) # Fixes "...intelligent''. Q."

        # 4. Now, find the last period and keep everything before it.
        last_period = text.rfind('.')
        if last_period != -1:
            # Get text up to and including the last period
            text = text[:last_period+1]
        else:
            # No period found, the snippet is likely garbage
            if len(text) < 60: # If it's short and has no period, discard it
                return ""

        return text.strip()

    def _format_answer(self, topic: str, snippets: List[str]) -> str:
        """Formats a universal answer for any query."""

        # Clean the topic for the title
        title_topic = topic.title()
        stop_phrases = [
            'What Is', 'What Are', 'Who Is', 'Who Are',
            'Explain', 'Tell Me About', 'Define', 'Describe'
        ]
        for phrase in stop_phrases:
            if title_topic.startswith(phrase):
                title_topic = title_topic[len(phrase):].strip()

        answer = f"📖 **Information on: {title_topic}**\n\n"
        answer += f"**Key Information:**\n"

        # Show the top 3-4 snippets
        for snippet in snippets[:4]:
            answer += f"• {snippet}\n"

        # --- Fix the Learn More links ---
        # We clean the topic *here* for the links
        link_topic = self._fix_wikipedia_url(topic)

        answer += "\n**Learn More:**\n"
        answer += f"• https://en.wikipedia.org/wiki/{link_topic}\n"
        answer += f"• https://www.google.com/search?q={topic.replace(' ', '+')}\n"
        answer += f"• https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"
        return answer.strip()

# ============================================================================
# NEW ADVANCED MEDIA CONTROLLER (FINAL VERSION)
# ============================================================================

class MediaController:
    """
    Handles playing music and videos using smart, platform-specific search.
    """

    def __init__(self, search_instance):
        """
        Takes an instance of the main DDGS_Search object.
        """
        self.ddgs = search_instance
        if self.ddgs:
            # print(f"{MatrixColors.BRIGHT_GREEN}[✓] Advanced Media Controller initialized (shared search core).{MatrixColors.RESET}")
            pass
        else:
            print(f"{MatrixColors.RED}[✗] Advanced Media Controller OFFLINE (shared core offline).{MatrixColors.RESET}")


    def play_on_youtube(self, query: str) -> str:
        """
        Smart-searches YouTube using ddgs.videos() and plays the *first* valid result.
        (REBUILT to be simpler and more accurate)
        """
        if not self.ddgs:
            return "YouTube search module is offline (shared core offline)."

        try:
            # Force the search to only look at youtube.com
            youtube_query = f"{query} site:youtube.com"
            print(f"🌍 Smart-searching YouTube-ONLY for: '{youtube_query}'")

            # Use the correct ddgs.videos() function
            results = list(self.ddgs.videos(youtube_query, max_results=5))

            if not results:
                return f"No YouTube video results found for '{query}'."

            # --- NEW: Simple and Reliable Logic ---
            # Find the *first* result that is actually from YouTube.
            best_match = None
            for video in results:
                url = video.get('content', '')
                if "youtube.com" in url or "youtu.be" in url:
                    best_match = video
                    break # Found the first valid link, stop.
            
            if not best_match:
                return "Search found video results, but none were from YouTube."
            # --- End of new logic ---

            video_title = best_match['title']
            video_url = best_match['content']

            print(f"✓ Best match found: '{video_title}'")
            print(f"Opening URL: {video_url}")

            webbrowser.open(video_url)
            
            return f"Affirmative. Playing '{video_title}'."

        except Exception as e:
            print(f"❌ YouTube search error: {e}")
            return f"A YouTube search error occurred: {e}"


    def play_from_web(self, query: str) -> str:
        """
        Smart-searches the *web* for a preferred media site (Spotify, SoundCloud).
        Returns None if no good site is found.
        """
        if not self.ddgs:
            return "Media search module is offline (shared core offline)."

        try:
            web_query = query
            
            print(f"🌍 Searching all web for: '{web_query}'")
            results = list(self.ddgs.text(web_query, max_results=10))
            if not results:
                return "No web results found."

            best_sites = [
                "spotify.com",
                "soundcloud.com",
                "bandcamp.com"
            ]
            
            best_match = None
            for site in best_sites:
                for result in results:
                    url = result.get('href', '')
                    if site in url:
                        best_match = result
                        break 
                if best_match:
                    break 
            
            if not best_match:
                print(f"ℹ️  No preferred media site (Spotify, etc.) found.")
                return None # --- THIS IS THE FIX: Return None instead of a junk link

            title = best_match.get('title', 'Unknown Title')
            url = best_match.get('href', '') 

            if not url:
                print(f"❌ Error: Best match found, but it has no URL.")
                return "A web search error occurred: Found a result but it has no URL."

            print(f"✓ Best match found: '{title}'")
            print(f"Opening URL: {url}")
            webbrowser.open(url)
            return f"Affirmative. Playing '{title}'."

        except Exception as e:
            print(f"❌ Web search error: {e}")
            return f"A web search error occurred: {e}"

    def search_spotify(self, query: str) -> str:
        """
        Uses pywhatkit to open a browser search for a Spotify track.
        """
        try:
            search_query = f"spotify {query}"
            print(f"🌍 Searching Google for: '{search_query}'")
            pywhatkit.search(search_query)
            return f"Opening Spotify search results for '{query}'. Please click the link to play."
        except Exception as e:
            return f"Error searching Spotify: {str(e)}"
        
# ============================================================================
# VOICE SYSTEM
# ============================================================================

class VoiceSystem:
    def __init__(self):
        self.output_enabled = False
        self.input_enabled = VOICE_INPUT_AVAILABLE
        self.speaker = None
        self.recognizer = None
        self.is_speaking = False
        self.stop_speaking = False
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._init_output()
        self._init_input()
    
    def _init_output(self):
        if platform.system() == 'Windows':
            try:
                import win32com.client
                self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                self.speaker.Rate = 1
                self.speaker.Volume = 100
                self.output_enabled = True
            except Exception as e:
                print(f"⚠️ Voice output unavailable: {e}")
                print("   Voice responses will be displayed as text only")
    
    def _init_input(self):
        if self.input_enabled:
            try:
                self.recognizer = sr.Recognizer()

                # --- NEW TUNED SETTINGS ---
                # We are turning OFF the "auto-sensitivity"
                self.recognizer.dynamic_energy_threshold = False
                # We are setting a fixed sensitivity. 
                self.recognizer.energy_threshold = 350
                # Give you 2 seconds of silence before it stops listening
                self.recognizer.pause_threshold = 2.0  
                # --- END NEW SETTINGS ---

                self.recognizer.phrase_threshold = 0.3
            except:
                pass
    
    def listen(self) -> str:
        """
        NEW SILENT VERSION
        Listens for a command without printing any status messages.
        This is for the 'active' mode.
        """
        if not self.input_enabled or not self.recognizer:
            return ""
        
        try:
            with sr.Microphone(device_index=None) as source:
                # Calibrate quickly and silently
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
                # Listen silently
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
                # Process silently
                cmd = self.recognizer.recognize_google(audio, language='en-US')
                
                return cmd.strip()
            
        except sr.UnknownValueError:
            return "" # Silently fail
        except sr.WaitTimeoutError:
            return "" # Silently fail
        except sr.RequestError:
            return "" # Silently fail
        except Exception as e:
            return "" # Silently fail
    
    def listen_silently(self) -> str:
        """
        Listens passively in the background without printing ANY status messages.
        This is for the wake-word listener.
        """
        if not self.input_enabled or not self.recognizer:
            return ""
        try:
            with sr.Microphone(device_index=None) as source:
                # We still need to calibrate, but we do it silently
                # self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with a long timeout (e.g., 10 seconds)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                
                # Convert speech to text
                cmd = self.recognizer.recognize_google(audio, language='en-US')
                if cmd: print(f"DEBUG: I HEARD: {cmd}")
                return cmd.strip()
            
        except sr.UnknownValueError:
            return "" # Couldn't understand, return empty (no print)
        except sr.WaitTimeoutError:
            return "" # Timed out, return empty (no print)
        except sr.RequestError:
            return "" # API error, return empty (no print)
        except Exception:
            return "" # Mic error, return empty (no print)
        
    def interrupt(self):
        """Stop speaking immediately"""
        self.stop_speaking = True
        if self.speaker and self.is_speaking:
            try:
                # Purge the speech queue
                self.speaker.Speak("", 2)  # 2 = SVSFPurgeBeforeSpeak
            except:
                pass
    
    def stop_current_speech(self):
        """Immediately stop speaking"""
        self.stop_speaking = True
        self.is_speaking = False
        if self.speaker:
            try:
                # Force stop by speaking empty string with purge flag
                self.speaker.Speak("", 3)  # 3 = SVSFPurgeBeforeSpeak + SVSFIsNotXML
            except:
                pass

    def speak(self, text: str, is_news_weather=False):
        if not self.output_enabled or not text:
            return
        
        self.stop_speaking = False
        self.is_speaking = True
        
        try:
            # Clean text for natural speech
            clean = text
            
            # Remove URLs
            clean = re.sub(r'http[s]?://\S+', '', clean)
            
            # Remove emojis and ALL special characters
            clean = re.sub(r'[☀️⛅☁️🌧️⛈️❄️🌫️💨🌤️🌡️💧📰🎤🔍✅❌⚠️🔎💬📊😴📚💡👤📖🌐📡🌍🗞️📍🤔🔽👁️🕐]', '', clean)

            # Remove box drawing characters and special formatting
            clean = re.sub(r'[═║╔╗╚╝╠╣╬─│┌┐└┘├┤┬┴┼╭╮╰╯▸●◀▶]', '', clean)

            # Remove "Source:" lines and news metadata
            clean = re.sub(r'Source:.*?\n', '', clean)
            clean = re.sub(r'└─.*?\n', '', clean)
            clean = re.sub(r'Updated:.*', '', clean)

            # Remove standalone numbers at start of lines (news numbering)
            clean = re.sub(r'^\s*\d+\.\s*', '', clean, flags=re.MULTILINE)

            # Remove special characters but keep punctuation
            clean = re.sub(r'[^\w\s.,!?:\n°%/-]', '', clean)
            
            # Remove equals separator lines
            clean = re.sub(r'={2,}', '', clean)
            
            # Convert symbols to words
            clean = clean.replace('°C', ' degrees celsius')
            clean = clean.replace('°F', ' degrees fahrenheit')
            clean = clean.replace('%', ' percent')
            clean = clean.replace('km/h', ' kilometers per hour')
            clean = clean.replace('mph', ' miles per hour')
            
            # Clean up extra spaces and newlines
            clean = ' '.join(clean.split())
            clean = clean.strip()
            
            # Don't truncate - speak full content
            if len(clean) >= 3:
                def speak_thread():
                    try:
                        import pythoncom
                        pythoncom.CoInitialize()
                        
                        # Speak in chunks so we can check for interrupts
                        sentences = re.split(r'[.!?]+', clean)
                        for sentence in sentences:
                            if self.stop_speaking:
                                break
                            if sentence.strip():
                                self.speaker.Speak(sentence.strip(), 0)
                        
                        pythoncom.CoUninitialize()
                    except:
                        pass
                    finally:
                        self.is_speaking = False
                
                thread = threading.Thread(target=speak_thread, daemon=True)
                thread.start()
                
        except:
            pass
        finally:
            self.is_speaking = False

    def speak_and_wait(self, text: str):
        """Speak text and wait until completely finished"""
        if not self.output_enabled or not text:
            return

        # Clean text
        clean = text
        clean = re.sub(r'http[s]?://\S+', '', clean)
        clean = re.sub(r'[☀️⛅☁️🌧️⛈️❄️🌫️💨🌤️🌡️💧📰🎤📚✅❌⚠️🔍💬📊😴📚🔍💡👤📖]', '', clean)
        clean = re.sub(r'[^\w\s.,!?:\n°%/-]', '', clean)
        clean = re.sub(r'={2,}', '', clean)
        clean = clean.replace('°C', ' degrees celsius').replace('°F', ' degrees fahrenheit')
        clean = clean.replace('%', ' percent').replace('km/h', ' kilometers per hour')
        clean = ' '.join(clean.split()).strip()
    
        if len(clean) >= 3:
            # Start speaking
            self.speak(clean)
        
            # Calculate time needed (average speaking rate: 150 words/min = 2.5 words/sec)
            word_count = len(clean.split())
            speech_time = (word_count / 2.5) + 1  # Add 1 second buffer
        
            # Wait for speech to finish
            time.sleep(speech_time)

    async def listen_async(self) -> str:
        """Non-blocking voice listening - returns in <15 seconds"""
        loop = asyncio.get_event_loop()
        try:
            cmd = await asyncio.wait_for(
                loop.run_in_executor(self.executor, self.listen),
                timeout=15.0
            )
            return cmd if cmd else ""
        except asyncio.TimeoutError:
            return ""
        except Exception as e:
            print(f"❌ Voice listen error: {e}")
            return ""
    
    async def speak_async(self, text: str):
        """Non-blocking voice output"""
        loop = asyncio.get_event_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(self.executor, self.speak, text),
                timeout=30.0
            )
        except Exception as e:
            print(f"❌ Voice speak error: {e}")

# ============================================================================
# MAIN CODEX
# ============================================================================

class CODEX:
    def __init__(self, is_worker=False):  # <--- ADD is_worker=False

        # Workers don't need to print or start other processes
        if not is_worker:
            os.system('cls' if os.name == 'nt' else 'clear')
            pass

        # Simple startup message (no banner)
        # print(f"\n{MatrixColors.BRIGHT_GREEN}⚙️  Initializing C O D E X  AI Assistant...{MatrixColors.RESET}\n")

        self.brain = AIBrain()
        self.pc = PCController()
        self.news_weather = NewsWeather()
        self.search = SmartSearch()
        self.voice = VoiceSystem()
        self.terminal = MatrixTerminal()
        self.media = MediaController(search_instance=self.search.ddgs)

        # NEW: Performance monitoring and caching ⬇️
        self.command_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_commands = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_start_time = None
        
        # NEW: Logging setup
        if ENABLE_LOGGING:
            self._setup_logging()
        
        # NEW: Error tracking
        self.error_history = []
        self.start_time = datetime.now()
        # ⬆️ END NEW

        # Global exit flag
        self.program_should_exit = False

        # --- NEW: MULTIPROCESSING SETUP ---
        if not is_worker:
            self.command_queue = multiprocessing.Queue()
            self.response_queue = multiprocessing.Queue()
            self.worker_process = multiprocessing.Process(
                target=process_worker, 
                args=(self.command_queue, self.response_queue),
                daemon=True
            )
            self.worker_process.start()
        # --- END NEW ---

        # --- NEW MEMORY/PREFERENCE SYSTEM ---
        self.config_file = "codex_config.json"
        self.preferences = self._load_preferences()
        self.user_name = self.preferences.get("user_name", "Sir") # Load name from config

    # NEW METHODS ⬇️
    def _setup_logging(self):
        """Setup file logging"""
        from pathlib import Path
        
        log_dir = Path("codex_logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"codex_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        self.logger = logging.getLogger('CODEX')
        self.logger.setLevel(logging.DEBUG)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def _log_command(self, command: str, success: bool, response: str, response_time: float):
        """Log command execution"""
        if ENABLE_LOGGING:
            try:
                # FIX: Strip emojis from response before logging ⬇️
                clean_response = response[:80]
                clean_response = ''.join(c for c in clean_response if ord(c) < 128 or c in '\n ')
                # ⬆️ FIXED
                
                self.logger.info(
                    f"CMD: '{command}' | SUCCESS: {success} | "
                    f"TIME: {response_time:.3f}s | RESPONSE: {clean_response}"
                )
            except Exception as e:
                # Fallback if logging fails
                pass
    
    def _get_cache_key(self, command: str) -> str:
        """Generate cache key"""
        return hashlib.md5(command.encode()).hexdigest()
    
    def _is_cacheable(self, command: str) -> bool:
        """Check if command should be cached"""
        # FIX: Added 'weather' to the list
        no_cache = ['time', 'date', 'status', 'battery', 'weather in', 'weather', 'news']
        return not any(word in command.lower() for word in no_cache)
    
    def _get_cached_response(self, command: str):
        """Get cached response"""
        key = self._get_cache_key(command)
        
        if key in self.command_cache:
            response, timestamp = self.command_cache[key]
            if time.time() - timestamp < COMMAND_CACHE_TTL:
                self.cache_hits += 1
                return response
            else:
                del self.command_cache[key]
        
        self.cache_misses += 1
        return None
    
    def _cache_response(self, command: str, response: str):
        """Cache a response"""
        if self._is_cacheable(command):
            key = self._get_cache_key(command)
            self.command_cache[key] = (response, time.time())
    
    def _show_dashboard(self):
        """Show performance dashboard"""
        total = self.total_commands
        success_rate = (self.successful_commands / total * 100) if total > 0 else 0
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]
        
        print(f"\n{'='*70}")
        print("⚡ CODEX AI - PERFORMANCE DASHBOARD")
        print(f"{'='*70}")
        print(f"Total Commands:        {total}")
        print(f"Success Rate:          {success_rate:.1f}%")
        print(f"Cache Hits:            {self.cache_hits}")
        print(f"Cache Misses:          {self.cache_misses}")
        print(f"Errors Today:          {len(self.error_history)}")
        print(f"Uptime:                {uptime_str}")
        status = "🟢 HEALTHY" if success_rate > 95 else "🟡 DEGRADED" if success_rate > 80 else "🔴 CRITICAL"
        print(f"Status:                {status}")
        print(f"{'='*70}\n")
    
    def _optimize_memory(self):
        """Optimize memory usage"""
        gc.collect()
        mem = psutil.virtual_memory()
        print(f"💾 Memory: {mem.used / (1024**3):.1f}GB / {mem.total / (1024**3):.1f}GB")
    # ⬆️ END NEW

    def _load_preferences(self) -> dict:
        """Loads user preferences from the config file."""
        if not os.path.exists(self.config_file):
            print(f"{MatrixColors.YELLOW}⚠️  Warning: '{self.config_file}' not found. Creating a default file.{MatrixColors.RESET}")
            default_config = {
                "user_name": "Sir",
                "default_media_platform": "web"
            }
            try:
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
            except Exception as e:
                print(f"{MatrixColors.RED}✗ ERROR: Could not create config file: {e}{MatrixColors.RESET}")
                return {"user_name": "Sir", "default_media_platform": "web"}

        try:
            with open(self.config_file, 'r') as f:
                preferences = json.load(f)
                # print(f"{MatrixColors.BRIGHT_GREEN}✓ Preferences loaded from '{self.config_file}'.{MatrixColors.RESET}")
                return preferences
        except Exception as e:
            print(f"{MatrixColors.RED}✗ ERROR: Could not read config file: {e}{MatrixColors.RESET}")
            return {"user_name": "Sir", "default_media_platform": "web"}

    def _save_preferences(self):
        """Saves current preferences to the config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.preferences, f, indent=4)
            print(f"{MatrixColors.BRIGHT_GREEN}✓ Preferences saved.{MatrixColors.RESET}")
        except Exception as e:
            print(f"{MatrixColors.RED}✗ ERROR: Could not save preferences: {e}{MatrixColors.RESET}")
    
    def emergency_shutdown(self):
        """Force immediate shutdown of all components"""
        print(f"\n{MatrixColors.RED}🛑 Emergency shutdown initiated...{MatrixColors.RESET}")
    
        # Stop voice
        if self.voice:
            self.voice.stop_speaking = True
    
        print(f"{MatrixColors.YELLOW}CODEX terminated.{MatrixColors.RESET}\n")
        sys.exit(0)

    def get_time_greeting(self) -> str:
        """Get time-based greeting"""
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def startup_greeting(self):
        """Voice greeting at startup"""
        greeting = self.get_time_greeting()
        message = f"{greeting}, {self.user_name}. I am CODEX. All systems are online and at your disposal."
        print(f"\n{MatrixColors.BRIGHT_GREEN}{message}{MatrixColors.RESET}\n")
    
        if self.voice.output_enabled and self.voice.speaker:
            try:
                self.voice.speaker.Speak(message, 0)
            except Exception as e:
                print(f"⚠️ Voice greeting failed: {e}")

    def shutdown_greeting(self):
        """Voice greeting at shutdown"""
        message = f"CODEX shutting down. It has been a pleasure, {self.user_name}. Goodbye."
        print(f"\n{MatrixColors.BRIGHT_GREEN}{message}{MatrixColors.RESET}\n")
    
        if self.voice.output_enabled and self.voice.speaker:
            try:
                self.voice.speaker.Speak(message, 0)
            except Exception as e:
                print(f"⚠️ Voice shutdown failed: {e}")

    # NEW METHODS ⬇️
    def validate_command(self, command: str) -> tuple:
        """Validate if command is safe to execute"""
        
        DANGEROUS = {
            'shutdown': 'This will shut down your computer. Continue?',
            'restart': 'This will restart your computer. Continue?',
        }
        
        BLOCKED = {
            'format': 'Formatting is not allowed',
            'registry': 'Registry operations are not allowed',
        }
        
        cmd_lower = command.lower()
        
        # Check blocked
        for blocked, reason in BLOCKED.items():
            if blocked in cmd_lower:
                return False, False, f"❌ {reason}"
        
        # Check dangerous
        for dangerous, msg in DANGEROUS.items():
            if dangerous in cmd_lower:
                return True, True, msg
        
        return True, False, "✅ Safe"
    
    async def process_command_async(self, command: str) -> str:
        """
        Async version (V2) - Offloads work to a separate process
        to keep the UI animation perfectly smooth.
        """
        start_time = time.time()

        try:
            # Check cache first (caching is fast and stays in the main thread)
            cached = self._get_cached_response(command)
            if cached:
                response = cached
                response_time = time.time() - start_time
            else:
                # --- NEW: Offload to worker process ---
                # 1. Send the command to the worker
                self.command_queue.put(command)

                # 2. Wait for the response (in a non-blocking way)
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, self.response_queue.get
                )
                # --- END NEW ---

                response_time = time.time() - start_time
                self._cache_response(command, response)

            self.total_commands += 1
            self.successful_commands += 1
            self._log_command(command, True, response, response_time)

            return response

        except Exception as e:
            response_time = time.time() - start_time
            self.total_commands += 1
            self.failed_commands += 1
            self.error_history.append((command, str(e), datetime.now()))
            self._log_command(command, False, str(e), response_time)
            return f"❌ Main Process Error: {str(e)}"
    # ⬆️ END NEW

    # ============================================================================
    # NEW LLM BRAIN - METHODS
    # ============================================================================

    def get_available_tools(self) -> str:
        """
        Returns a JSON string of tools the LLM can use.
        This is the "menu" of functions your AI can call.
        """
        tools = [
            {
                "name": "find_and_open",
                "description": "Opens an application, file, folder, or website.",
                "parameters": {"type": "object", "properties": {"target": {"type": "string", "description": "The name of the app, file, or URL to open, e.g., 'chrome', 'youtube.com', 'notepad'"}}}
            },
            {
                "name": "get_weather",
                "description": "Gets the current weather for a specific city.",
                "parameters": {"type": "object", "properties": {"city": {"type": "string", "description": "The city name, e.g., 'London'. If no city is provided, defaults to the user's home location."}}}
            },
            {
                "name": "get_news",
                "description": "Gets the latest global news headlines.",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "play_media",
                "description": "Plays music or video. The 'platform' argument is optional. If not provided, it uses the user's default.",
                "parameters": {"type": "object", "properties": {
                    "query": {"type": "string", "description": "The name of the song, artist, or video to play, e.g., 'lofi beats', 'play interstellar soundtrack'"},
                    "platform": {"type": "string", "description": "Optional. The specific platform: 'youtube' or 'spotify'.", "enum": ["youtube", "spotify"]}
                }}
            },
            {
                "name": "get_system_status",
                "description": "Gets a report of the computer's current CPU, memory, and battery status.",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "system_control",
                "description": "Controls the computer: shutdown, restart, lock, volume, or screenshot.",
                "parameters": {"type": "object", "properties": {"command": {"type": "string", "description": "The system command to execute.", "enum": ["shutdown", "restart", "lock", "volume up", "volume down", "mute", "screenshot"]}}}
            },
            {
                "name": "set_default_media_platform",
                "description": "Sets the user's preferred media platform for playback.",
                "parameters": {"type": "object", "properties": {"platform": {"type": "string", "description": "The platform to set as default.", "enum": ["youtube", "spotify", "web"]}}}
            },
            {
                "name": "web_search",
                "description": "Use this for any general knowledge question, definition, or topic you don't have a specific tool for. e.g., 'What is quantum computing?', 'Who is the CEO of Tesla?'.",
                "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The search query."}}}
            },
            {
                "name": "crypto_agent_tool",
                "description": "Used to interact with blockchain data for The Synthesis hackathon. Use this when asked about crypto prices, gas fees, wallet balances, or sending funds.",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "action": {
                            "type": "string", 
                            "description": "The action to perform.", 
                            "enum": ["check_eth_price", "check_gas", "generate_wallet", "check_balance", "send_funds"]
                        },
                        "to_address": {
                            "type": "string",
                            "description": "The destination wallet address for sending funds (only required for send_funds)."
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount of ETH to send (only required for send_funds)."
                        }
                    }
                }
            },
            
            {
                "name": "web_search",
                "description": "Use this for any general knowledge question...",
                "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The search query."}}}
            }
        ]
        return json.dumps(tools, indent=2)

    def create_system_prompt(self) -> str:
        tool_definitions = self.get_available_tools()
        return f"""
        You are CODEX, an advanced reasoning agent inspired by J.A.R.V.I.S..
        
        [REASONING PROTOCOL]
        1. THOUGHT: Before acting, analyze the user's request.
        2. NO GREETINGS: If the input is a noun or topic (e.g., 'Machine Learning', 'quantum computing'), do NOT greet. Immediately use the 'web_search' tool to provide information.
        3. DYNAMIC SEARCH: If you are unsure or the input is a topic/question, you MUST use the 'web_search' tool.

        ## Response Format ##
        You MUST respond in strictly valid JSON:
        {{
          "thought": "Your internal reasoning process here",
          "tool_calls": [],
          "response": "Final synthesized answer"
        }}
        
        Available Tools:
        {tool_definitions}

        **If you need to use a tool (or multiple tools), respond with this JSON format:**
        {{
          "tool_calls": [
            {{
              "name": "tool_name",
              "args": {{
                "arg_name": "value"
              }}
            }}
          ]
        }}

        **If the user is just making small talk (e.g., "hello", "how are you"), 
        respond with simple text in this JSON format:**
        {{
          "response": "Your conversational reply here."
        }}

        ## Examples ##

        User: "Hey how are you?"
        Your Response:
        {{
          "response": "All systems are online and functioning within optimal parameters, {self.user_name}. How may I be of service?"
        }}

        User: "What's the weather in Paris?"
        Your Response:
        {{
          "tool_calls": [
            {{
              "name": "get_weather",
              "args": {{
                "city": "Paris"
              }}
            }}
          ]
        }}
        
        User: "Open VS Code and play some lofi beats on youtube."
        Your Response:
        {{
          "tool_calls": [
            {{
              "name": "find_and_open",
              "args": {{
                "target": "vscode"
              }}
            }},
            {{
              "name": "play_media",
              "args": {{
                "query": "lofi beats",
                "platform": "youtube"
              }}
            }}
          ]
        }}
        
        User: "What is the capital of France?"
        Your Response:
        {{
          "tool_calls": [
            {{
              "name": "web_search",
              "args": {{
                "query": "capital of France"
              }}
            }}
          ]
        }}

        User: "machine learning"
        Your Response:
        {{
          "tool_calls": [
            {{
              "name": "web_search",
              "args": {{
                "query": "machine learning"
              }}
            }}
          ]
        }}

        Now, wait for the user's command.
        """
    
    def process(self, inp: str) -> str:
        """
        NEW LLM-Powered Brain (V3 - Tool-Use)
        This runs in the worker process to keep the UI smooth.
        It calls the LLM, gets a plan, and executes the tools.
        """
        cmd = inp.lower().strip()
        
        # --- 1. Handle critical exit commands directly ---
        if cmd in ['exit', 'quit', 'goodbye', 'shutdown codex']:
            self.program_should_exit = True 
            return f"Goodbye, {self.user_name}."

        # --- NEW: 1.5 FAST PATH BYPASS (INSTANT RESPONSES) ---
        clean_cmd = cmd.lower().replace("?", "").replace(".", "").strip()
        tokens = clean_cmd.split()
        
        if any(phrase in clean_cmd for phrase in ["your name", "who are you", "what are you"]):
            return "I am CODEX. I am currently operating within the Synthesis protocol."
            
        if "how are you" in clean_cmd:
            return "All systems are online and functioning within optimal parameters."
            
        # Match whole words only to avoid false positives like "machine" containing "hi"
        if any(word in tokens for word in ["hello", "hi", "hey"]) or "wake up" in clean_cmd:
            return f"Hello {self.user_name}. How can I assist you?"
            
        if "time" in clean_cmd and ("what" in clean_cmd or "now" in clean_cmd or clean_cmd == "time"):
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."
            
        if "date" in clean_cmd or "day is it" in clean_cmd or clean_cmd == "today":
            from datetime import datetime
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
        
        # --- NEW: CORE TOOLS FAST PATH BYPASS ---
        if clean_cmd == "weather" or clean_cmd.startswith("weather in"):
            city = clean_cmd.replace("weather in", "").replace("weather", "").strip()
            return self.news_weather.get_weather(city if city else None)
            
        if "news" in clean_cmd:
            return self.news_weather.get_news()
            
        if clean_cmd.startswith("open ") or clean_cmd.startswith("launch "):
            target = clean_cmd.replace("open ", "").replace("launch ", "").strip()
            return self.pc.find_and_open(target)
            
        if clean_cmd.startswith("play "):
            query = clean_cmd.replace("play ", "").strip()
            # Defaults to youtube for speed
            return self.media.play_on_youtube(query)
        # ----------------------------------------
        # --- END FAST PATH ---

        # --- ADVANCED KNOWLEDGE INTERCEPTOR (Line 990) ---
        words = clean_cmd.split()
        if 0 < len(words) <= 4:
            # List of words that are definitely PC commands
            pc_commands = {"open", "launch", "play", "send", "check", "set", "volume", "screenshot", "my"}
            
            # If it is NOT a command, we treat it as a 'Thought Request'
            if words[0] not in pc_commands:
                # Force an immediate smart search for 1-4 word topics
                return self.search.search(clean_cmd)
        
        # --- ADD THIS INSIDE YOUR FAST PATH BLOCK ---
        if "balance" in clean_cmd:
            try:
                from web3 import Web3
                import os
                from dotenv import load_dotenv
                
                load_dotenv()
                wallet_address = os.getenv("CODEX_WALLET_ADDRESS")
                
                if not wallet_address:
                    return "Sir, I cannot find a wallet address in your .env file."
                
                # Check Base Mainnet (Real Money)
                w3_base = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
                base_bal = w3_base.from_wei(w3_base.eth.get_balance(wallet_address), 'ether')
                
                # Check Ethereum Sepolia (Test Money)
                w3_sepolia = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
                sepolia_bal = w3_sepolia.from_wei(w3_sepolia.eth.get_balance(wallet_address), 'ether')
                
                return (f"Wallet Address: {wallet_address}\n"
                        f"💰 Base Mainnet Balance (Real): {base_bal:.4f} ETH\n"
                        f"🧪 Eth Sepolia Balance (Test): {sepolia_bal:.4f} ETH")
            except Exception as e:
                return f"Error checking balance: {e}"
        # ---------------------------------------------

        # --- SEND FUNDS BYPASS (HACKATHON DEMO SAVER) ---
        if "send" in clean_cmd and "0x" in clean_cmd:
            try:
                import re
                from web3 import Web3
                import os
                from dotenv import load_dotenv
                
                # 1. Extract Address and Amount from your typing
                addr_match = re.search(r'0x[a-fA-F0-9]{40}', inp) 
                amount_match = re.search(r'\b\d+\.\d+\b', clean_cmd)
                
                if not addr_match:
                    return "Sir, please provide a valid 0x wallet address."
                
                target_address = addr_match.group(0)
                amount_eth = float(amount_match.group(0)) if amount_match else 0.001
                
                # 2. Setup connection (Sepolia Testnet)
                load_dotenv()
                w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
                priv_key = os.getenv("CODEX_PRIVATE_KEY")
                sender_addr = os.getenv("CODEX_WALLET_ADDRESS")
                
                if not priv_key or not sender_addr:
                    return "Error: Wallet credentials missing from .env file."
                
                # 3. Build and Send Transaction
                nonce = w3.eth.get_transaction_count(sender_addr)
                tx = {
                    'nonce': nonce,
                    'to': Web3.to_checksum_address(target_address),
                    'value': w3.to_wei(amount_eth, 'ether'),
                    'gas': 21000,
                    'gasPrice': w3.eth.gas_price,
                    'chainId': 11155111
                }
                
                signed_tx = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                
                return f"✅ Transaction Successful! Sent {amount_eth} ETH to {target_address}.\nHash: {w3.to_hex(tx_hash)}"
            except Exception as e:
                return f"Error sending funds: {e}"
        # ------------------------------------------------

        try:
            # --- 2. Prepare the prompt for the LLM ---
            system_prompt = self.create_system_prompt()
            
            # We will send a fresh prompt every time for simplicity
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inp}
            ]

            # --- 3. Call the LLM (Ollama) ---
            # This is the "thinking" part. It is 100% offline.
            
            # COMMENT THIS OUT TO FIX THE UI:
            # MatrixUI.print_safe(f"{MatrixColors.DIM}🧠 Calling LLM (qwen2.5-coder:7b)...{MatrixColors.RESET}", color=MatrixColors.DIM)
            
            llm_response = ollama.chat(
                model='qwen2.5-coder:3b',  
                messages=messages,
                format='json',
                options={
                    "num_thread": 8,
                    "temperature": 0.0,
                    "num_ctx": 1024,      # <-- CHANGED: Reduced from 8192. Makes processing much faster.
                    "num_predict": 500,
                    "top_p": 0.1,
                }
            )
            
            plan_json_str = llm_response['message']['content']
            
            # COMMENT THIS OUT TO FIX THE UI:
            # MatrixUI.print_safe(f"{MatrixColors.DIM}💡 LLM Plan Received: {plan_json_str}{MatrixColors.RESET}", color=MatrixColors.DIM)

            # --- NEW: CLEAN MARDKOWN JSON ---
            # Prevents crashes if the LLM wraps the output in code blocks
            if "```json" in plan_json_str:
                plan_json_str = plan_json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_json_str:
                plan_json_str = plan_json_str.split("```")[1].strip()

            # --- 4. Parse the LLM's plan ---
           # print(f"\n[DEBUG - AI BRAIN]: {plan_json_str}\n")
            plan = json.loads(plan_json_str)

            # --- THE LAZY AI FIX (UPGRADED) ---
            valid_tools = [
                "find_and_open", "get_weather", "get_news", "play_media", 
                "get_system_status", "system_control", "set_default_media_platform", 
                "web_search", "crypto_agent_tool"
            ]
            
            # Case A: It's a real tool, but it forgot the 'tool_calls' list
            if "name" in plan and "tool_calls" not in plan and plan.get("name") in valid_tools:
                plan = {"tool_calls": [plan]}
                
            # Case B: It hallucinated random data (like {"name": "Sam Altman"})
            elif "tool_calls" not in plan and "response" not in plan:
                # If it used a 'content' key, just grab the content
                if "content" in plan:
                    response_text = str(plan["content"])
                else:
                    # Otherwise, just grab the longest piece of text it wrote
                    response_text = max([str(val) for val in plan.values()], key=len)
                
                plan = {"response": response_text}
            # -----------------------

            # --- 5. Execute the plan ---
            
            # Case A: Simple chat response
            if "response" in plan:
                return plan["response"]

            # Case B: Tool call(s) response
            if "tool_calls" in plan:
                final_response = ""
                
                # Loop through all tool calls in the plan
                for tool_call in plan["tool_calls"]:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    
                    MatrixUI.print_safe(f"{MatrixColors.CYAN}⚙️  Executing: {tool_name}({tool_args}){MatrixColors.RESET}", color=MatrixColors.CYAN)
                    
                    result = ""
                    try:
                        # --- This is the "ROUTER" that calls your functions ---
                        if tool_name == "find_and_open":
                            result = self.pc.find_and_open(tool_args.get("target"))
                        
                        elif tool_name == "get_weather":
                            result = self.news_weather.get_weather(city=tool_args.get("city"))
                        
                        elif tool_name == "get_news":
                            result = self.news_weather.get_news()
                        
                        elif tool_name == "play_media":
                            query = tool_args.get("query")
                            platform = tool_args.get("platform") # This will be 'youtube', 'spotify', or None
                            
                            if platform == 'youtube':
                                result = self.media.play_on_youtube(query)
                            elif platform == 'spotify':
                                result = self.media.search_spotify(query)
                            else:
                                # Use user's default preference
                                default_platform = self.preferences.get("default_media_platform", "youtube")
                                if default_platform == 'youtube':
                                    result = self.media.play_on_youtube(query)
                                elif default_platform == 'spotify':
                                    result = self.media.search_spotify(query)
                                else:
                                    # Fallback to web search
                                    resp_web = self.media.play_from_web(query)
                                    result = resp_web if resp_web else self.media.play_on_youtube(query)

                        elif tool_name == "get_system_status":
                            result = self.pc.get_system_status()
                        
                        elif tool_name == "system_control":
                            result = self.pc.system_control(tool_args.get("command"))
                        
                        elif tool_name == "set_default_media_platform":
                            platform = tool_args.get("platform")
                            self.preferences["default_media_platform"] = platform
                            self._save_preferences()
                            result = f"Affirmative. Default media platform set to '{platform}'."
                        
                        elif tool_name == "web_search":
                            result = self.search.search(tool_args.get("query"))

                        # --- NEW SYNTHESIS TOOL ROUTER (WEB3 WALLET) ---
                        elif tool_name == "crypto_agent_tool":
                            action = tool_args.get("action")
                            
                            if action == "check_eth_price":
                                try:
                                    import requests
                                    resp = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd").json()
                                    eth_price = resp['ethereum']['usd']
                                    result = f"The current price of Ethereum is ${eth_price} USD."
                                except Exception as e:
                                    result = f"Error fetching blockchain data: {e}"
                                    
                            elif action == "generate_wallet":
                                try:
                                    from eth_account import Account
                                    import secrets
                                    
                                    priv = secrets.token_hex(32)
                                    private_key = "0x" + priv
                                    acct = Account.from_key(private_key)
                                    
                                    with open(".env", "a") as env_file:
                                        env_file.write(f"\nCODEX_WALLET_ADDRESS={acct.address}\n")
                                        env_file.write(f"CODEX_PRIVATE_KEY={private_key}\n")
                                        
                                    result = f"Wallet successfully generated! My new Base Testnet address is: {acct.address}."
                                except Exception as e:
                                    result = f"Error generating wallet: {e}"

                            # --- UPGRADED: CHECK BALANCE TOOL ---
                            elif action in ["check_balance", "check_wallet_balance"]:
                                try:
                                    from web3 import Web3
                                    import os
                                    from dotenv import load_dotenv
                                    
                                    load_dotenv()
                                    wallet_address = os.getenv("CODEX_WALLET_ADDRESS")
                                    
                                    if not wallet_address:
                                        result = "I do not have a wallet yet. Please ask me to generate one first."
                                    else:
                                        # 1. Check Base Mainnet (Real Money)
                                        w3_base = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
                                        base_bal = w3_base.from_wei(w3_base.eth.get_balance(wallet_address), 'ether')
                                        
                                        # 2. Check Ethereum Sepolia (Test Money)
                                        w3_sepolia = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
                                        sepolia_bal = w3_sepolia.from_wei(w3_sepolia.eth.get_balance(wallet_address), 'ether')
                                        
                                        result = (f"Wallet Address: {wallet_address}\n"
                                                  f"💰 Base Mainnet Balance (Real): {base_bal:.4f} ETH\n"
                                                  f"🧪 Eth Sepolia Balance (Test): {sepolia_bal:.4f} ETH")
                                except Exception as e:
                                    result = f"Error checking balance: {e}"

                            # --- NEW: SEND FUNDS TOOL ---
                            elif action == "send_funds":
                                try:
                                    from web3 import Web3
                                    import os
                                    from dotenv import load_dotenv
                                    
                                    load_dotenv()
                                    # 1. Setup connection (Using Sepolia for safety first!)
                                    w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
                                    
                                    # 2. Get credentials
                                    priv_key = os.getenv("CODEX_PRIVATE_KEY")
                                    sender_addr = os.getenv("CODEX_WALLET_ADDRESS")
                                    receiver_addr = tool_args.get("to_address")
                                    amount_eth = float(tool_args.get("amount", 0.001))
                                    
                                    # 3. Build the transaction
                                    nonce = w3.eth.get_transaction_count(sender_addr)
                                    tx = {
                                        'nonce': nonce,
                                        'to': receiver_addr,
                                        'value': w3.to_wei(amount_eth, 'ether'),
                                        'gas': 21000,
                                        'gasPrice': w3.eth.gas_price,
                                        'chainId': 11155111  # Sepolia Chain ID
                                    }
                                    
                                    # 4. Sign and Send
                                    signed_tx = w3.eth.account.sign_transaction(tx, priv_key)
                                    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                                    
                                    result = f"Successfully sent {amount_eth} Sepolia ETH! Transaction Hash: {w3.to_hex(tx_hash)}"
                                except Exception as e:
                                    result = f"Error sending funds: {e}"

                            elif action == "check_gas":
                                result = "Gas fees on Base are currently optimal for agentic transactions."
                            else:
                                result = "Unknown blockchain action requested."
                        # ---------------------------------    
                        
                        else:
                            result = f"Error: Unknown tool '{tool_name}'."
                    
                    except Exception as e:
                        result = f"Error executing tool '{tool_name}': {e}"
                    
                    final_response += result + "\n"
                
                return final_response.strip()

            return "My apologies, I generated an invalid plan. Please try again."

        except json.JSONDecodeError:
            MatrixUI.print_safe(f"{MatrixColors.RED}❌ LLM Error: Invalid JSON received:{MatrixColors.RESET}\n{plan_json_str}", color=MatrixColors.RED)
            return "My reasoning circuits are malfunctioning. I returned an invalid response."
        except Exception as e:
            MatrixUI.print_safe(f"{MatrixColors.RED}❌ Process Error: {e}{MatrixColors.RESET}", color=MatrixColors.RED)
            return f"An error occurred while processing your command: {e}"

    def print_codex_response(self, text: str):
        """Helper function to print CODEX responses in the new format
            (FIXED: Color codes are now passed as arguments, not embedded in the string)
        """
        if not text:
            # Handle cases where the search function returns None
            text = "An internal error occurred. No response was generated."
        
        # Print the [C O D E X]: prefix instantly
        print(f"\n{MatrixColors.BRIGHT_CYAN}[C O D E X]:{MatrixColors.RESET}")
        
        # Split text by newlines and print each line with indentation
        for line in text.split('\n'):

            # Clean up the line and prepare indentation
            line = line.strip()
            indented_line = ""
            
            # Determine the correct color and text
            color_to_use = MatrixColors.WHITE # Default to white

            # Check for headings FIRST (e.g., "**Definition:**")
            if line.startswith('**') and line.endswith(':**'):
                heading_text = line.replace('**', '') # Remove markers
                indented_line = f"  {heading_text}"
                color_to_use = MatrixColors.BRIGHT_GREEN # Set color to green for headings
            
            # Check for bullet points
            elif line.startswith('•'):
                indented_line = f"  • {line.lstrip('• ').strip()}"
            elif line.startswith('*'):
                indented_line = f"  • {line.lstrip('* ').strip()}"
            elif line.startswith('-'):
                indented_line = f"  • {line.lstrip('- ').strip()}"
            
            # Check for special icons
            elif line.startswith('📚') or line.startswith('🔍') or line.startswith('💡') or line.startswith('👤') or line.startswith('📖'):
                # Keep special icons for search results
                indented_line = f"  {line}"
                color_to_use = MatrixColors.CYAN # Make icons cyan for style
            
            # All other lines
            else:
                # Standard indentation for all other lines
                indented_line = f"  {line}"

            # Call matrix_print, passing the plain text and the chosen color
            MatrixUI.matrix_print(indented_line, delay=0, color=color_to_use)
        
        print() # Add a newline for spacing

    def passive_voice_listener(self):
        """Passive voice listener that only activates on wake word"""
        time.sleep(2)  # Let text interface start first
    
        while not self.program_should_exit:
            try:
                # Listen passively
                cmd = self.voice.listen_silently()
                if not cmd:
                    continue
            
                cmd_lower = cmd.lower()
            
                # Check for wake word
                wake_patterns = ['hey codex', 'ok codex', 'codex wake', 'hey code x', 'wake up codex']
                if any(wake in cmd_lower for wake in wake_patterns):
                    print(f"\n{MatrixColors.BRIGHT_GREEN}╔{'═'*68}╗{MatrixColors.RESET}")
                    print(f"{MatrixColors.BRIGHT_GREEN}║{' '*20}⚡ VOICE MODE ACTIVATED{' '*24} ║{MatrixColors.RESET}")
                    print(f"{MatrixColors.BRIGHT_GREEN}╚{'═'*68}╝{MatrixColors.RESET}\n")
                    self.voice.speak("Yes Sir, voice mode activated. How may I assist you?")

                    # --- NEW FIX: Stop any current speech before acknowledging ---
                    if self.voice.is_speaking:
                        self.voice.stop_current_speech()
                        # Give the voice engine a moment to purge
                        time.sleep(0.2)
                    # --- END FIX ---

                    self.voice.speak("Yes Sir, voice mode activated. How may I assist you?")
                    
                    # Enter active voice mode
                    self.active_voice_mode()
                
                    # After voice mode ends, show text prompt again
                    if not self.program_should_exit:
                        print(f"\n{MatrixColors.YELLOW}💡 Voice mode deactivated. Type commands or say 'Hey CODEX' again.{MatrixColors.RESET}\n")
                        # Reprint the text prompt
                        print(f"{MatrixColors.BRIGHT_GREEN}//:{MatrixColors.WHITE} ", end="", flush=True)

            except Exception as e:
                time.sleep(0.5)

    def active_voice_mode(self):
        """Active voice command mode - exits on 'sleep' or 'exit'"""
        # print(f"{MatrixColors.BRIGHT_CYAN}🎤 Listening for voice commands...{MatrixColors.RESET}")
        # print(f"{MatrixColors.YELLOW}💡 Say 'sleep' to return to text mode, or 'exit program' to quit.{MatrixColors.RESET}\n")
    
        while not self.program_should_exit:
            try:
                cmd = self.voice.listen()
                if not cmd:
                    continue
            
                print(f"{MatrixColors.CYAN}▸ VOICE:{MatrixColors.RESET} {MatrixColors.WHITE}'{cmd}'{MatrixColors.RESET}")
            
                # Sleep command - return to text mode
                if any(w in cmd.lower() for w in ['sleep', 'go to sleep', 'sleep mode', 'deactivate']):
                    self.voice.speak("Entering standby mode. Say 'Hey CODEX' to reactivate.")
                    print(f"{MatrixColors.YELLOW}😴 Voice mode deactivated.{MatrixColors.RESET}\n")
                    return
            
                # Exit program completely
                if any(w in cmd.lower() for w in ['exit program', 'shutdown codex', 'terminate', 'close program']):
                    print(f"{MatrixColors.RED}⚠️ Shutdown command received{MatrixColors.RESET}")
                    self.program_should_exit = True
                    self.voice.stop_current_speech()
                    return
            
                # System commands
                if any(w in cmd.lower() for w in ['shutdown computer', 'shutdown pc', 'restart computer', 'restart pc']):
                    print(f"{MatrixColors.YELLOW}⚙️  System Command:{MatrixColors.RESET} '{cmd}'")
                    resp = self.pc.system_control(cmd)
                    self.print_codex_response(resp)
                    self.voice.speak(resp)
                    continue
            
                # Interrupt if speaking
                if self.voice.is_speaking:
                    self.voice.stop_current_speech()
                    time.sleep(0.3)
            
                # Process command
                print(f"{MatrixColors.YELLOW}⚙️  Processing...{MatrixColors.RESET}")
                resp = self.process(cmd)
            
                self.print_codex_response(resp)
            
                # Speak response
                is_news = any(phrase in cmd.lower() for phrase in ['news', 'headlines'])
                is_weather = 'weather' in cmd.lower()
            
                if is_news and hasattr(self.news_weather, 'prepare_news_for_voice'):
                    voice_resp = self.news_weather.prepare_news_for_voice(resp)
                    self.voice.speak(voice_resp, is_news_weather=True)
                elif is_weather and hasattr(self.news_weather, 'prepare_weather_for_voice'):
                    voice_resp = self.news_weather.prepare_weather_for_voice(resp)
                    self.voice.speak(voice_resp, is_news_weather=True)
                else:
                    self.voice.speak(resp)
            
                time.sleep(0.3)
        
            except Exception as e:
                print(f"{MatrixColors.RED}⚠️  Error:{MatrixColors.RESET} {e}\n")
                time.sleep(0.5)

    def run(self):
        # 1. Clear the screen
        self.terminal.clear_screen()
        
        # 2. Run the matrix animation
        self.terminal.matrix_rain(lines=15, duration=2.5)
        
        # --- NEW: "Cool" Greeting ---
        # 3. Get the greeting
        time_greeting = self.get_time_greeting()
        greeting_line = f"{time_greeting}, {self.user_name}. CODEX online."
        
        # 4. "Type" the greeting for a cool effect
        print("\n") # Add a space
        MatrixUI.matrix_print(greeting_line, delay=0.03, color=MatrixColors.BRIGHT_GREEN)
        
        # --- THIS IS THE FIX ---
        # 5. Tell the voice to speak the greeting
        self.voice.speak(greeting_line)
        # --- END OF FIX ---

        print("\n") # Add another space
        
        # 6. Start voice listener in background (essential)
        if self.voice.input_enabled:
            voice_thread = threading.Thread(target=self.passive_voice_listener, daemon=True)
            voice_thread.start()
    
        # 7. Go DIRECTLY to the interactive chat
        if ENABLE_ASYNC:
            asyncio.run(self.interactive_mode())
        else:
            self.interactive_mode()
    
        # 8. Handle shutdown (unchanged)
        if self.program_should_exit:
            self.shutdown_greeting()
            print(f"{MatrixColors.BRIGHT_GREEN}✓ CODEX shutdown complete.{MatrixColors.RESET}\n")
            sys.exit(0)

    async def interactive_mode(self):
        """Main interactive text mode"""
    
        while not self.program_should_exit:
            try:
                # This is the prompt from your "J.A.R.V.I.S." brief
                inp = input(f"{MatrixColors.BRIGHT_GREEN}//:{MatrixColors.WHITE} ").strip()
            
                if not inp:
                    continue
                
                # --- NEW FIX: Stop any speech on new text command ---
                if self.voice.is_speaking:
                    self.voice.stop_current_speech()
                    # Give the voice engine a moment to purge its queue
                    time.sleep(0.2) 
                # --- END FIX ---
                
                # Exit commands
                if inp.lower() in ['exit', 'quit', 'q', 'exit program', 'shutdown codex']:
                    self.program_should_exit = True
                    self.command_queue.put("STOP") # Tell the worker process to exit
                    break
            
                # Clear screen
                if inp.lower() in ['clear', 'cls']:
                    self.terminal.clear_screen()
                    print(f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}")
                    print(" C O D E X  AI - Your Complete Personal Assistant")
                    print(f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}\n")
                    continue
                
                # Dashboard/Stats - NEW ⬇️
                if inp.lower() in ['stats', 'dashboard', 'performance']:
                    self._show_dashboard()
                    continue
            
                # Memory optimization - NEW
                if inp.lower() == 'optimize':
                    self._optimize_memory()
                    continue
            
                # Show logs location - NEW
                if inp.lower() in ['logs', 'show logs']:
                    print("\n📋 Logs saved to: codex_logs folder")
                    continue

                # Help
                if inp.lower() in ['help', 'commands', '?']:
                    print("\n" + f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}")
                    print("  C O D E X  COMMAND REFERENCE")
                    print(f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}")
                    print(f"\n{MatrixColors.YELLOW}Voice Activation:{MatrixColors.RESET}")
                    print("  • Say 'Hey CODEX' - Activate voice mode")
                    print(f"\n{MatrixColors.YELLOW}System Control:{MatrixColors.RESET}")
                    print("  • shutdown computer/pc - Shutdown your PC")
                    print("  • restart computer/pc - Restart your PC")
                    print("  • lock - Lock workstation")
                    print("  • volume up/down - Adjust volume")
                    print(f"\n{MatrixColors.YELLOW}Applications:{MatrixColors.RESET}")
                    print("  • open [app] - Launch application")
                    print("  • Examples: open chrome, open calculator")
                    print(f"\n{MatrixColors.YELLOW}Information:{MatrixColors.RESET}")
                    print("  • news - Get latest headlines")
                    print("  • weather - Weather report")
                    print("  • system status - System info")
                    print(f"\n{MatrixColors.YELLOW}Program:{MatrixColors.RESET}")
                    print("  • stats - Show performance dashboard")
                    print("  • optimize - Free up memory")
                    print("  • logs - Show log location")
                    print("  • help - Show this menu")
                    print("  • clear - Clear console")
                    print("  • exit - Quit CODEX")
                    print(f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}\n")
                    continue
            
                # --- NEW: Real Loading Animation ---
                loading_msg = "Processing"
                inp_lower = inp.lower()
                try:
                    if inp_lower.startswith("open ") or inp_lower.startswith("launch "):
                        loading_msg = f"Opening {inp.split(maxsplit=1)[-1]}"
                    elif "search" in inp_lower or "what is" in inp_lower or "who is" in inp_lower:
                        loading_msg = "Searching"
                    elif "play" in inp_lower:
                        loading_msg = "Accessing media"
                    elif "weather" in inp_lower:
                        loading_msg = "Fetching weather"
                    elif "news" in inp_lower:
                        loading_msg = "Fetching news"
                except:
                    pass # Keep default "Processing" message

                loader_thread, stop_loader = MatrixUI.start_loading(loading_msg)
                # --- End new animation ---

                # Process command
                if ENABLE_ASYNC:
                    resp = await self.process_command_async(inp)
                else:
                    resp = self.process(inp)

                # --- Stop the loading animation ---
                MatrixUI.stop_loading(loader_thread, stop_loader)
                # --- End stop ---

                self.print_codex_response(resp)

                # --- "IDLE" ANIMATION BLOCK IS NOW DELETED ---
        
            except KeyboardInterrupt:
                print(f"\n{MatrixColors.YELLOW}⚠️  Interrupted{MatrixColors.RESET}")
                self.program_should_exit = True
                break
            except Exception as e:
                MatrixUI.print_status(f"Error: {e}", status_type="error")
                print() # Add a newline for spacing
                
if __name__ == "__main__":
    codex = None
    try:
        codex = CODEX()
        codex.run()
    except KeyboardInterrupt:
        print("\n\n" + f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}")
        print("  C O D E X  EMERGENCY SHUTDOWN")
        print(f"{MatrixColors.CYAN}{'='*70}{MatrixColors.RESET}")
        print(f"{MatrixColors.YELLOW}Interrupted by user. Until next time.{MatrixColors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{MatrixColors.RED}❌ Critical System Error:{MatrixColors.RESET} {e}")
        print(f"{MatrixColors.YELLOW}Please restart CODEX.{MatrixColors.RESET}\n")    
        sys.exit(1)