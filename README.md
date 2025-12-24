
🤖 Voice Assistant (Jarvis)

A powerful Python-based Voice & Text Assistant that works as a personal desktop helper.
It supports voice commands, text input, system monitoring, productivity tools, and fun utilities — all in one script.

✨ Features
🗣️ Voice & Text Interaction

Voice commands using SpeechRecognition

Automatic fallback to text mode if microphone isn’t available

Switch modes anytime by saying “text mode” or “voice mode”

⏰ Productivity

Get time & date

Set timers and reminders

Take notes (saved locally)

Calculator (safe math evaluation)

Screenshots

File & directory listing

🌐 Web & Media

Open popular websites (Google, YouTube, GitHub, etc.)

Search the web

Play YouTube videos

Open music platforms (Spotify, YouTube Music, SoundCloud)

🖥️ System Information

CPU usage & per-core stats

RAM & disk usage

Battery status

Running processes

IP address (local & public)

🎉 Fun & Extras

Jokes 😂

Inspirational quotes 💡

Movie suggestions 🎬

Simple translations 🌍

⚙️ Configuration

Persistent config (assistant_config.json)

Rename the assistant anytime

Adjustable speech rate & voice

Enable/disable voice input

🛠️ Technologies Used

Python 3.8+

pyttsx3 – Text-to-Speech

SpeechRecognition – Voice input

psutil – System monitoring

pyautogui – Screenshots

aiohttp, asyncio – Async support

webbrowser – Web control

📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/fixed-voice-assistant.git
cd fixed-voice-assistant

2️⃣ Install Required Packages
pip install SpeechRecognition pyttsx3 psutil pyautogui aiohttp requests


💡 Windows users:
You may also need:

pip install pypiwin32

▶️ How to Run
python main.py


You’ll be asked to enter an assistant name (default is Jarvis).

🧠 Example Commands
Command	Description
time	Get current time
date	Get today’s date
open youtube	Open YouTube
search python asyncio	Google search
note buy milk	Save a note
timer 10 minutes	Set a timer
calculate 15 * 7	Math calculation
system	Full system info
cpu	CPU details
ram	Memory usage
screenshot	Take screenshot
joke	Hear a joke
quote	Inspirational quote
help	Show all commands
exit	Quit assistant
🎤 Voice Commands

Speak naturally:

“What time is it?”
“Open Google”
“Set a timer for 5 minutes”

Say “text mode” to type

Say “voice mode” to talk again

📁 Generated Files

assistant_config.json → Stores preferences

notes.txt → Saved notes

reminders.txt → Saved reminders

screenshot_YYYYMMDD_HHMMSS.png → Screenshots

⚠️ Troubleshooting
Microphone Not Working?

Check system microphone permissions

Make sure mic isn’t muted

Try running the script as Administrator

Install PyAudio (optional but recommended)

Missing Packages?
pip install --upgrade pip
pip install SpeechRecognition pyttsx3 psutil pyautogui

🚀 Future Improvements (Ideas)

Real weather API integration

Offline speech recognition

GUI interface

Task scheduler for reminders

Plugin system
