import csv
import random

Y = "y"
DOWN = "v"
UP = "^"
GREY = "grey"
GREEN = "green"
MANUS = "manufacturers"

NUM = "num"
NAME = "name"
MANU = "manufacturer"
SP = "speed"
GL = "glide"
TURN = "turn"
FADE = "fade"
TYPE = "type"

info_columns = [MANU, SP, GL, TURN, FADE, TYPE]

db_version = 4
max_guesses = 6

identifier_padding = 8
num_padding = 6
string_padding = 12


def read_disc_db(file):
    with open(file) as csv_file:
        column_numbers = {}
        disc_lookup = {MANUS: []}

        rows = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in rows:
            # for the first row just extract the column order to a dict
            if line_count == 0:
                column_index = 0
                for item in row:
                    column_numbers[item] = column_index
                    column_index += 1
            else:
                # creating manufacturer list for later creating exclusion list
                if row[column_numbers[MANU]] not in disc_lookup[MANUS]:
                    disc_lookup[MANUS].append(row[column_numbers[MANU]])

                # initial setup for the lookup entry
                name = row[column_numbers[NAME]]
                disc_lookup[name] = {
                    NUM: row[column_numbers[NUM]],
                    NAME: name
                }
                # extracting the info columns into a dict with name as the key
                for column in info_columns:
                    disc_lookup[name][column] = row[column_numbers[column]]

            line_count += 1
        return disc_lookup


def compare_num(actual, disc_guess) -> str:
    # converting strings to numerics
    num_actual = float(actual)
    num_guess = float(disc_guess)
    if num_actual == num_guess:
        return GREEN
    elif num_actual > num_guess:
        return UP
    elif num_actual < num_guess:
        return DOWN
    else:
        # should not happen
        return GREY


def compare_str(actual, disc_guess) -> str:
    if actual == disc_guess:
        return GREEN
    else:
        return GREY


def pad(val: str, size=num_padding):
    return str(val).ljust(size, ' ')


def print_stat_output(identifier, man, speed, glide, turn, fade, disc_type):
    print(f'{pad(identifier, identifier_padding)} = {MANU}:{pad(man, string_padding)}'
          f'{SP}:{pad(speed)}'
          f'{GL}:{pad(glide)}'
          f'{TURN}:{pad(turn)}'
          f'{FADE}:{pad(fade)}'
          f'{TYPE}:{disc_type}')


if __name__ == '__main__':
    lookup = read_disc_db(f'discLookups/discs-db-{db_version}.csv')
    disc = random.choice(list(lookup))

    exclude_manufacturers = input("exclude manufacturers? type y to exclude: ")
    exclude_list = []
    if exclude_manufacturers == Y:
        for manufacturer in lookup[MANUS]:
            exclude = input(f"exclude {manufacturer}? type y to exclude: ")
            if exclude == Y:
                exclude_list.append(manufacturer)

    while lookup[disc][MANU] in exclude_list:
        disc = random.choice(list(lookup))

    correct = False
    guesses = 1
    print("note: disc types are defined by speed: putter 1-3, mid 4-5, fairway 6-8, distance 9-14")
    while not correct and guesses < max_guesses + 1:
        inp = input(f'guess {guesses} -> ')
        if lookup.get(inp) is None:
            print("not a disc... guess again!")
        elif inp == disc:
            print(f'\nyou win! it took you {guesses} guesses')
            correct = True
        else:
            guesses += 1
            print("wrong, guess again!")

            guess = lookup[inp]
            print_stat_output("guess", guess[MANU], guess[SP], guess[GL], guess[TURN], guess[FADE], guess[TYPE])
            print_stat_output("actual",
                              compare_str(lookup[disc][MANU], lookup[inp][MANU]),
                              compare_num(lookup[disc][SP], lookup[inp][SP]),
                              compare_num(lookup[disc][GL], lookup[inp][GL]),
                              compare_num(lookup[disc][TURN], lookup[inp][TURN]),
                              compare_num(lookup[disc][FADE], lookup[inp][FADE]),
                              compare_str(lookup[disc][TYPE], lookup[inp][TYPE]))

    if guesses > max_guesses:
        print("\nyou failed!")
        print("it was the " + disc)

    print_stat_output("stats",
                      lookup[disc][MANU], lookup[disc][SP],
                      lookup[disc][GL], lookup[disc][TURN],
                      lookup[disc][FADE], lookup[disc][TYPE])
