# Automating System Tasks with Your AI Assistant

This project provides an AI assistant that automates various tasks on your system, including:

- **File management:** Search for files, view file details, and run executables.
- **Media playback:** Play music and video files in their default media players.
- **System adjustments:** Control display brightness and volume levels.
- **Information retrieval:** Get the current date and time (using system commands).
- **Conversational interaction:** Respond to basic greetings, answer simple questions, and tell jokes.

## Key Features

- **Natural language processing:** Understands user commands spoken or typed in plain language.
- **Cross-platform compatibility:** Should work on major operating systems (potential OS-specific adjustments may be required).
- **Extensibility:** The modular design allows for adding new functionalities in the future.

## Installation

### Prerequisites:

Ensure you have Python 3 ([Download Python](https://www.python.org/downloads/)) and the following libraries installed:

- collections
- os
- re
- random
- subprocess
- screen_brightness_control  # Might require OS-specific library
- pyvolume                   # Might require OS-specific library
- speech_recognition         # Requires Google Speech-to-Text API setup ([Google Speech-to-Text API](https://cloud.google.com/speech-to-text))
- pyttsx3                    ([Pyttsx3](https://pypi.org/project/pyttsx3/))

### Clone the Repository:

```bash
git clone https://github.com/abhishekvadve/automating_system.git
````
### Install Dependencies:

Navigate to the project directory. Run `pip install -r requirements.txt` (create a requirements.txt file listing the dependencies if it doesn't exist).

## Usage

1. Run the script: `python main.py`
2. Interact with the AI assistant by speaking or typing commands.
3. Use a conversational tone, such as "Search for my presentation.ppt" or "Play some music."
4. Exit the program by saying "exit" or typing "exit".

## Example Usage

```plaintext
You: Hello!
AI Assistant: Hello! I'm your AI assistant. How can I help you today?
You: Play some music.mp3.
AI Assistant: Music file is now playing.
(Music starts playing in the default media player)
You: What is the time?
AI Assistant: (Current date and time retrieved from system commands)
You: Search for my report.docx.
AI Assistant: I found the file 'report.docx' at: C:\Users\your_username\Documents
You: Set brightness to 75%.
AI Assistant: Brightness level set to 75%.
You: Exit
AI Assistant: Goodbye! Have a great day!
```

## Contributions

We welcome contributions to enhance this project! Here are some potential areas for improvement:

- Support for additional file formats (e.g., images, documents)
- Advanced file operations (e.g., move, copy, rename)
- Integration with cloud storage services
- Multitasking and task scheduling
- Accessibility features (e.g., screen reader compatibility)

