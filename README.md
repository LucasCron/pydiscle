# PyDiscle
Python implementation of Discle, the disc golf disc mold Wordle game.

The player essentially has a set number of guesses to figure out which mold is the correct answer.

Each round the player guesses a mold, and if incorrect, the game will tell the player certain pieces of information.

Said pieces of information:
* Manufacturer
* Speed
* Glide
* Turn
* Fade
* Type

For the flight numbers, the game will tell the player if the actual number is higher or lower than the guess. For the manufacturer and type, it will just tell the player whether or not the guess is correct.

I manually made the CSV files with all the disc mold information, so it is not necessarily correct, and is definitely not comprehensive. I mostly chose to include molds I had either thrown or heard of before. Eventually I may add even more to try to be as comprehensive as possible.