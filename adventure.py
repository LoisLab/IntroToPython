import pandas as pd
from incantations import *


class Weapon:
    '''
    Base class for weapons
    '''
    def __init__(self):
        self.serial_number = random.randint(1000000, 9999999)

    def sound(self):
        return 'thud'

    def __str__(self):
        return 'serial #' + str(self.serial_number)


def non_conflicting_elf(conflicts):
    '''
    The argument 'conflicts' is a set of elf names to be avoided at all cost.
    '''
    while True:
        next_elf = elf()
        is_a_friend = {next_elf['name']} & conflicts
        has_friends_in_common = next_elf['friends'] & conflicts
        if len(is_a_friend)+len(has_friends_in_common) == 0:
            return next_elf


def get_happy_elves(n):
    happy_elves = []
    conflicts = set()
    while len(happy_elves) < n:
        next_elf = non_conflicting_elf(conflicts)
        happy_elves.append(next_elf)
        conflicts |= {next_elf['name']}
        conflicts |= next_elf['friends']
    return happy_elves


def get_the_elves():
    elves = get_happy_elves(5)
    sett = {'name': "Sett",
            'race': 'elf',
            'friends': {'Fredsie'},
            'spells': {'poof'},
            'height': 5.5,
            'health': 36,
            'intelligence': 45}
    elves.insert(0, sett)
    return elves


def equip_the_elves(f, elves):
    for next_elf in elves:
        weapon = f(next_elf)
        if not isinstance(weapon, Weapon):
            raise ValueError(str(weapon) + ' is not a weapon')

        try:
            test = weapon.attack()
        except Exception:
            raise ValueError(str(weapon) + ' cannot attack')

        if not isinstance(test, int):
            raise ValueError(str(weapon) + ' has an attack that does not return an integer value')
        
        attacks = [weapon.attack() for x in range(1000)]
        if max(attacks) > 12:
            raise ValueError(str(weapon) + ' is too powerful! maximum attack exceeds 12')
        if sum(attacks)//1000 > 8:
            raise ValueError(str(weapon) + ' is too powerful! average attack exceeds 8')

        try:
            test = weapon.sound()
        except Exception:
            raise ValueError(str(weapon) + ' does not make a sound')

        if not isinstance(test, str):
            raise ValueError(str(weapon) + ' makes a sound that is not a string')

        next_elf['weapon'] = weapon
        print(next_elf['name'] + ' carries a ' + str(next_elf['weapon']) + ' that goes ' + next_elf['weapon'].sound())
