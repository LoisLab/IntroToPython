import random

ELF_NAMES =['Elas','Ardith','Candra','Aidon','Kyo','Ryo','Sneiji','Bre','Fra','Elgin','Meina','Posi',\
            'Cosi','Dorn','Klee','Qaio','Maio','Zey','Paila','Sash']

ELF_SPELLS = ['heal', 'sleep', 'invisible', 'freeze', 'fireball', 'poof', 'shadow', 'stall']

def party(t, n=1):
    party = []
    while (len(party)<n):
        attempts = 0
        new_member = t()
        while new_member['name'] in [existing_member['name'] for existing_member in party]:
            new_member = t()
            attempts += 1
            if attempts>1000:
                break
        if attempts<1000:
            party.append(new_member)
    return party
    
def elf():
    name = random.choice(ELF_NAMES)
    return {'name': name,
            'race': 'elf',
            'friends': {random.choice(ELF_NAMES) for x in range(3)}-{name},
            'spells': {random.choice(ELF_SPELLS) for x in range(3)},
            'height': round(3 + 3*random.random(), 1),
            'intelligence': random.randint(15,45)}


def weapon_test(weapon):
    e = elf()
    print(e['name'] + ' wields a ' + weapon.__str__() + ' with ' + random.choice((['determination', 'ferocity', 'angst'])))
    print(e['name'] + ' attacks, ' + weapon.sound() + '!, doing ' + str(weapon.attack()) + ' damage.\n')
       