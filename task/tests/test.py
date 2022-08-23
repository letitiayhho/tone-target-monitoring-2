from psychopy import core, visual, event

win = visual.Window(
    size=[400, 400],
    units="pix",
    fullscr=False
)

block_begin = visual.TextStim(win, 
                              text = "How many times did you hear the target",
                              pos=(0.0, 0.0),
                              color=(1, 1, 1), 
                              colorSpace='rgb')
block_begin.draw()
win.flip()
event.waitKeys()
win.flip()
core.wait(1)

keyList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'backspace']
response = []
response_text = ''

while True:
    keys = event.getKeys(keyList = keyList)
    if response_text and 'return' in keys: # empty response not accepted
        break
    elif keys:
        if 'return' in keys:
            None
        elif 'backspace' in keys:
            response = response[:-1]
        else:
            response.append(keys)
        response_text = ''.join([item for sublist in response for item in sublist])
        win.flip()
        print(response_text)
        show_response = visual.TextStim(win,
                                       text = response_text,
                                       pos=(0.0, 0.0),
                                       color=(1, 1, 1), 
                                       colorSpace='rgb')
        show_response.draw()
        win.flip()

print('Response was:')
print(int(response_text))

# win.close()

# from cgitb import reset
# from re import M
# from tracemalloc import stop
# from psychopy import prefs
# from psychopy.hardware.keyboard import Keyboard 
# from psychopy.gui import DlgFromDict
# from psychopy import visual, core

# from psychopy import prefs
# prefs.hardware['audioLib'] = ['ptb']
# from psychopy.sound.backend_ptb import SoundPTB as Sound
# from psychtoolbox import GetSecs, WaitSecs
# from events import EventMarker
# from psychopy import visual, core

# import string

# KB = Keyboard()
# KB.clearEvents()

# WIN = visual.Window([800,600], monitor="testMonitor", units="deg")
# text = "How many times did you hear the target tone? \
#         \
#         "
# ask_response = visual.TextStim(WIN, 
#                   text = text,
#                   pos=(0.0, 0.0),
#                   color=(1, 1, 1), 
#                   colorSpace='rgb')
# ask_response.draw()
# WIN.flip()


# #     while True:
# #         keys = KB.getKeys()
# #         if 'return' in keys: 
# #             WIN.flip()
# #             break
# # Get response
# numbers = list(string.digits)
# response = []
# while True:
#     keys = KB.getKeys()
#     if 'return' in keys:
#         break
#     elif keys:
#         response.append(keys)
#         print(response)
        
# for key in keys:
#     print(key.name, key.rt, key.duration)
        
        
# WIN.flip()
# WaitSecs(0.5)
# core.quit()
# #     print(keys)
# #     if 'escape' in keys:
# #         core.quit()  # So you can quit
# #     else:
# #     if keys[0]:
# #         print(keys)
# #     if 'backspace' in keys:
# #         response = response[:-1]  # Deletes
# #     elif numbers in keys:
# #         print(keys)
# #         response += keys  # Adds character to text if a number
# #         setText(response)  # Set new text on screen
# #     elif 'enter' in keys:
# #         break
# # print(response)
# # response = int(response)
# # print(response)


# #     block_begin = visual.TextStim(WIN, 
# #                                   text = "Please count how many times you hear the target tone. Press 'enter' to begin!",
# #                                   pos=(0.0, 0.0),
# #                                   color=(1, 1, 1), 
# #                                   colorSpace='rgb')
# #     block_begin.draw()
# #     WIN.flip()
    
# #     while True:
# #         keys = KB.getKeys()
# #         if 'return' in keys: 
# #             WIN.flip()
# #             break