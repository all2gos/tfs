import numpy as np
import random
def get_fight_attributes(strength, dxt, condition, int, lvl, armor, min_weapon, max_weapon, hp_by_hand, additional_hp_from_poey, block_chance, crit_chance):
    

    ap = dxt +10 
    hp = 1.25*lvl**2 + 24.4*condition - 96.4*lvl -4948 if hp_by_hand ==0 else hp_by_hand
    sp = 0.2*int*lvl + 2*int - 1.98*lvl  - 22.2
    redu = np.exp(-0.002619*armor)
    min_dmg = 5.14*lvl + 9.49*strength + 120.3*min_weapon-11859.1
    max_dmg = 2.18*lvl + 18.67*strength + 121.4*max_weapon -22352.3


    return {'min_dmg':min_dmg,'max_dmg':max_dmg, 'ap':ap, 'hp':hp+additional_hp_from_poey, 'sp':sp, 'redu':redu, 'block_chance':block_chance, 'crit_chance':crit_chance}



def fight(p1, p2):

    duelist1 = get_fight_attributes(*p1)
    duelist2 = get_fight_attributes(*p2)

    #reduce damage:
    duelist1['min_dmg'] = int(duelist1['min_dmg']*duelist2['redu'])
    duelist2['min_dmg'] = int(duelist2['min_dmg']*duelist1['redu'])

    duelist1['max_dmg'] = int(duelist1['max_dmg']*duelist2['redu'])
    duelist2['max_dmg'] = int(duelist2['max_dmg']*duelist1['redu'])

    #spell damage
    duelist1['hp'] - duelist2['sp'] if duelist2['sp'] > duelist1['sp'] else duelist2['hp'] - duelist1['sp']

    while duelist1['hp'] > 0 and duelist2['hp'] >0:
        
        who_attack = random.choices([0,1], weights=[duelist1['ap'],duelist2['ap']], k=1)[0]


        if who_attack == 0:

            #block = random.choices([1,0], weights=[duelist2['block_chance'],1 - duelist2['block_chance']], k=1)[0]
            #crit = random.choices([1,0], weights=[duelist1['crit_chance'],1 - duelist1['crit_chance']], k=1)[0]
            
            #hit = random.randint(duelist1['min_dmg'],duelist1['max_dmg']) 

            #hit *= random.uniform(1.4,2) if crit == 1 else 1
            #hit *= random.uniform(0.5,0.8) if block ==1 else 1

            duelist2['hp'] -= random.randint(duelist1['min_dmg'],duelist1['max_dmg']) 

        else:

            #block = random.choices([1,0], weights=[duelist1['block_chance'],1 - duelist1['block_chance']], k=1)[0]
            #crit = random.choices([1,0], weights=[duelist2['crit_chance'],1 - duelist2['crit_chance']], k=1)[0]

            #hit = random.randint(duelist2['min_dmg'],duelist2['max_dmg']) 

            #hit *= random.uniform(1.4,2) if crit == 1 else 1
            #hit *= random.uniform(0.5,0.8) if block ==1 else 1

            duelist1['hp'] -= random.randint(duelist2['min_dmg'],duelist2['max_dmg']) 

    return 1 if duelist2['hp'] <1 else 0

if __name__ == '__main__':
    p1 = [6544,1365,1201,1238,112,775,96,183,0, 1, 200]
    p2 = [2311,1000,1000,1000,185,600,1,2,0, 0, 0]

    i = 10000
    cnt = sum(fight(p1,p2) for _ in range(i))

    print(f"Na {i} przeprowadzonych symulacji gracz 1 wygrał {cnt} razy")












