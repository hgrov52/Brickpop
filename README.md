# Brickpop

REQUIREMENTS: (last two obtaibable by downloading pip then in command prompt type "pip install ____")

Python27

pyautogui

PIL

HOW TO RUN:

Open facebook to the game "Brickpop"

Maximize the window

Calibration has not been built into the program yet, so uncomment the #im.show line before it resizes the image and adjust the image coordinates accordingly. Remember to change the numbers in the automate() function as well. Change until the image boarder is at the very edge of the blocks. Practice left works consistently right now, however facebook left (the real game but the window on theleft half of the computer screen) only works sometimes. This is why I recommend using facebook (the real game on a maximized window). Uncomment only one im=_____ under the correct comment.

Always wait for the bricks to settle before running the program. 

Run Brickpop.py

If the error "Something went wrong" happens, it prevented a desynchronization of the program and the real game happening live. Should this happen to you, run the Brickpop_backup_3.py on the remaining bricks on the board. The board should not be full if you get this error. You will have to transfer your image coordinates from the calibration you did before, as well as uncommnet the right line for the image grab and make sure box_l in automate is being assigned to the right window and game configuration, either practice, practice game on the left half of the screen, the real game, or the real game on the left half of the screen.

When that game finishes, run Brickpop.py again unless you wish to play each board at a time, in which case continue running the backup_3.





