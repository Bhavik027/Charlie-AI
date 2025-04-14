from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time  # Import the time module

env_vars = dotenv_values(".env")

InputLanguage = env_vars.get("InputLanguage")

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

os.makedirs(r"Data", exist_ok=True)
with open(r"Data/Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()

Link = f"file:///{current_dir}/Data/Voice.html"

chrome_options = Options()

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.42 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirPath = rf"{current_dir}/Frontend/Files"
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how ", "what ", "who ", "where ", "when ", "why ", "which ", "whose ", "whom ", "can you ", "what's ", "where's ", "how's "]

    is_question = any(word in new_query for word in question_words)

    if is_question:
        if query_words and query_words[-1].endswith(('.', '?', '!')):
            new_query = new_query[:-1] + "?"
        elif query_words:
            new_query += "?"
    else:
        if query_words and query_words[-1].endswith(('.', '?', '!')):
            new_query = new_query[:-1] + "."
        elif query_words:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        print(f"Translation error: {e}")
        return Text.capitalize() # Return original text if translation fails

def SpeechRecognition():
    driver.get(Link)

    start_button = driver.find_element(by=By.ID, value="start")
    start_button.click()

    output_element = driver.find_element(by=By.ID, value="output")

    while True:
        try:
            Text = output_element.text
            if Text:
                end_button = driver.find_element(by=By.ID, value="end")
                end_button.click()

                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
            time.sleep(0.1)  # Add a small delay to avoid busy-waiting
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            time.sleep(1) # Wait a bit before retrying

if __name__ == "__main__":
    try:
        while True:
            Text = SpeechRecognition()
            print(Text)
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()