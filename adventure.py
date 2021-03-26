import time
import numpy as np
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


class DragonFire(Weapon):
    def attack(self):
        return 3 + np.random.randint(1, 6) + np.random.randint(1, 6) + np.random.randint(1, 6)

    def sound(self):
        return random.choice(['whoosh', 'screeeeee', 'foom', 'kaboom', 'zwishhhhhh'])

    def __str__(self):
        return 'dragon fire'


class FreezeSpell(Weapon):

    def attack(self):
        return 3 + np.random.randint(1, 6)

    def sound(self):
        return 'brrrrr...zap'

    def __str__(self):
        return 'ice ball'

class FireballSpell(Weapon):

    def attack(self):
        return np.random.randint(6, 12) * 2

    def sound(self):
        return random.choice(['whoosh', 'screeeeee', 'foom', 'kaboom', 'zwishhhhhh'])

    def __str__(self):
        return 'fireball'


def cast_a_spell(spell, caster, target):
    if spell in caster['spells']:
        caster['spells'].remove(spell)
        print(caster['name'] + ' casts ' + spell + '!')
        if spell == 'freeze':
            use_a_weapon(FreezeSpell(), caster, target)
        elif spell == 'fireball':
            use_a_weapon(FireballSpell(), caster, target)
        elif spell == 'heal':
            effect = sum([np.random.randint(1, 4) for x in range(4)])
            caster['health'] += effect
            print(caster['name'] + ' mumbles heal and gains', effect, 'health, total health is now', caster['health'])
        elif spell == 'poof':
            caster['health'] += sum([np.random.randint(1, 4) for x in range(2)])
            print('Poof! ', caster['name'] + 'vanishes is a puff of smoke and reappears with health of', caster['health'])
            print('...the flash and smoke confuses ', target['name'])
            target['notes'].add('confused')
        elif spell == 'invisible':
            print('(pzzzwing) ', caster['name'], 'casts a spell and the entire party becomes invisible')
            target['notes'].add('blinded')
        elif spell == 'shadow':
            print('(faaaawaaaa) ', caster['name'], 'casts a spell and the entire party becomes shadows of themselves')
            target['notes'].add('seeing shadows')
        elif spell == 'sleep':
            if random.randint(1, 2) == 1:
                print('Shhhh...', caster['name'] + 'casts sleep, ', target['name'], 'nods off.')
                target['notes'].add('asleep')
            else:
                print('Shhhh....', caster['name'] + 'casts sleep, ', target['name'], 'shakes itself awake again!')
        elif spell == 'stall':
            print('Whoa!...', caster['name'] + 'casts stall, ', target['name'], 'stumbles!')
            target['notes'].add('stalled')
    else:
        print(caster['name'] + ' utters ' + spell + ' but nothing happens...')


def use_a_weapon(weapon, attacker, target):
    effect = weapon.attack()
    target['health'] -= min(effect, target['health'])
    print(attacker['name'], 'attacks', target['name'], 'with a', weapon, '...', weapon.sound(), \
          '...', effect, 'damage (', target['health'], 'to go).')


def fight_the_dragon(f, elves):
    dragon = {'name': 'Dread Fxnord', 'weapon': DragonFire(), 'health': 400, 'spells': ['fireball' for x in range (12)]}
    while sum([elf['health'] for elf in elves]) > 0:
        '''
        Elves' turn to attack
        '''
        print('---the elves attack------------------------------------------')
        dragon['notes'] = set()
        for next_elf in elves:
            if next_elf['health'] > 0:
                spell_or_weapon = f(next_elf)
                if isinstance(spell_or_weapon, Weapon): 
                    use_a_weapon(spell_or_weapon, next_elf, dragon)
                elif spell_or_weapon in ELF_SPELLS:
                    cast_a_spell(spell_or_weapon, next_elf, dragon)
                else:
                    print(next_elf['name'] + ' stands idly by, seemingly unconcerned about the dragon.')
                time.sleep(0.75)

        '''
        Dragon's turn to attack
        '''
        print('---the dragon attacks----------------------------------------')
        if dragon['health'] == 0:
            print('The dragon is defeated! It lumbers into the air and flies away.')
            break
        targets = [next_elf for next_elf in elves if next_elf['health'] > 0]

        # cast fireball
        if len(dragon['spells']) > 0:
            if 'confused' in dragon['notes']:
                print(dragon['name'], 'is confused and cannot cast a spell')
            elif 'seeing shadows' in dragon['notes']:
                print(dragon['name'], 'is seeing shadows and cannot decide where to cast a spell')
            else:
                cast_a_spell(dragon['spells'].pop(), dragon, random.choice(targets))

        # use dragon fire
        if 'blinded' in dragon['notes']:
            print(dragon['name'], 'cannot lash out because its enemies are invisible')
        elif 'stalled' in dragon['notes']:
            print(dragon['name'], 'cannot lash out because it is unable to move')
        else:
            use_a_weapon(dragon['weapon'], dragon, random.choice(targets))

        # Status report... how are the combatants holding up?
        print('HEALTH:', [(next_elf['name'], next_elf['health']) for next_elf in elves],'\n')
        if len(dragon['notes']) > 0:
            print(dragon['name'], 'is', dragon['notes'])
            dragon['notes'] = set()
        time.sleep(2.5)

    for next_elf in elves:
        if next_elf['health'] > 0:
            print(next_elf['name'], 'has prevailed over the dragon!')
        else:
            print(next_elf['name'] + ' lies unconscious, waiting for help.')