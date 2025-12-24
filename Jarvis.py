
import asyncio
import aiohttp
import pyttsx3
import datetime
import webbrowser
import os
import json
import pyautogui
import psutil
import time
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
import sys
import random
import warnings
warnings.filterwarnings("ignore")

print(f"Python version: {sys.version}")

class FixedVoiceAssistant:
    def __init__(self, name: str = "Jarvis"):
        self.name = name
        self.engine = None
        self.recognizer = None
        self.setup_complete = False
        self.microphone_available = False
        
    
        self.config_file = Path("assistant_config.json")
        self.load_config()
        
      
        self.commands = {
            'time': self.get_time,
            'date': self.get_date,
            'open': self.open_website,
            'play': self.play_youtube,
            'search': self.search_web,
            'weather': self.get_weather_async,
            'note': self.take_note,
            'timer': self.set_timer,
            'calculate': self.calculate,
            'joke': self.tell_joke,
            'screenshot': self.take_screenshot,
            'system': self.system_info,
            'translate': self.translate_text,
            'remind': self.set_reminder,
            'music': self.play_music,
            'movie': self.suggest_movie,
            'quote': self.inspirational_quote,
            'help': self.show_help,
            'exit': self.exit_assistant,
            'clear': self.clear_screen,
            'files': self.list_files,
            'ip': self.get_ip_address,
            'cpu': self.get_cpu_info,
            'ram': self.get_ram_info,
            'disk': self.get_disk_info,
            'battery': self.get_battery_info,
            'process': self.list_processes,
            'shutdown': self.shutdown_assistant,
            'restart': self.restart_assistant,
            'config': self.show_config,
            'rename': self.rename_assistant
        }
        
        self.setup()
    
    def load_config(self) -> None:
        """Load or create configuration"""
        default_config = {
            "assistant_name": "Jarvis",
            "speech_rate": 180,
            "voice_gender": "female",
            "user_preferences": {
                "name": "User",
                "city": "New York",
                "language": "en"
            },
            "features": {
                "voice_input": False,
                "sound_effects": True,
                "auto_update": False
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                print(f"✅ Configuration loaded from {self.config_file}")
                
               
                if "features" not in self.config:
                    self.config["features"] = default_config["features"]
                if "user_preferences" not in self.config:
                    self.config["user_preferences"] = default_config["user_preferences"]
                if "assistant_name" not in self.config:
                    self.config["assistant_name"] = self.name
                if "speech_rate" not in self.config:
                    self.config["speech_rate"] = default_config["speech_rate"]
                if "voice_gender" not in self.config:
                    self.config["voice_gender"] = default_config["voice_gender"]
                    
            except Exception as e:
                print(f"⚠️ Config error: {e}, creating new one")
                self.config = default_config
                self.save_config()
        else:
            self.config = default_config
            self.save_config()
            print(f"📝 Configuration file created: {self.config_file}")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup(self) -> None:
        """Initialize all components"""
        try:
            
            self.engine = pyttsx3.init()
            print("✅ Text-to-speech engine initialized")
            
           
            voices = self.engine.getProperty('voices')
            if len(voices) > 0:
                print(f"🎤 Found {len(voices)} voice(s)")
                voice_gender = self.config.get('voice_gender', 'female')
                voice_index = 1 if voice_gender == 'female' else 0
                if voice_index < len(voices):
                    self.engine.setProperty('voice', voices[voice_index].id)
                    print(f"✅ Voice set: {voices[voice_index].name}")
            
            self.engine.setProperty('rate', self.config.get('speech_rate', 180))
            
            
            self.setup_speech_recognition()
            
            self.setup_complete = True
            
            user_name = self.config.get("user_preferences", {}).get("name", "User")
            city = self.config.get("user_preferences", {}).get("city", "New York")
            
            print(f"\n{'='*60}")
            print(f"✅ {self.name} Assistant v1.0")
            print(f"👤 User: {user_name}")
            print(f"📍 Location: {city}")
            print(f"🎤 Microphone: {'Available' if self.microphone_available else 'Not available'}")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"⚠️ Setup warning: {e}")
            print("📝 Running with limited features")
            self.setup_complete = True
    
    def setup_speech_recognition(self):
        """Setup speech recognition with detailed troubleshooting"""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            print("✅ Speech recognition module loaded")
            
            try:
                print("🔍 Checking for microphones...")
                mic_list = sr.Microphone.list_microphone_names()
                
                if len(mic_list) == 0:
                    print("❌ No microphones found!")
                    self.microphone_available = False
                    self.config["features"]["voice_input"] = False
                else:
                    print(f"✅ Found {len(mic_list)} microphone(s):")
                    for i, mic_name in enumerate(mic_list):
                        print(f"   {i}: {mic_name}")
                    
                    try:
                        with sr.Microphone() as mic:
                            print(f"✅ Default microphone: {mic_list[0]}")
                            self.microphone_available = True
                            self.config["features"]["voice_input"] = True
                            print("🎤 Voice input enabled!")
                    except Exception as mic_error:
                        print(f"❌ Could not access microphone: {mic_error}")
                        self.microphone_available = False
                        self.config["features"]["voice_input"] = False
                        
            except Exception as e:
                print(f"❌ Error checking microphones: {e}")
                self.microphone_available = False
                self.config["features"]["voice_input"] = False
                
        except ImportError:
            print("❌ SpeechRecognition not installed")
            print("💡 Install it with: pip install SpeechRecognition")
            self.microphone_available = False
            self.config["features"]["voice_input"] = False
        except Exception as e:
            print(f"❌ Speech recognition setup failed: {e}")
            self.microphone_available = False
            self.config["features"]["voice_input"] = False
    
    def speak(self, text: str, speed: float = 1.0) -> None:
        """Convert text to speech with optional speed control"""
        text = str(text).replace('[sound]', '').replace('[music]', '')
        
        print(f"🤖 {self.name}: {text}")
        
        if self.engine:
            try:
                if speed != 1.0:
                    current_rate = self.engine.getProperty('rate')
                    self.engine.setProperty('rate', int(current_rate * speed))
                
                self.engine.say(text)
                self.engine.runAndWait()
                
                if speed != 1.0:
                    self.engine.setProperty('rate', self.config.get('speech_rate', 180))
            except Exception as e:
                print(f"⚠️ Speech error: {e}")
        else:
            time.sleep(len(text) * 0.03)  
    
    async def get_input(self) -> Optional[str]:
        """Get input from user with voice or text"""
        try:
            voice_enabled = self.config.get("features", {}).get("voice_input", False)
            
            if voice_enabled and self.microphone_available and self.recognizer:
                print("\n" + "="*50)
                print("🎤 VOICE MODE ACTIVE")
                print("="*50)
                print("Speak your command after the beep...")
                print("Say 'text mode' to switch to typing")
                print("="*50)
                
                try:
                    import winsound
                    winsound.Beep(1000, 300)
                except:
                    print("🔔 (beep sound)")
                
                try:
                    import speech_recognition as sr
                    with sr.Microphone() as source:
                        print("\n🎤 Listening... (speak now)")
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                        
                        try:
                            command = self.recognizer.recognize_google(audio)
                            print(f"👤 You said: {command}")
                            
                            if 'text mode' in command.lower() or 'type' in command.lower():
                                print("🔄 Switching to text input mode...")
                                self.speak("Switching to text mode")
                                return await self.get_text_input()
                            
                            return command.lower().strip()
                            
                        except sr.UnknownValueError:
                            print("❌ Could not understand audio")
                            self.speak("Sorry, I didn't catch that. Please try again.")
                            return await self.get_input()
                        except sr.RequestError as e:
                            print(f"❌ Speech recognition error: {e}")
                            self.speak("Speech recognition service is unavailable.")
                            return await self.get_text_input()
                            
                except sr.WaitTimeoutError:
                    print("⏰ No voice detected, switching to text...")
                    return await self.get_text_input()
                except Exception as e:
                    print(f"🎤 Voice input error: {e}")
                    return await self.get_text_input()
            
            return await self.get_text_input()
            
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    async def get_text_input(self) -> str:
        """Get text input from user"""
        print("\n" + "="*50)
        print("📝 TEXT MODE")
        print("="*50)
        print("Type your command (or 'voice mode' to switch):")
        command = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
        
        if 'voice mode' in command.lower() or 'speak' in command.lower():
            if self.microphone_available:
                print("🔄 Switching to voice input mode...")
                self.speak("Switching to voice mode")
                self.config["features"]["voice_input"] = True
                self.save_config()
            else:
                print("❌ Voice mode not available - microphone not detected")
                self.speak("Voice mode is not available. Please check your microphone.")
        
        return command.lower().strip()
    
    def get_time(self) -> None:
        """Get current time"""
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        hour = now.hour
        
        greetings = {
            range(5, 12): "morning",
            range(12, 17): "afternoon",
            range(17, 21): "evening"
        }
        
        time_of_day = "night"
        for time_range, greeting in greetings.items():
            if hour in time_range:
                time_of_day = greeting
                break
        
        self.speak(f"Good {time_of_day}! The current time is {current_time}")
    
    def get_date(self) -> None:
        """Get current date"""
        today = datetime.datetime.now()
        date_str = today.strftime("%A, %B %d, %Y")
        day_num = today.day
        suffix = "th" if 11 <= day_num <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day_num % 10, "th")
        self.speak(f"Today is {today.strftime('%A')}, {today.strftime('%B')} {day_num}{suffix}, {today.year}")
    
    def open_website(self, site: str = "") -> None:
        """Open websites"""
        websites = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "github": "https://github.com",
            "gmail": "https://gmail.com",
            "chatgpt": "https://chat.openai.com",
            "reddit": "https://reddit.com",
            "spotify": "https://open.spotify.com",
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://linkedin.com",
            "whatsapp": "https://web.whatsapp.com",
            "netflix": "https://netflix.com",
            "amazon": "https://amazon.com",
            "wikipedia": "https://wikipedia.org",
            "stackoverflow": "https://stackoverflow.com"
        }
        
        if not site:
            self.speak("Available websites: " + ", ".join(sorted(websites.keys())))
            return
        
        site_lower = site.lower()
        if site_lower in websites:
            webbrowser.open(websites[site_lower])
            self.speak(f"Opening {site}")
        elif "." in site_lower: 
            if not site_lower.startswith(('http://', 'https://')):
                site_lower = f"https://{site_lower}"
            webbrowser.open(site_lower)
            self.speak(f"Opening {site}")
        else:
            
            webbrowser.open(f"https://www.google.com/search?q={site.replace(' ', '+')}")
            self.speak(f"Searching for {site} on Google")
    
    def play_youtube(self, query: str = "") -> None:
        """Play YouTube video"""
        if query:
            self.speak(f"Searching YouTube for {query}")
            query_encoded = query.replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
        else:
            self.speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
    
    def search_web(self, query: str = "") -> None:
        """Search the web"""
        if query:
            self.speak(f"Searching for {query}")
            query_encoded = query.replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={query_encoded}")
        else:
            self.speak("What would you like to search for?")
    
    async def get_weather_async(self, city: str = "") -> None:
        """Get weather information"""
        if not city:
            
            city = self.config.get("user_preferences", {}).get("city", "New York")
        
        
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy", "snowy"]
        temp_c = random.randint(15, 35)
        temp_f = int(temp_c * 9/5 + 32)
        humidity = random.randint(40, 90)
        condition = random.choice(conditions)
        
       
        if temp_c > 30:
            clothing = "light clothing"
        elif temp_c > 20:
            clothing = "a t-shirt"
        elif temp_c > 10:
            clothing = "a jacket"
        else:
            clothing = "a warm coat"
        
        self.speak(
            f"In {city}, it's {temp_c}°C ({temp_f}°F) and {condition}. "
            f"Humidity is {humidity}%. You might want to wear {clothing}."
        )
    
    def take_note(self, note: str = "") -> None:
        """Take and save notes"""
        if not note:
            self.speak("What would you like me to note down?")
            return
        
        notes_file = Path("notes.txt")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(notes_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {note}\n")
            
            self.speak("Note saved successfully!")
            print(f"📝 Saved to notes.txt")
            
            # Show last 3 notes
            if notes_file.exists():
                with open(notes_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        print("\n📋 Recent notes:")
                        for line in lines[-3:]:
                            print(f"  • {line.strip()}")
        except Exception as e:
            print(f"Note error: {e}")
            self.speak("Sorry, I couldn't save the note.")
    
    def set_timer(self, minutes: str = "") -> None:
        """Set a timer"""
        try:
            if not minutes:
                self.speak("For how many minutes?")
                return
            
           
            import re
            numbers = re.findall(r'\d+', minutes)
            if not numbers:
                self.speak("Please specify a number of minutes.")
                return
            
            mins = int(numbers[0])
            if mins <= 0:
                self.speak("Please specify a positive number.")
                return
            if mins > 180: 
                self.speak("Maximum timer is 3 hours (180 minutes).")
                return
            
            self.speak(f"Timer set for {mins} minute{'s' if mins != 1 else ''}!")
            print(f"⏰ Timer started: {mins} minute{'s' if mins != 1 else ''}")
            
            
            def timer_task():
                for i in range(mins * 60, 0, -1):
                    if i % 60 == 0 and i != mins * 60:  
                        remaining_mins = i // 60
                        print(f"⏰ {remaining_mins} minute{'s' if remaining_mins != 1 else ''} remaining...")
                    time.sleep(1)
                
               
                self.speak("⏰ Timer is up! Time's over!")
             
                try:
                    import winsound
                    for _ in range(3):
                        winsound.Beep(1000, 500)
                        time.sleep(0.3)
                except:
                    pass
            
            import threading
            timer_thread = threading.Thread(target=timer_task)
            timer_thread.daemon = True
            timer_thread.start()
            
        except ValueError:
            self.speak("Please specify a valid number.")
    
    def set_reminder(self, reminder: str = "") -> None:
        """Set a reminder"""
        if not reminder:
            self.speak("What should I remind you about and when?")
            return
        
        reminders_file = Path("reminders.txt")
        timestamp = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")
        
        try:
            with open(reminders_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] REMINDER: {reminder}\n")
            
            self.speak(f"Reminder set: {reminder}")
            print(f"🔔 Reminder saved: {reminder}")
        except Exception as e:
            print(f"Reminder error: {e}")
            self.speak("Sorry, couldn't save reminder.")
    
    def calculate(self, expression: str = "") -> None:
        """Calculate mathematical expressions"""
        if not expression:
            self.speak("What should I calculate? Example: 'calculate 15 + 27'")
            return
        
       
        expression = expression.replace("calculate", "").replace("what is", "").strip()
        
        
        expression = expression.replace("plus", "+").replace("add", "+")
        expression = expression.replace("minus", "-").replace("subtract", "-")
        expression = expression.replace("times", "*").replace("multiply", "*")
        expression = expression.replace("divided by", "/").replace("divide", "/")
        
        try:
            
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters")
            
            result = eval(expression, {"__builtins__": {}}, {})
            
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)
            
            self.speak(f"{expression} equals {result}")
            print(f"🧮 Calculation: {expression} = {result}")
        except ZeroDivisionError:
            self.speak("Cannot divide by zero!")
        except Exception as e:
            print(f"Calculation error: {e}")
            self.speak("Sorry, I couldn't calculate that.")
    
    def tell_joke(self) -> None:
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call fake spaghetti? An impasta!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the math book look so sad? Because it had too many problems.",
            "What do you get when you cross a snowman and a vampire? Frostbite!",
            "Why did the coffee file a police report? It got mugged!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why did the bicycle fall over? Because it was two-tired!"
        ]
        
        joke = random.choice(jokes)
        self.speak(joke, speed=0.9)  
    
    def inspirational_quote(self) -> None:
        """Tell an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The harder I work, the more luck I seem to have. - Thomas Jefferson",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        ]
        
        quote = random.choice(quotes)
        self.speak(quote)
    
    def take_screenshot(self) -> None:
        """Take a screenshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            self.speak(f"Screenshot saved as {filename}")
            print(f"📸 Screenshot saved: {filename}")
            
         
            width, height = pyautogui.size()
            print(f"📱 Screen resolution: {width}x{height}")
            
        except Exception as e:
            print(f"Screenshot error: {e}")
            self.speak("Sorry, I couldn't take a screenshot.")
    
    def system_info(self) -> None:
        """Display comprehensive system information"""
        try:
            
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total = memory.total / (1024**3)
            memory_used = memory.used / (1024**3)
            memory_available = memory.available / (1024**3)
            
            
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_total = disk.total / (1024**3)
            disk_used = disk.used / (1024**3)
            disk_free = disk.free / (1024**3)
            
            
            battery = psutil.sensors_battery()
            if battery:
                battery_percent = battery.percent
                if battery.power_plugged:
                    battery_status = "plugged in and charging"
                else:
                    minutes_left = battery.secsleft // 60 if battery.secsleft > 0 else "unknown"
                    battery_status = f"{minutes_left} minutes remaining"
            else:
                battery_percent = "N/A"
                battery_status = "not available"
            
            info = f"""
            🖥️ SYSTEM INFORMATION:
            ════════════════════════════════════════
            💻 CPU: {cpu_percent}% usage, {cpu_count} cores
            🧠 RAM: {memory_percent}% used ({memory_used:.1f} GB of {memory_total:.1f} GB)
            💾 Disk: {disk_percent}% used ({disk_used:.1f} GB of {disk_total:.1f} GB)
            🔋 Battery: {battery_percent}%, {battery_status}
            ════════════════════════════════════════
            """
            
            print(info)
            self.speak(f"System status: CPU at {cpu_percent}%, RAM at {memory_percent}%, Disk at {disk_percent}%")
            
        except Exception as e:
            print(f"System info error: {e}")
            self.speak("Couldn't retrieve system information.")
    
    def get_cpu_info(self) -> None:
        """Get detailed CPU information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            print(f"💻 CPU Information:")
            print(f"   Cores: {cpu_count}")
            if cpu_freq:
                print(f"   Frequency: {cpu_freq.current:.0f} MHz (max: {cpu_freq.max:.0f} MHz)")
            
            print(f"   Usage per core:")
            for i, percent in enumerate(cpu_percent, 1):
                print(f"     Core {i}: {percent}%")
            
            avg_cpu = sum(cpu_percent) / len(cpu_percent)
            self.speak(f"CPU has {cpu_count} cores, average usage is {avg_cpu:.1f} percent")
            
        except Exception as e:
            print(f"CPU info error: {e}")
            self.speak("Couldn't get CPU information.")
    
    def get_ram_info(self) -> None:
        """Get detailed RAM information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            print(f"🧠 RAM Information:")
            print(f"   Total: {memory.total / (1024**3):.2f} GB")
            print(f"   Used: {memory.used / (1024**3):.2f} GB ({memory.percent}%)")
            print(f"   Available: {memory.available / (1024**3):.2f} GB")
            print(f"   Free: {memory.free / (1024**3):.2f} GB")
            
            if swap.total > 0:
                print(f"💾 SWAP Information:")
                print(f"   Total: {swap.total / (1024**3):.2f} GB")
                print(f"   Used: {swap.used / (1024**3):.2f} GB ({swap.percent}%)")
            
            self.speak(f"RAM usage is {memory.percent} percent")
            
        except Exception as e:
            print(f"RAM info error: {e}")
            self.speak("Couldn't get RAM information.")
    
    def get_disk_info(self) -> None:
        """Get disk information"""
        try:
            partitions = psutil.disk_partitions()
            print(f"💾 DISK Information:")
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"\n   Drive: {partition.device}")
                    print(f"   Mount: {partition.mountpoint}")
                    print(f"   Type: {partition.fstype}")
                    print(f"   Total: {usage.total / (1024**3):.2f} GB")
                    print(f"   Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
                    print(f"   Free: {usage.free / (1024**3):.2f} GB")
                except:
                    continue
            
            self.speak("Disk information displayed on screen")
            
        except Exception as e:
            print(f"Disk info error: {e}")
            self.speak("Couldn't get disk information.")
    
    def get_battery_info(self) -> None:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                print(f"🔋 BATTERY Information:")
                print(f"   Percentage: {battery.percent}%")
                print(f"   Plugged in: {'Yes' if battery.power_plugged else 'No'}")
                
                if battery.secsleft > 0:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    print(f"   Time left: {hours}h {minutes}m")
                
                self.speak(f"Battery is at {battery.percent} percent")
                if battery.power_plugged:
                    self.speak("and is charging")
                elif battery.secsleft > 0:
                    self.speak(f"with approximately {hours} hours and {minutes} minutes remaining")
            else:
                self.speak("Battery information not available")
                
        except Exception as e:
            print(f"Battery info error: {e}")
            self.speak("Couldn't get battery information.")
    
    def list_processes(self, count: str = "10") -> None:
        """List running processes"""
        try:
            num = min(int(count) if count.isdigit() else 10, 50)
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            print(f"🔄 TOP {num} PROCESSES (by CPU):")
            print(f"{'PID':>6} {'Name':<25} {'CPU%':>6} {'Mem%':>6}")
            print("-" * 45)
            
            for i, proc in enumerate(processes[:num]):
                print(f"{proc['pid']:>6} {proc['name'][:24]:<24} {proc['cpu_percent']:>6.1f} {proc['memory_percent']:>6.1f}")
            
            self.speak(f"Showing top {num} processes")
            
        except Exception as e:
            print(f"Process list error: {e}")
            self.speak("Couldn't list processes.")
    
    def translate_text(self, text: str = "") -> None:
        """Translate text (demo)"""
        if not text:
            self.speak("What would you like to translate?")
            return
        
        translations = {
            "hello": {
                "spanish": "hola",
                "french": "bonjour",
                "german": "hallo",
                "italian": "ciao",
                "japanese": "こんにちは (konnichiwa)",
                "korean": "안녕하세요 (annyeonghaseyo)"
            },
            "thank you": {
                "spanish": "gracias",
                "french": "merci",
                "german": "danke",
                "italian": "grazie",
                "japanese": "ありがとう (arigatou)",
                "korean": "감사합니다 (gamsahabnida)"
            },
            "goodbye": {
                "spanish": "adiós",
                "french": "au revoir",
                "german": "auf wiedersehen",
                "italian": "arrivederci",
                "japanese": "さようなら (sayounara)",
                "korean": "안녕히 가세요 (annyeonghi gaseyo)"
            }
        }
        
        text_lower = text.lower()
        if text_lower in translations:
            langs = translations[text_lower]
            print(f"🌍 Translations for '{text}':")
            for lang, trans in langs.items():
                print(f"   {lang.capitalize()}: {trans}")
            self.speak(f"I've shown translations for {text} on screen")
        else:
            self.speak(f"I can translate: {', '.join(translations.keys())}")
    
    def play_music(self) -> None:
        """Play music"""
        options = {
            "1": "https://open.spotify.com",
            "2": "https://music.youtube.com",
            "3": "https://soundcloud.com",
            "4": "https://www.deezer.com"
        }
        
        print("🎵 Music Players:")
        for key, url in options.items():
            print(f"   {key}. {url.split('//')[1]}")
        
        self.speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
    
    def suggest_movie(self) -> None:
        """Suggest a movie"""
        categories = {
            "action": ["John Wick", "Mad Max: Fury Road", "The Dark Knight", "Die Hard", "Terminator 2"],
            "comedy": ["The Hangover", "Superbad", "Step Brothers", "Bridesmaids", "Anchorman"],
            "sci-fi": ["Inception", "The Matrix", "Interstellar", "Blade Runner 2049", "Arrival"],
            "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "Fight Club", "Parasite"],
            "animation": ["Spirited Away", "Toy Story", "The Incredibles", "Spider-Man: Into the Spider-Verse", "Your Name"]
        }
        
        category = random.choice(list(categories.keys()))
        movie = random.choice(categories[category])
        
        self.speak(f"How about watching {movie}? It's a great {category} movie!")
        print(f"🎬 Suggested: {movie} ({category.capitalize()})")
    
    def clear_screen(self) -> None:
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"🧹 Screen cleared!")
        print(f"🤖 {self.name} Assistant ready...")
    
    def list_files(self, directory: str = ".") -> None:
        """List files in directory"""
        try:
            path = Path(directory)
            if not path.exists():
                path = Path.cwd()
            
            print(f"📁 Files in {path}:")
            print("-" * 50)
            
            
            dirs = [d for d in path.iterdir() if d.is_dir()]
            files = [f for f in path.iterdir() if f.is_file()]
            
            for d in sorted(dirs):
                print(f"📂 {d.name}/")
            
            for f in sorted(files):
                size = f.stat().st_size
                size_str = f"{size:,} bytes"
                if size > 1024**2:  # MB
                    size_str = f"{size/(1024**2):.1f} MB"
                elif size > 1024:   # KB
                    size_str = f"{size/1024:.1f} KB"
                print(f"📄 {f.name} ({size_str})")
            
            self.speak(f"Found {len(dirs)} folders and {len(files)} files")
            
        except Exception as e:
            print(f"File list error: {e}")
            self.speak("Couldn't list files.")
    
    def get_ip_address(self) -> None:
        """Get IP address information"""
        try:
            import socket
            import requests
            
            # Local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
           
            try:
                response = requests.get('https://api.ipify.org?format=json', timeout=3)
                public_ip = response.json()['ip']
            except:
                public_ip = "Not available"
            
            print(f"🌐 NETWORK Information:")
            print(f"   Hostname: {hostname}")
            print(f"   Local IP: {local_ip}")
            print(f"   Public IP: {public_ip}")
            
            self.speak(f"Your local IP address is {local_ip}")
            
        except Exception as e:
            print(f"IP error: {e}")
            self.speak("Couldn't get IP address.")
    
    def show_config(self) -> None:
        """Show current configuration"""
        print(f"⚙️ CURRENT CONFIGURATION:")
        print(f"   Assistant: {self.config.get('assistant_name', 'Jarvis')}")
        print(f"   Speech Rate: {self.config.get('speech_rate', 180)}")
        print(f"   Voice: {self.config.get('voice_gender', 'female')}")
        
        prefs = self.config.get('user_preferences', {})
        print(f"👤 USER PREFERENCES:")
        print(f"   Name: {prefs.get('name', 'User')}")
        print(f"   City: {prefs.get('city', 'New York')}")
        print(f"   Language: {prefs.get('language', 'en')}")
        
        features = self.config.get('features', {})
        print(f"🔧 FEATURES:")
        print(f"   Voice Input: {'Enabled' if features.get('voice_input', False) else 'Disabled'}")
        print(f"   Sound Effects: {'Enabled' if features.get('sound_effects', True) else 'Disabled'}")
        
        self.speak("Current configuration displayed on screen")
    
    def rename_assistant(self, new_name: str = "") -> None:
        """Rename the assistant"""
        if not new_name:
            self.speak("What would you like to call me?")
            return
        
        old_name = self.name
        self.name = new_name
        self.config['assistant_name'] = new_name
        self.save_config()
        
        self.speak(f"Hello! I'm now {new_name}. How can I help you?")
        print(f"🔄 Assistant renamed from {old_name} to {new_name}")
    
    def shutdown_assistant(self) -> None:
        """Shutdown the assistant"""
        self.speak("Shutting down. Goodbye!")
        print("🔄 Assistant shutting down...")
        raise SystemExit
    
    def restart_assistant(self) -> None:
        """Restart the assistant"""
        self.speak("Restarting... Please wait.")
        print("🔄 Restarting assistant...")
        
       
        self.save_config()
    
        os.execv(sys.executable, ['python'] + sys.argv)
    
    def show_help(self, category: str = "") -> None:
        """Show comprehensive help"""
        help_categories = {
            "basic": {
                "time": "Get current time",
                "date": "Get current date",
                "open [site]": "Open website (google, youtube, etc.)",
                "search [query]": "Search the web",
                "play [video]": "Search YouTube",
                "help": "Show this help message",
                "exit": "Exit the assistant"
            },
            "productivity": {
                "note [text]": "Take a note",
                "remind [task]": "Set a reminder",
                "timer [minutes]": "Set a timer",
                "calculate [expression]": "Calculate math",
                "screenshot": "Take screenshot",
                "files": "List files",
                "clear": "Clear screen"
            },
            "system": {
                "system": "System information",
                "cpu": "CPU details",
                "ram": "RAM details",
                "disk": "Disk information",
                "battery": "Battery status",
                "process [count]": "List running processes",
                "ip": "Network information"
            },
            "fun": {
                "joke": "Tell a joke",
                "quote": "Inspirational quote",
                "movie": "Movie suggestion",
                "music": "Play music",
                "translate [word]": "Translate words"
            },
            "config": {
                "config": "Show configuration",
                "rename [name]": "Rename assistant",
                "restart": "Restart assistant",
                "shutdown": "Shutdown assistant"
            }
        }
        
        if category in help_categories:
            print(f"\n📚 {category.upper()} COMMANDS:")
            for cmd, desc in help_categories[category].items():
                print(f"   {cmd:<25} - {desc}")
        else:
            print(f"\n{'='*60}")
            print(f"🤖 {self.name} ASSISTANT - COMMAND REFERENCE")
            print(f"{'='*60}")
            
            for category_name, commands in help_categories.items():
                print(f"\n📌 {category_name.upper()}:")
                for cmd, desc in commands.items():
                    print(f"   {cmd:<25} - {desc}")
            
            print(f"\n{'='*60}")
            print(f"💡 TIPS:")
            print(f"   • Type commands naturally (e.g., 'what time is it')")
            print(f"   • Use 'open youtube' to open websites")
            print(f"   • Say 'note' followed by your text to save notes")
            print(f"   • 'system' gives comprehensive system info")
            print(f"{'='*60}")
        
        self.speak("Help information displayed on screen. Take your time to read it.")
    
    def exit_assistant(self) -> None:
        """Exit the assistant"""
        
        user_name = self.config.get("user_preferences", {}).get("name", "User")
        
        self.speak(f"Goodbye {user_name}! Have a wonderful day!")
        print(f"\n👋 {self.name} Assistant shutting down...")
        print(f"💾 Configuration saved to {self.config_file}")
        raise SystemExit
    
    def process_command(self, command: str) -> bool:
        """Process commands intelligently"""
        if not command or command.strip() == "":
            return True
        
       
        command_lower = command.lower().strip()
        
       
        if any(exit_cmd in command_lower for exit_cmd in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
            self.exit_assistant()
            return False
        
        
        if 'help' in command_lower:
            
            for category in ['basic', 'productivity', 'system', 'fun', 'config']:
                if category in command_lower:
                    self.show_help(category)
                    return True
            self.show_help()
            return True
        
        
        natural_commands = {
            'what time': 'time',
            'current time': 'time',
            'what date': 'date',
            'today date': 'date',
            'take screenshot': 'screenshot',
            'system info': 'system',
            'cpu info': 'cpu',
            'ram info': 'ram',
            'disk info': 'disk',
            'battery info': 'battery',
            'ip address': 'ip',
            'list files': 'files',
            'clear screen': 'clear',
            'tell joke': 'joke',
            'inspire me': 'quote',
            'motivational quote': 'quote',
            'suggest movie': 'movie',
            'play music': 'music',
            'translate': 'translate',
            'calculate': 'calculate',
            'set timer': 'timer',
            'take note': 'note',
            'set reminder': 'remind',
            'open': 'open',
            'search': 'search',
            'play': 'play'
        }
        
        
        for phrase, cmd_key in natural_commands.items():
            if phrase in command_lower:
                
                arg = command_lower.replace(phrase, "").strip()
                if cmd_key in self.commands:
                    if cmd_key in ['weather']:
                        asyncio.create_task(self.commands[cmd_key](arg))
                    elif asyncio.iscoroutinefunction(self.commands[cmd_key]):
                        asyncio.create_task(self.commands[cmd_key](arg))
                    else:
                        self.commands[cmd_key](arg)
                    return True
        
        
        for cmd_key, cmd_func in self.commands.items():
            if cmd_key in command_lower:
                arg = command_lower.replace(cmd_key, "").strip()
                
                if cmd_key == 'weather':
                    asyncio.create_task(cmd_func(arg))
                elif asyncio.iscoroutinefunction(cmd_func):
                    asyncio.create_task(cmd_func(arg))
                else:
                    cmd_func(arg)
                return True
        
      
        if command_lower:
           
            user_name = self.config.get("user_preferences", {}).get("name", "User")
            
            responses = [
                f"I'm not sure how to help with '{command}'.", 
                f"Try saying 'help' to see what I can do.",
                f"I don't understand '{command}'. Maybe try a different phrase?",
                f"Sorry {user_name}, I didn't get that."
            ]
            response = random.choice(responses)
            self.speak(response)
            print(f"💡 Try: time, date, open google, search python, note 'buy milk', etc.")
        
        return True
    
    async def run(self) -> None:
        """Main async loop"""
        if not self.setup_complete:
            print("⚠️ Assistant initialized with some limitations")
        
       
        user_name = self.config.get("user_preferences", {}).get("name", "User")
        voice_enabled = "Enabled" if (self.microphone_available and 
                                     self.config.get("features", {}).get("voice_input", False)) else "Text only"
        
        
        greeting = random.choice([
            f"Hello {user_name}! I'm {self.name}, ready to assist you.",
            f"Hi {user_name}! {self.name} here. How can I help today?",
            f"Greetings {user_name}! I'm {self.name}, your personal assistant.",
            f"Good to see you {user_name}! I'm {self.name}. What can I do for you?"
        ])
        
        self.speak(greeting)
        
        print(f"\n{'='*60}")
        print(f"🚀 {self.name} ASSISTANT v2.0 - ACTIVE")
        print(f"{'='*60}")
        print(f"👤 User: {user_name}")
        print(f"🎤 Voice: {voice_enabled}")
        print(f"💡 Tip: Type 'help' to see all commands")
        print(f"💡 Say 'text mode' to type, or 'voice mode' to speak")
        print(f"👋 Say 'exit' or type 'exit' to quit")
        print(f"{'='*60}\n")
        
       
        running = True
        while running:
            try:
                
                command = await self.get_input()
                
                
                if command:
                    running = self.process_command(command)
                
                
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted by user")
                self.speak("Goodbye!")
                running = False
            except SystemExit:
                running = False
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
                await asyncio.sleep(1)
        
        print(f"\n{'='*60}")
        print(f"👋 {self.name} Assistant terminated")
        print(f"{'='*60}")

def main():
    """Main entry point"""
    print(f"{'='*60}")
    print(f"🚀 STARTING VOICE ASSISTANT")
    print(f"{'='*60}")
    print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python {sys.version}")
    print(f"{'='*60}")
    
   
    print("🔍 Checking required packages...")
    try:
        import speech_recognition
        print("✅ SpeechRecognition is installed")
    except ImportError:
        print("❌ SpeechRecognition not found!")
        print("💡 Install it with: pip install SpeechRecognition")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 is installed")
    except ImportError:
        print("❌ pyttsx3 not found!")
        print("💡 Install it with: pip install pyttsx3")
    
    try:
        import psutil
        print("✅ psutil is installed")
    except ImportError:
        print("❌ psutil not found!")
        print("💡 Install it with: pip install psutil")
    
    print(f"{'='*60}")
    
    
    assistant_name = input("Enter assistant name (default: Jarvis): ").strip()
    if not assistant_name:
        assistant_name = "Jarvis"
    
    assistant = FixedVoiceAssistant(name=assistant_name)
    
    
    try:
        asyncio.run(assistant.run())
    except KeyboardInterrupt:
        print("\n\n👋 Assistant stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 TROUBLESHOOTING:")
        print("1. Install missing packages: pip install SpeechRecognition pyttsx3 psutil pyautogui")
        print("2. Check microphone connection and permissions")
        print("3. Run as administrator if needed")
        print("4. Make sure microphone is not muted in system settings")

if __name__ == "__main__":
    main()