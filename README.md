# Wordament_Solver
This is a coding project that I was most happy with - building a solver that could search for possible words in the Microsoft Wordament game.
Disclaimer: Of course, do not use such code to cheat in multi-player. My code is designed to work in single-player, and the motivation for this (in addition to the joy of learning to code) is to find those last few pesky 'common words' that Wordament says that I have yet to find...

## Coding Concepts
The following ideas and approaches were adopted:-
- Read in a word list (I tried various dictionaries found online and ultimately settled on using a Scrabble word list)
- Prep a set of 'valid' truncated words from the word list (this is used later to decide to stop 'pathing', e.g. say the code finds a path with letters in the sequence 'XYZ', there is no point pathing further since there are no words that start with 'XYZ')
- Define a bunch of functions to help with pathing (given any starting point in the grid, go left/right/up/down/etc to as yet unused tiles to form letter sequences and test if they might be valid words)
- Get user to manually input the letters left to right, top row to bottom row, in space delimited manner
- Detect the presence of special tiles (prefix, suffix, either/or, digram, corners)
- Seek user input on whether user wants to search for words using special tiles only, or search for words of specific length, or search for all words
- Run the pathing based on user's selection, taking note of special tiles (e.g. prefix tiles can only be pathed from but cannot be pathed to, either/or tiles will require two runs, etc)
- Finally, output the words found to the terminal

## OCR
After I got the above working, I proceeded to code in some OCR to detect the tile grid automatically:-
- Used the pyautogui library to take screenshots, cv2 and numpy to assist with image processing, and pytessaract for OCR
- For convenience, I used pyautogui to search for the hint button as a way to detect if the Wordament game is on-screen
- From there a snapshot is taken of the tile grid (pixel coordinates are coded for 1920 by 1080 screen resolution)
- The tile grid is then 'chopped up' to obtain the 16 tiles, then some image pre-processing is applied before attempting OCR
- From my tests, I was unable to properly detect the letters P, I and R, so some hardcoded correction was needed
- Thereafter, the OCR detected grid is printed for the user to review before proceeding with the rest of the solver code

## OCR Part 2
After I decided that I have achieved sufficiently good results with using OCR to detect the tile grid, I moved on to:-
- Chop up the tile grid to obtain and detect the scores for each tile
- Detect the 3 tasks required to complete the puzzle with maximum 3 stars
- List out the optimum shortest set of words to complete the puzzle

## Notes
As usual, I am not the first to attempt this coding project and there is always room for improvement. Options include optimising the algorithm for pathing and searching for valid words, improving on the OCR, using the pyautogui library to auto-input words, etc.
