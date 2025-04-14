# required libraries
#Import functtions to open and close apps.
from AppOpener import close, open as appopen
from webbrowser import open as webopen     # Import web browser functionality.
from pywhatkit import search, playonyt   # Import search functionality and play video functionality from pywhatkit.
from dotenv import dotenv_values      # Import dotenv library to load environment variables.
from bs4 import BeautifulSoup      # Import BeautifulSoup library to parse HTML and XML documents.
from rich import print            # Import print function from rich library to print text in a rich format.
from groq import Groq           # Import Groq library to interact with Notion API.
import webbrowser         # Import webbrowser library to open web pages.
import subprocess       # Import subprocess library to run shell commands.
import requests      # Import requests library to make HTTP requests.
import keyboard   # Import keyboard library to simulate keyboard events.
import asyncio   # Import asyncio library to run asynchronous tasks.
import os # Import os library to interact with the operating system.
import typing


# load environment variables from the .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Defone css classes for parsing specific elements in html content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw_Data_text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d","webanswers-webanswers_table__webanswers-tables", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web request.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else i can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role":"system","content":f"Hello, I am {os.environ['Username']},You're a content writer. you have to write content like letters, codes, applications, essays, notes, songs, poem etc."}]

# Function to perform Google search.
def GoogleSearch(Topic):
    search(Topic)  # Perform a Google search on the topic.
    return True   # Return True to indicate a successful search.

# Function to generate content using AI and save it to a file.
def Content(Topic):
  
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor  = 'notepad.exe' # Default text editor.
        subprocess.Popen([default_text_editor, File]) # Open the file in Notepad.
        
    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content":f"{prompt}"}) # Add the user's prompt to messages.
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Specify the AI Model.
            messages=SystemChatBot + messages, # Include the system instruction and chat history.
            max_tokens=2048, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, # use nucleus sampling for response diversity.
            stream=True, # Enable streaming response.
            stop=None # Allow the model to determine stopping conditions.
        )
        
        Answer = "" # Initialize an empty string for the response.
        
        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content: # Check if the chunk contains content.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.
                
        Answer = Answer.replace("</s", "")  # Remove "Content" from the topic.
        messages.append({"role":"assistent", "content":Answer})  # Add the AI response to the messages.
        return Answer
    
    Topic: str = Topic.replace("Content ", "") # Remove "Content " from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.
    
    
    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()
        
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")  # Open the file in Notepad.
    return True #Indicate success.

# Function to search for a topic on youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the youtube search URL.
    webbrowser.open(Url4Search)  # Open the search URL in a web browser.
    return True  # Indicate Success.

# Fuction to Play a video on youtube.
def PlayYoutube(query):
    playonyt(query)  # Use pywhat's kit playonyt fuction to play the video.
    return True # Indicate Success.  

# Function to open an application or a relavent webpage.
def OpenApp(app, sess=requests.session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    
    except Exception as e:
        print("error while opening app")

        try:
            query = f"{app}"
            url = f"https://www.{query}.com"

            webbrowser.open(url)
            return True
        except Exception as e:
            print("error while opening websites")
            return False
              


    #def find_url_by_name(name)
#  Function to close an application.
def CloseApp(app):
    
    if "chrome" in app:
        pass # Skip if the app is chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.

# Function to execute the system level commands.
def System(command):
    
    # Nested fuction to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
        
    # Nested fuction to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute") # Simulate the unmute key press.
        
    # Nested fuction to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the volume up key press.
        
    # Nested fuction to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.
        
        
    # Execute the Appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume_up":
        volume_up()
    elif command == "volume_down":
        volume_down()
        
    return True # Indicate Success.

# Asynchronous fuction to translate and execute user commands.
async def TranslateAndExecute(command: list[str]):
    
    funcs = [] # List to store asynchronous tasks.
    
    for command in command:
        
        if command.startswith("open "):  # Handle "open" command.
            
            if "open it" in command:   # Ignore "Open it" commands.
                pass
            
            if "open file"== command: # Ignore the "open file" command.
                pass
            
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)
            
        elif command.startswith("general "):  # Placeholder for general  commands.
            pass
        
        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass
        
        elif command.startswith("close "):  # Handle close commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)
            
        elif command.startswith("play "):  # Handle "Play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))  # Schedule YouTube  playback.
            funcs.append(fun)
            
        elif command.startswith("content "):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
            funcs.append(fun)
            
        elif command.startswith("google search "):  # Handle "google search" commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search.
            funcs.append(fun)
            
        elif command.startswith("youtube search "):  # Handle "youtube search" commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)
            
        elif command.startswith("system "):  # Handle "system" commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system commands.
            funcs.append(fun)
            
        else:
            print(f"No Function Found for {command}") # Print message if no function is found.
            
    result = await asyncio.gather(*funcs)  # Execute all tasks concurrently.
    
    for result in result: # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result
            
            
# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):   # Translate and execute commands.
        pass
    
    return True # Return True to indicate successful execution.

if __name__ == "__main__":
    asyncio.run(Automation([""]))