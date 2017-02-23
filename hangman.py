import random

HANGMANIMGS = ['''
   +---+
   |   |
       |
       |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
       |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
   |   |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|   |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
       |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
  /    |
       |
 =========''', '''

   +---+
   |   |
   O   |
  /|\  |
  / \  |
       |
 =========''']


# grab list of words from the web and save them into a list, remove all words smaller than 4 characters
from urllib.request import urlopen
word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urlopen(word_site).read().decode("utf-8")
words = response.split()
blanks = ''
for word in words:
    word.lower()
    if len(word)<4:
      words.remove(word)

# Get random word from list of words
def getRandomWord(wordList):
   wordIndex = random.randint(0, len(wordList) - 1)
   return wordList[wordIndex]

# Displays board of hangman after every turn 
def displayBoard(HANGMANIMGS, missedLetters, correctLetters, secretWord):
   print(HANGMANIMGS[len(missedLetters)])
   print()

   print('There are', (len(HANGMANIMGS)-1)-(len(missedLetters)), 'tries left')
   print('Missed letters:', end=' ')
   for letter in missedLetters:
       print(letter, end=' ')
   print()
   
   blanks = '_' * len(secretWord)
   for i in range(len(secretWord)): # replace blanks with correctly guessed letters
       if secretWord[i] in correctLetters:
           blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
   for letter in blanks: # show the secret word with spaces in between each letter
       print(letter, end=' ')
   print()

# Asks user for letter entry and checks for errors 
def userGuess(alreadyGuessed):
   while True:
       print('Guess a letter.')
       guess = input()
       guess = guess.lower()
       if len(guess) != 1:
           print('Please enter a letter.')
       elif guess in alreadyGuessed:
           print('You have already guessed that letter. Choose again.')
       elif guess not in 'abcdefghijklmnopqrstuvwxyz\'':
           print('That was not a letter. Please try again.')
       else:
           return guess

# Return a letter based on letter frequencies in English language
def compGuess(alreadyGuessed): 
  frequencies = {'E':13, 'T':9, 'A':8, 'O':8, 'I':7, 'N':7, 'S':6, 'H':6, 'R':6, 'D':5, 'L':4.0, 'C':3, 'U':3, 'M':2, 'W':2, 'F':2, 'G':2, 'Y':2, 'P':2, 'B':2, 'V':1, 'K':1, 'J':1, 'X':1, 'X':1, 'Q':1, 'Z':1}
  freqArray = []
  # creates array where each letter appears the same number of times as its frequency
  for letter,frequency in frequencies.items(): 
    for i in range(int(frequency)):
      freqArray.append(letter)
  randomLet = freqArray[random.randint(0, len(freqArray) -1)]
  # makes sure the letter hasn't been guessed already
  while (randomLet in alreadyGuessed):
    randomLet = freqArray[random.randint(0, len(freqArray) -1)]
  return randomLet
  
# start of the user interaction
print('Time to play HANGMAN!')
while True: #ask user to input 1 or 2 and makes sure that user inputs only that
  try:
    choice=int(input('Enter (1) to guess a word or (2) for the computer to guess your word '))
  except ValueError:
    print('Please input 1 or 2')
    continue
  if 0<choice<3:
    break
  else:
    print('That is not 1 or 2! Try again.')
#If person is guessing
if choice==1:  
  missedLetters = ''
  correctLetters = ''
  secretWord = getRandomWord(words)
  while True:
     displayBoard(HANGMANIMGS, missedLetters, correctLetters, secretWord)

     #Get guess from the user 
     guess = userGuess(missedLetters + correctLetters)
     if guess in secretWord:
         correctLetters = correctLetters + guess

         # Check if the user has won
         foundAllLetters = True
         for i in range(len(secretWord)):
             if secretWord[i] not in correctLetters:
                 foundAllLetters = False
                 break
         if foundAllLetters:
             print('Yes! The secret word is "' + secretWord + '"! You have won!')
             break
        
     else:
         missedLetters = missedLetters + guess

         # Check if user has guessed too many times and lost
         if len(missedLetters) == len(HANGMANIMGS) - 1:
             displayBoard(HANGMANIMGS, missedLetters, correctLetters, secretWord)
             print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
             break

#if computer is guessing
elif choice==2: 
  print('Think of a word and the computer will guess it!')
  while True:
    try:
      wordLength=int(input('How many letters is your word? '))
    except ValueError:
      print('That is not a number. Please input a number.')
      continue
    if type(wordLength) == int:
      break
    else:
      print('That is not a number. Please try again')

  filledPositions = []
  missedLetters = ''
  correctLetters = ''
  
  # Create a dummy string equivalent in length to the word 
  secretWord = str(wordLength) 
  for i in range(wordLength-1):
    secretWord += str(i)

  while True:
    displayBoard(HANGMANIMGS, missedLetters, correctLetters,secretWord)

    # Computer needs to guess a random letter
    guess = compGuess(missedLetters + correctLetters);
    
    userInput=input('is ' + guess + ' in your word? ')
    if userInput in ('yes','y'):
      correctLetters += guess 
      # error testing to make sure position entered is accurate 
      while True:
        try:
          position=int(input('What position is ' + guess + ' in? '))
        except ValueError:
          print('Please enter a number')
          continue
        #if user input of position is an integer, smaller than length of word, and not already filled then break loop 
        if type(position == int) and (position <= wordLength) and (position not in filledPositions): 
          filledPositions.append(position)
          break
        else:
          print('That position is already filled or is larger than the length of your word')

      secretWord = secretWord[:position-1] + guess + secretWord[position:]

      # Check if the computer has won
      if len(filledPositions) == wordLength:
        print('Your secret word was ' + secretWord)
        print('The computer guessed your secret word! You lost!')
        break

    elif userInput in('no','n'):
          missedLetters += guess;
    else:
      print('Please write yes/y or no/n.')

    # check if game is won
    if len(missedLetters) == len(HANGMANIMGS) - 1:
        displayBoard(HANGMANIMGS, missedLetters, correctLetters, secretWord)
        print('The computer ran of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses. The computer lost, you won!')
        break;
      
  
  
