import os
from collections import deque
import re
import random
import subprocess
import screen_brightness_control as sbc
import pyvolume
import speech_recognition as sr
import pyttsx3

def speak(text, voice_id=None):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if voice_id is not None:
        engine.setProperty('voice', voice_id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            print("Sorry, I couldn't reach the Google API.")
        except Exception as e:
            print(f"An error occurred: {e}")
    return ""


def search_file(filename):
    """
    Search for a file in the entire system.
    Returns the absolute path of the file if found, otherwise returns None.
    """
    root_directories = [f"{drive}:\\" for drive in 'CDE' if os.path.exists(f"{drive}:\\")]
    directories_to_search = deque(root_directories)
    searched_locations = []

    while directories_to_search:
        current_dir = directories_to_search.popleft()
        searched_locations.append(current_dir)
        try:
            for item in os.listdir(current_dir):
                full_path = os.path.join(current_dir, item)
                if os.path.isdir(full_path):
                    directories_to_search.append(full_path)
                elif os.path.isfile(full_path) and item == filename:
                    return full_path, searched_locations
        except PermissionError:
            pass

    return None, searched_locations

def get_file_details(file_path):
    """
    Get details about the file.
    If the file is a Python script, read and provide details about the script.
    If the file is a text file, provide details about its content.
    """
    if os.path.isfile(file_path):
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.py':
            try:
                with open(file_path, 'r') as file:
                    script_content = file.read()
                num_lines = script_content.count('\n') + 1
                num_words = len(script_content.split())
                details = (
                    f"Python Script Details:\n"
                    f"File Path: {file_path}\n"
                    f"Number of Lines: {num_lines}\n"
                    f"Number of Words: {num_words}\n"
                    f"Script Content:\n{script_content}"
                )
                return details
            except Exception as e:
                return f"Error reading Python script: {e}"

        elif file_extension == '.txt':
            try:
                with open(file_path, 'r') as file:
                    text_content = file.read()
                num_lines = text_content.count('\n') + 1
                num_words = len(text_content.split())
                details = (
                    f"Text File Details:\n"
                    f"File Path: {file_path}\n"
                    f"Number of Lines: {num_lines}\n"
                    f"Number of Words: {num_words}\n"
                    f"Text Content:\n{text_content}"
                )
                return details
            except Exception as e:
                return f"Error reading text file: {e}"

        else:
            try:
                file_size = os.path.getsize(file_path)
                details = (
                    f"File Details:\n"
                    f"File Path: {file_path}\n"
                    f"File Size: {file_size / 1024 / 1024:.2f} MB\n"

                )
                if file_extension in ['.jpg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.svg', '.webp', '.eps', '.ai', '.psd', '.raw']:
                    details += f"\nFile Type: Image"
                elif file_extension in ['.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a', '.aiff', '.ape', '.mpc', '.wv', '.opus', '.amr', '.pcm']:
                    details += f"\nFile Type: Audio"
                elif file_extension in ['.avi', '.mp4', '.mov', '.wmv', '.flv', '.mkv']:
                    details += f"\nFile Type: Video"
                elif file_extension in ['.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.jar']:
                    details += f"\nFile Type: Archive"
                elif file_extension in ['.json', '.xml', '.html', '.css', '.js', '.php', '.java', '.cpp', '.h', '.cs', '.rb', '.pl', '.sh', '.bat', '.ps1', '.cmd']:
                    details += f"\nFile Type: Code"
                elif file_extension in ['.csv', '.tsv', '.dat', '.log', '.sql', '.db', '.dbf', '.mdb', '.accdb', '.sqlite', '.db', '.db3', '.bak', '.tmp', '.temp']:
                    details += f"\nFile Type: Database"
                elif file_extension in ['.cfg', '.ini', '.conf', '.yaml', '.yml', '.json', '.toml']:
                    details += f"\nFile Type: Configuration"
                elif file_extension in ['.md', '.rst', '.tex', '.rtf', '.odt', '.ott', '.ods', '.ots', '.odp', '.otp', '.odg', '.otg', '.odf', '.odb', '.odc', '.odf', '.odi', '.odm', '.ott', '.otp', '.otg', '.otc', '.otf', '.otn', '.odp', '.otp', '.ots', '.otg', '.otc', '.otf', '.otn', '.otl', '.oth']:
                    details += f"\nFile Type: Document"
                return details
            except Exception as e:
                return f"Error getting file details: {e}"

    else:
        return "Invalid file path."

# def extract_filename(command, previous_command=None):
#     """
#     Extracts the filename from the command.
#     Identifies potential filenames based on common file extensions and patterns.
#     """
#     # Common file extensions
#     file_extensions = ['.txt', '.py', '.doc', '.docx', '.pdf', '.jpg', '.png', '.xls', '.xlsx', '.ppt', '.pptx', '.exe', '.mp4', '.mp3', '.wav', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.jar', '.json', '.xml', '.html', '.css', '.js', '.php', '.java', '.cpp', '.h', '.cs', '.rb', '.pl', '.sh', '.bat', '.ps1', '.cmd', '.csv', '.tsv', '.dat', '.log', '.sql', '.db', '.dbf', '.mdb', '.accdb', '.sqlite', '.db', '.db3', '.bak', '.tmp', '.temp', '.cfg', '.ini', '.conf', '.yaml', '.yml', '.json', '.toml', '.md', '.rst', '.tex', '.rtf', '.odt', '.ott', '.ods', '.ots', '.odp', '.otp', '.odg', '.otg', '.odf', '.odb', '.odc', '.odf', '.odi', '.odm', '.ott', '.otp', '.otg', '.otc', '.otf', '.otn', '.odp', '.otp', '.ots', '.otg', '.otc', '.otf', '.otn', '.otl', '.oth', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.jpg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.svg', '.webp', '.eps', '.ai', '.psd', '.raw', '.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a', '.aiff', '.ape', '.mpc', '.wv', '.opus', '.amr', '.pcm', '.avi', '.mp4', '.mkv', '.flv', '.wmv', '.mov', '.webm', '.vob', '.3gp', '.3g2', '.m4v', '.mpg', '.mpeg', '.m2v', '.m4p', '.m2p', '.m2ts', '.ts', '.divx', '.xvid', '.rm', '.rmvb']
#     pattern = re.compile(r'\b\w+(' + '|'.join(re.escape(ext) for ext in file_extensions) + r')\b')
#     match = pattern.search(command)
#     if match:
#         return match.group(0)
#     else:
#         if previous_command:
#             previous_filename = extract_filename(previous_command)
#             if previous_filename:
#                 # Check if the command contains reference to the previous filename using pronouns
#                 pronouns = ['it', 'that']
#                 for pronoun in pronouns:
#                     if pronoun in command and previous_filename:
#                         return previous_filename
#         return None

def extract_filename(command, previous_command=None):
    """
    Extracts the filename from the command.
    Identifies potential filenames based on common file extensions and patterns.
    """
    # Common file extensions
    file_extensions = ['.txt', 'lnk', '.py', '.doc', '.docx', '.pdf', '.jpg', '.png', '.xls', '.xlsx', '.ppt', '.pptx', '.exe', '.mp4', '.mp3', '.wav', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.jar', '.json', '.xml', '.html', '.css', '.js', '.php', '.java', '.cpp', '.h', '.cs', '.rb', '.pl', '.sh', '.bat', '.ps1', '.cmd', '.csv', '.tsv', '.dat', '.log', '.sql', '.db', '.dbf', '.mdb', '.accdb', '.sqlite', '.db', '.db3', '.bak', '.tmp', '.temp', '.cfg', '.ini', '.conf', '.yaml', '.yml', '.json', '.toml', '.md', '.rst', '.tex', '.rtf', '.odt', '.ott', '.ods', '.ots', '.odp', '.otp', '.odg', '.otg', '.odf', '.odb', '.odc', '.odf', '.odi', '.odm', '.ott', '.otp', '.otg', '.otc', '.otf', '.otn', '.odp', '.otp', '.ots', '.otg', '.otc', '.otf', '.otn', '.otl', '.oth', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.jpg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.ico', '.svg', '.webp', '.eps', '.ai', '.psd', '.raw', '.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a', '.aiff', '.ape', '.mpc', '.wv', '.opus', '.amr', '.pcm', '.avi', '.mp4', '.mkv', '.flv', '.wmv', '.mov', '.webm', '.vob', '.3gp', '.3g2', '.m4v', '.mpg', '.mpeg', '.m2v', '.m4p', '.m2p', '.m2ts', '.ts', '.divx', '.xvid', '.rm', '.rmvb']
    pattern = re.compile(r'\b\w+(' + '|'.join(re.escape(ext) for ext in file_extensions) + r')\b')
    match = pattern.search(command)
    if match:
        return match.group(0)
    else:
        words = command.split()
        if len(words) > 1 and words[0] == 'play':
            return words[1]
        if previous_command:
            previous_filename = extract_filename(previous_command)
            if previous_filename:
                # Check if the command contains reference to the previous filename using pronouns
                pronouns = ['it', 'that']
                for pronoun in pronouns:
                    if pronoun in command and previous_filename:
                        return previous_filename
    return None


def process_command(command):
    """
    Process a single command.
    """
    command = command.strip().lower()
    filename = extract_filename(command)
    # if not filename:
        # return "I'm sorry, I couldn't identify a filename in your command. Please specify a valid

    if "search" in command:
        file_path, searched_locations = search_file(filename)
        if file_path:
            return f"I found the file '{filename}' at: {file_path}"
        else:
            searched_locs = "\n".join(searched_locations)
            if searched_locs > 50:
                searched_locs = searched_locs[:50] + "..."
            return f"Sorry, I couldn't find the file '{filename}'. Here are the locations I searched:\n{searched_locs}"
    elif "where" in command:
        file_path, _ = search_file(filename)
        if file_path:
            return f"I found the file '{filename}' at: {file_path}"
        else:
            return f"Sorry, I couldn't find the file '{filename}'."
    elif "what" in command:
        file_path, _ = search_file(filename)
        if file_path:
            return get_file_details(file_path)
        else:
            return "Sorry, I couldn't find the file."
    elif "brightness" in command:
        level = int(re.search(r'\d+', command).group())
        set_brightness(level)
        return f"Brightness level set to {level}%."
    elif "volume" in command:
        level = int(re.search(r'\d+', command).group())
        set_volume(level)
        return f"Volume level set to {level}%."
    elif ".exe" in command:
        file_path, _ = search_file(filename)
        if file_path:
            return run_executable(file_path)
        else:
            return "Sorry, I couldn't find the executable file."
    # elif "play" and ".mp4" or ".avi" or ".mov" or ".wmv" or ".flv" or ".mkv" in command:
    #     print("In play with extension - 11")
    #     return play_video(filename)
    # elif "play" and ".mp3" or ".wav" or ".wma" or ".aac" or ".flac" or ".ogg" or ".m4a" or ".aiff" or ".ape" or ".mpc" or ".wv" or ".opus" or ".amr" or ".pcm" in command:
    #     print("In play with extension - 12")
    #     return play_music(filename)
    # elif "play" in command:
    #     print("In play with no extension")
    #     extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a', '.aiff', '.ape', '.mpc', '.wv', '.opus', '.amr', '.pcm']
    #     for ext in extensions:
    #         print("In play with no extension - 1")
    #         file_path, _ = search_file(filename + ext)
    #         if file_path:
    #             print("In play with no extension - 2")

    #             if ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']:
    #                 print("In play with no extension - 3")

    #                 return play_video(filename + ext)
    #             else:
    #                 print("In play with no extension - 4")

    #                 return play_music(filename + ext)
    #     return "Sorry, I couldn't find the media file."
    elif "play" in command:
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
        audio_extensions = ['.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a', '.aiff', '.ape', '.mpc', '.wv', '.opus', '.amr', '.pcm']
        
        if any(ext in command for ext in video_extensions):
            return play_video(filename)
        elif any(ext in command for ext in audio_extensions):
            return play_music(filename)
        else:
            extensions = video_extensions + audio_extensions
            for ext in extensions:
                found_files, _ = search_file(filename + ext)
                if found_files:
                    if ext in video_extensions:
                        return play_video(filename + ext)
                    else:
                        return play_music(filename + ext)
            return "Sorry, I couldn't find the media file."
    elif command == "exit":
        return "Goodbye! Have a great day!"
    else:
        return gossips(command)
# Run executable files 
def run_executable(command):
    """
    Run an executable file.
    """
    try:
        subprocess.run(command, shell=True)
        return "Executable file executed successfully."
    except Exception as e:
        return f"Error executing file: {e}"
    

# Play video files
def play_video(command):
    """
    Play a video file.
    """
    try:
        file_path, _ = search_file(command)
        if file_path:
            subprocess.run(f'start {file_path}', shell=True)
            return "Video file is now playing."
        else:
            return "Sorry, I couldn't find the video file."
    except Exception as e:
        return f"Error playing video: {e}"
    
    
# Play music files
def play_music(command):
    """
    Play a music file.
    """
    try:
        file_path, _ = search_file(command)
        if file_path:
            subprocess.run(f'start {file_path}', shell=True)
            return "Music file is now playing."
        else:
            return "Sorry, I couldn't find the music file."
    except Exception as e:
        return f"Error playing music: {e}"

def set_brightness(level):
    # get current brightness value
    print(sbc.get_brightness())
    
    #set brightness to 50%
    sbc.set_brightness(level)
    
    print(sbc.get_brightness())
    
    #set the brightness of the primary display to 75%
    sbc.set_brightness(level, display=0)
    
    print(sbc.get_brightness())

def set_volume(level):
    pyvolume.custom(level)

def gossips(command):
    if "hi" in command:
        return "Hello! How can I help you today?"
    elif "how are you" in command:
        return "I'm a computer program, so I don't have feelings, but I'm here to help you!"
    elif "your name" in command:
        return "I'm an AI assistant. You can call me Jarvis!"
    elif "who are you" in command:
        return "I'm an AI assistant. You can call me Jarvis!"
    elif "what can you do" in command:
        return "I can help you find files, run executables, play media files, and more!"
    elif "what is your purpose" in command:
        return "My purpose is to assist you with your tasks and provide information."
    elif "what time is it" in command:
        return subprocess.run('time /t', shell=True)
    elif "what day is it" in command:
        return subprocess.run('date /t', shell=True)
    elif "what is the weather" in command:
        return "I'm sorry, I don't have access to the internet to check the weather."
    elif "tell me a joke" in command:
        jokes = [
            "Why do we tell actors to 'break a leg'? Because every play has a cast.",
            "I told my wife she should embrace her mistakes. She gave me a hug.",
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "I used to play piano by ear, but now I use my hands.",
            "I'm terrified of elevators, so I'm going to start taking steps to avoid them.",
            "I used to be a baker, but I couldn't make enough dough.",
            "I'm reading a book on the history of glue. I just can't seem to put it down!"
        ]
        return random.choice(jokes)
    else:
        return "I'm not sure I understand. Please ask me something else."

def process_multiple_commands(commands):
    """
    Process multiple commands in a single input line.
    """
    responses = []
    for command in commands.split(' and '):
        responses.append(process_command(command))
    return '\n'.join(responses)

# def main():
#     print("Hello! I'm your AI assistant. How can I help you today?")
#     while True:
#         user_input = input("\nYou: ")
#         response = process_multiple_commands(user_input)
#         print("\nAI Assistant:", response)
#         if "exit" in user_input.lower():
#             break

def main():
    speak("Hello! I'm your AI assistant. How can I help you today?")
    while True:
        command = listen()
        response = process_command(command)
        print("\nAI Assistant:", response)
        speak(response)
        if "exit" in command.lower():
            break



if __name__ == "__main__":
    main()


