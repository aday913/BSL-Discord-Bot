# goal of automaticUpdate: Using the datetime and pyautogui libraries,
#  automate the process of running the BSL discord bot "bot.py" in a 
#  raspberry pi command line terminal while also checking for updates
#  to the git repository at a specific time every day

import pyautogui
import datetime
import time

# when we initially run the file, let's give me a few seconds to click into
# the correct terminal window
time.sleep(10)

#boolean variable used to determine whether an update has already been ran
alreadyRan = False

def stopBot():
    '''
    Function stops the bot.py file by pressing ctrl+c in the terminal window
    '''
    # assuming the bot.py script is already running, we first need to stop it
    print('Stopping the bot')
    pyautogui.keyDown('ctrlleft')
    pyautogui.press('c')
    pyautogui.keyUp('ctrlleft')

    # let the bot finish stopping before we try to pull from the repo:
    print('Waiting for the bot to complete stopping...')
    time.sleep(10)
    return

def pullRepo():
    '''
    Function runs "git pull" in the terminal window to update the BSL Discord
    bot so that we always have up-to-date functionality
    '''
    print('Running git pull')
    pyautogui.typewrite('git pull')
    pyautogui.press('enter')

    # We need to wait for the pull to be complete before continuing:
    time.sleep(30)
    return

def runBot():
    '''
    Function runs "python3 bot.py" in the terminal window to run the bot
    '''
    print('Bringing bot back online...')
    pyautogui.typewrite('python3 src/bot.py')
    pyautogui.press('enter')
    return

def autoUpdate(updateHour=4, updateMinute=0):
    '''
    Function runs continuously to see if the time is right for an update!
    '''
    now = datetime.datetime.now()
    correctHour = (now.hour == updateHour)
    correctMinute = (now.minute == updateMinute)
    alreadyRan = None
    if correctHour and correctMinute and not alreadyRan:
        # If the time is right and we haven't already ran an update, then
        # we stop the bot and pull from the repo
        alreadyRan = True
        stopBot()
        pullRepo()
        runBot()
    elif not correctHour and not correctMinute:
        # Once the update has been ran, we reset alreadyRan to False
        alreadyRan = False


if __name__ == '__main__':
    print('Running automaticUpdate.py as main')
    while True:
        autoUpdate()