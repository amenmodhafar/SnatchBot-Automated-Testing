# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Arguments for the voice paths
emptyUtterance = '/Users/apple/Documents/GitHub/SnatchBot/res/empty.wav'
nameUtterance = '/Users/apple/Documents/GitHub/SnatchBot/res/john_smith.wav'
explainUtterance = '/Users/apple/Documents/GitHub/SnatchBot/res/explain_chatbox.wav'

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")
chrome_options.binary_location = "/usr/bin/chromium"

def print_hi(name):
    # Hello world
    print(f'Hi, {name}')
if __name__ == '__main__':
    print_hi('SnatchBot')

# Test Case #1: Snatchbot conversation_Explain_Snatchbot

# Test case assumes:
# 1. microphone access has been given
# 2. Not handling multiple tabs open with snatchbot for the first iteration

# Test case procedure:
# 1. Accessing the snatchbot site.
# Expected: site launches successfully


driver = webdriver.Chrome()
driver.get("https://snatchbot.me/")
assert "Snatch" in driver.title

# 1. Waiting for the sntch_button to become available to access the snatchbot button.
# Expected: The snatch bot dialog popups
try:
    chatbot = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "sntch_button"))
    )
    chatbot.click()
    print("chatbot opened")

except TimeoutException as e:
    print("chatbot failed to open")


# 2. Snatchbot asks for a name. Wait for the microphone button to be available then click it

try:

    # This is where the expcetion is happenning in accessing chat audio button. these are the different things I've tried, among others
    #  EC._find_elements((By.CSS_SELECTOR,".mat-mini-fab"))
    # EC.presence_of_element_located((By.XPATH, "//app-audio-recorder[@id='sendAudioRec']/div/button"))
    # driver.find_element_by_class_name("chat__audio")
    # driver.find_element(By.CLASS_NAME, "chat__audio")
    # driver.find_element((By.CSS_SELECTOR, ".mat-mini-fab"))
    utter_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.CLASS_NAME,"chat__audio")

    )
    utter_name.click()
    # Enters the name from the .wave file saved in the assets
    chrome_options.add_argument("--use-file-for-fake-audio-capture={0}".format(nameUtterance))
    print("name entered")

except TimeoutException as e:
    print("name failed to enter")

# Results: assert that the answer the chatbot gives contains the name
# A better design would iterate instead of having hardcoded indices for the messages
try:
    assert ("john smith") in driver.find_element_by_css_selector(
        '.message:nth-child(4) .angular-with-newlines')
    print("Name processing - pass")

except AssertionError as e:
    print("Name processing - failed")

#class="messages ng-star-inserted"
#test="chat-messages"

# 3. Wait for the microphone button to be available again, then click it
try:

    enter_text = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(By.CLASS_NAME,"chat__audio")

    )
    enter_text.click()

    # Enter the utterance "Explain chatbots" via .wav file
    chrome_options.add_argument("--use-file-for-fake-audio-capture={0}".format(explainUtterance))
    print("Explain Utterance recorded")

except TimeoutException as e:
    print("Explain Utterance to record")

# Result: confirm the bot answer contains the following chatbot exaplanation:
# "Basically, we chatbots are just software applications, like any other application you use on your computer. " \
# "The important difference is that people interface with us using conversation. Shall I say more about this?"

try:
    assert("Basically, we chatbots are just software applications, like any other application you use on your computer. "
           "The important difference is that people interface with us using conversation. Shall I say more about this?") in driver.find_element_by_css_selector('.message:nth-child(8) .angular-with-newlines')
    print("Explain chatbot - pass")

except AssertionError as e:
    print("Explain chatbot - fail")

# Exploratory testing
# Using the text chat-input target to continue testing

#driver.close()

