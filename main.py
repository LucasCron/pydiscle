import csv
import random

NUM = "num"
NAME = "name"
MANU = "manufacturer"
SP = "speed"
GL = "glide"
TURN = "turn"
FADE = "fade"
TYPE = "type"


def read_disc_db(file):
    with open(file) as csv_file:
        columns = {}
        lookup = {}
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                row_count = 0
                for item in row:
                    columns[item] = row_count
                    row_count += 1
                line_count += 1
            else:
                lookup[row[columns[NAME]]] = {
                    NUM: int(row[columns[NUM]]),
                    NAME: row[columns[NAME]],
                    MANU: row[columns[MANU]],
                    SP: float(row[columns[SP]]),
                    GL: float(row[columns[GL]]),
                    TURN: float(row[columns[TURN]]),
                    FADE: float(row[columns[FADE]]),
                    TYPE: row[columns[TYPE]],
                }
                line_count += 1
        return lookup


def compare_num(actual, guess) -> str:
    if actual == guess:
        return "Green"
    elif actual > guess:
        return "^"
    elif actual < guess:
        return "V"
    else:
        return "Grey?"


def compare_str(actual, guess) -> str:
    if actual == guess:
        return "Green"
    else:
        return "Grey"


def pad(val: str, size=6):
    return str(val).ljust(size, ' ')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db_version = 3
    db = read_disc_db(f'discs-db-{db_version}.csv')
    disc = random.choice(list(db))
    correct = False
    guesses = 0
    while not correct and guesses < 5:
        inp = input("tell me a disc name: ")
        if db.get(inp) is None:
            print("not a disc...")
        elif inp == disc:
            print("you win!")
            correct = True
        else:
            guesses += 1
            print("wrong")
            print(f'guess  = {MANU}:{pad(db[inp][MANU], 10)}'
                  f'{SP}:{pad(db[inp][SP])}'
                  f'{GL}:{pad(db[inp][GL])}'
                  f'{TURN}:{pad(db[inp][TURN])}'
                  f'{FADE}:{pad(db[inp][FADE])}'
                  f'{TYPE}:{db[inp][TYPE]}')
            print(f'actual = {MANU}:{pad(compare_str(db[disc][MANU], db[inp][MANU]), 10)}'
                  f'{SP}:{pad(compare_num(db[disc][SP], db[inp][SP]))}'
                  f'{GL}:{pad(compare_num(db[disc][GL], db[inp][GL]))}'
                  f'{TURN}:{pad(compare_num(db[disc][TURN], db[inp][TURN]))}'
                  f'{FADE}:{pad(compare_num(db[disc][FADE], db[inp][FADE]))}'
                  f'{TYPE}:{compare_str(db[disc][TYPE], db[inp][TYPE])}')

    if guesses >= 5:
        print("you failed, it was the " + disc)
