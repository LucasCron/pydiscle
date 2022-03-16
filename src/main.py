import csv
import random

Y = 'y'
DOWN = 'v'
UP = '^'
GREY = 'grey'
GREEN = 'green'
MANUS = 'manufacturers'

NUM = 'num'
NAME = 'name'
MANU = 'manufacturer'
SP = 'speed'
GL = 'glide'
TURN = 'turn'
FADE = 'fade'
D_RATING = 'discraft rating'
TYPE = 'type'

info_columns = [MANU, SP, GL, TURN, FADE, D_RATING, TYPE]

db_version = 5
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
    # handling for empty Discraft ratings
    if actual is None or disc_guess is None:
        return None

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


def get_d_rating(discraft_only_game, disc_entry):
    return disc_entry.get(D_RATING) if discraft_only_game else None


def print_stat_output(identifier, man, speed, glide, turn, fade, disc_type, drating):
    drating_str = ''
    if drating is not None:
        drating_str = f'{D_RATING}:{drating}'
    print(f'{pad(identifier, identifier_padding)} = {MANU}:{pad(man, string_padding)}'
          f'{SP}:{pad(speed)}'
          f'{GL}:{pad(glide)}'
          f'{TURN}:{pad(turn)}'
          f'{FADE}:{pad(fade)}'
          f'{TYPE}:{pad(disc_type, 10)}'
          f'{drating_str}')


if __name__ == '__main__':
    file_name = f'src/discLookups/discs-db-{db_version}.csv'
    lookup = read_disc_db(file_name)
    disc = random.choice(list(lookup))
    include_list = []

    # short circuit if only want to do Discraft game, since that is my favorite :)
    discraft_only = False
    discraft_only_input = input('discraft only? type y to guess from only discraft: ')
    if discraft_only_input == Y:
        discraft_only = True
        include_list.append('discraft')

    # create include list of manufacturers, can still end up with a Discraft only game
    if not discraft_only:
        include_manufacturers = input('specific manufacturers? type y to choose: ')
        if include_manufacturers == Y:
            for manufacturer in lookup[MANUS]:
                exclude = input(f'include {manufacturer}? type y to include: ')
                if exclude == Y:
                    include_list.append(manufacturer)
        if len(include_list) == 1 and 'discraft' in include_list:
            discraft_only = True

    # getting random disc until found in include list (not optimal, oh well)
    while len(include_list) > 0 and lookup[disc][MANU] not in include_list:
        disc = random.choice(list(lookup))

    actual = lookup[disc]
    actual_drating = get_d_rating(discraft_only, actual)

    correct = False
    guesses = 1
    print('note: disc types are defined by speed: putter 1-3, mid 4-5, fairway 6-8, distance 9-14')
    while not correct and guesses < max_guesses + 1:
        inp = input(f'guess {guesses} -> ')
        if lookup.get(inp) is None:
            print('not a disc... guess again!')
        elif inp == disc:
            print(f'\nyou win! it took you {guesses} guesses')
            correct = True
        else:
            guesses += 1
            print('wrong, guess again!')

            guess = lookup[inp]
            guess_drating = get_d_rating(discraft_only, guess)

            print_stat_output('guess',
                              guess[MANU],
                              guess[SP],
                              guess[GL],
                              guess[TURN],
                              guess[FADE],
                              guess[TYPE],
                              guess_drating)
            print_stat_output('actual',
                              compare_str(actual[MANU], guess[MANU]),
                              compare_num(actual[SP], guess[SP]),
                              compare_num(actual[GL], guess[GL]),
                              compare_num(actual[TURN], guess[TURN]),
                              compare_num(actual[FADE], guess[FADE]),
                              compare_str(actual[TYPE], guess[TYPE]),
                              compare_num(actual_drating, guess_drating))

    if guesses > max_guesses:
        print('\nyou failed!')
        print('it was the ' + disc)

    print_stat_output('stats',
                      actual[MANU], actual[SP],
                      actual[GL], actual[TURN],
                      actual[FADE], actual[TYPE],
                      actual_drating)
