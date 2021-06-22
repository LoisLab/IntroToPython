import random
import copy

ELF_NAMES =['Elas','Ardith','Candra','Aidon','Kyo','Ryo','Sneiji','Bre','Fra','Elgin','Meina','Posi',\
            'Cosi','Dorn','Klee','Qaio','Maio','Zey','Paila','Sash']

ELF_SPELLS = ['heal', 'sleep', 'invisible', 'freeze', 'fireball', 'poof', 'shadow', 'stall']


def party(n):
    names = copy.deepcopy(ELF_NAMES)
    elves = []
    for x in range(n):
        new_elf = elf(names)
        names.remove(new_elf['name'])
        elves.append(new_elf)
    return elves
    
    
def elf(names = ELF_NAMES):
    name = random.choice(names)
    return {'name': name,
            'race': 'elf',
            'friends': {random.choice(ELF_NAMES) for x in range(5)}-{name},
            'spells': {random.choice(ELF_SPELLS) for x in range(3)},
            'height': round(3 + 3*random.random(), 1),
            'health': random.randint(30,45),
            'intelligence': random.randint(15,45)}


def weapon_test(weapon):
    e = elf()
    print(e['name'] + ' wields a ' + weapon.__str__() + ' with ' + random.choice((['determination', 'ferocity', 'angst'])))
    print(e['name'] + ' attacks, ' + weapon.sound() + '!, doing ' + str(weapon.attack()) + ' damage.\n')
       