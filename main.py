import streamlit as st
from PIL import Image
import os
from mechanics import *
import itertools
import contextlib
from dungeon_database import dung_dict
import math

st.set_page_config(page_title='TFS', page_icon=':shield:')
st.title('Tanoth Fight Simulator')

st.markdown('Welcome to the website where we implement our project: the [Tanoth](https://tanoth.pl) battle simulator. We created it for one main purpose: to be able to select optimal companions and potions for dungeon and map battles. How and why we do it this way is described here (soon). We hope you find our work useful. ')


def load_image(file_name):
    return Image.open(os.path.join(image_folder, file_name))

def convert_to_int(input_value):
    if input_value:
        with contextlib.suppress(ValueError):
            return int(input_value)


num_companions = st.radio('Choose a number of companions you want to consider',('Just me', '1','2','3'))



image_folder = 'images'
image_files = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

st.write('Pick companions which you already picked')

selected_images = []
cols_per_row = 11
num_rows = len(image_files) // cols_per_row  

for row_idx in range(num_rows):
    cols = st.columns(cols_per_row) 
    for col_idx in range(cols_per_row):
        img_index = row_idx * cols_per_row + col_idx
        if img_index < len(image_files):
            img = load_image(image_files[img_index])
            
            with cols[col_idx]:
                st.image(img, use_column_width=True)
                
                if st.checkbox("label", key=img_index, label_visibility='hidden'):
                    selected_images.append(image_files[img_index].split('.')[0])

num_companions = 0 if num_companions =='Just me' else int(num_companions)

print(selected_images)
if len(selected_images) != num_companions:
    st.error(f"You have to select exactly {num_companions} companions. Instead you pick {len(selected_images)}.")
else:

    your_lvl = convert_to_int(st.text_input('Please enter your lvl:'))

    st.write('Please enter your stats now.')


    type_of_fight = st.radio('Select which type of fight do you want to analyze',('map/dung','pvp fight'))

    if type_of_fight == 'pvp fight':
        st.write('in future')

    if type_of_fight == 'map/dung':
        your_s = convert_to_int(st.text_input('Please enter your strenght in dun/map:'))
        your_d = convert_to_int(st.text_input('Please enter your dexterity in dun/map:'))
        your_c = convert_to_int(st.text_input('Please enter your constitution in dun/map:'))
        your_i = convert_to_int(st.text_input('Please enter your intelligence in dun/map:'))

        st.write('Also we need your main character stats separately')

        char_s = convert_to_int(st.text_input('Please enter character strenght:'))
        char_d = convert_to_int(st.text_input('Please enter character dexterity:'))
        char_c = convert_to_int(st.text_input('Please enter character constitution:'))
        char_i = convert_to_int(st.text_input('Please enter character intelligence:'))

        d = {
            'galwin': [9.33, 4.66, 4.66, 4.66],
            'theo': [7, 4.66, 9.33, 2.33],
            'melpheus': [2.33, 4.66, 4.66, 11.66],
            'paul': [4.66, 4.66, 7, 7],
            'rubus':[4.66, 4.66, 4.66,  9.33],
            'etheria':[3.5, 4.66, 9.33, 5.85],
            'lorica':[2.33, 11.66, 4.66, 4.66],
            'metrix':[0.23, 7, 4.66, 11.45],
            'askar':[13.78, 0.23, 7, 2.33],
            'thorax':[7,3.5,9.33, 3.5],
            'aurum':[4.66, 8.18, 4.66, 5.85],
            'forbis':[5.85,8.18,4.66,4.66],
            'urk':[9.33,2.33,7,2.33],
            'ganuk':[2.33,16.12,0.23,4.75],
            'dark knight':[9.33,7,7,0.23],
            'tar':[4.66,7,4.66,7],
            'tim':[2.33,9.33,9.33,2.33],
            'zor':[9.11,0.23,4.9,9.11],
            'caro':[6.3,4.66,10.5,1.86],
            'anja':[5.37,12.85,2.33,2.8],
            'sylvia':[2.33,8.4,3.5,9.11],
            'eliane':[3.5,8.17,4.66,7]
        }

        if your_lvl:
            comp_s = sum(d[x][0] for x in selected_images) * your_lvl
            comp_d = sum(d[x][1] for x in selected_images) * your_lvl
            comp_c = sum(d[x][2] for x in selected_images) * your_lvl
            comp_i = sum(d[x][3] for x in selected_images) * your_lvl

        if str(char_i).isdigit():
            if num_companions > 0:
                st.write(f'Based on your companions selection we can compute that your character and all eq stats are: {int(your_s - comp_s)} strenght, {int(your_d - comp_d)} dexterity, {int(your_c - comp_c)} constitution, {int(your_i - comp_i)} intelligence')

            your_s_comps_eq = int(your_s - comp_s-char_s)
            your_d_comps_eq = int(your_d - comp_d-char_d)
            your_c_comps_eq = int(your_c - comp_c-char_c)
            your_i_comps_eq = int(your_i - comp_i-char_i)

            your_dmg = st.text_input('Add your weapon damage in form 50-100')
            if len(your_dmg) > 0: your_dmg_min, your_dmg_max = [int(x) for x in your_dmg.split('-')]
            your_block = st.text_input('Add your block chance in form 27%').replace('%','')
            if your_block.isdigit(): your_block = int(your_block)
            your_armor =  st.text_input('Add your armor')
            if your_armor.isdigit(): your_armor = int(your_armor)

            your_poey = 0
            if st.checkbox('Select this if you use Potion of Eternal Youth'):
                your_poey = 1
            rune_lvl = st.text_input('Please provide your Ruby level')
            if rune_lvl.isdigit(): 
                rune_lvl = int(rune_lvl)/1000
            skull_lvl = st.text_input('Please provide your Skull lvl')
            if skull_lvl.isdigit(): skull_lvl = int(skull_lvl)
            potion_size = st.radio('Select the size of potion to be considered in simulations',('small','medium','big'))

            if active_potion := st.checkbox('Select this if you have an active potion'):
                active_potion_size = st.radio('Select size of potion',('small','medium','big'))
                active_potion_type = st.radio('Select type of potion', ('str','dex','con','int'))

            if rune_lvl: stat_potion_inf = 1+ 0.1*(1+rune_lvl) if potion_size == 'small' else 1+ 0.15*(1+rune_lvl) if potion_size == 'medium' else 1 + 0.25*(1+rune_lvl)

            st.markdown('#### Enemy info')  

            enemy_type_info = st.radio('',('I want to pick the enemy from the prepared database','I want to type the stats of my enemy by hand'))


            if enemy_type_info == 'I want to type the stats of my enemy by hand':
                enemy_hp = 0
                enemy_lvl = convert_to_int(st.text_input('Please enter enemy level:'))
                enemy_s = convert_to_int(st.text_input('Please enter enemy strenght:'))
                enemy_d = convert_to_int(st.text_input('Please enter enemy dexterity:'))
                enemy_c = convert_to_int(st.text_input('Please enter enemy constitution:'))
                if st.checkbox('Click here if you would rather prefer to type enemy hp by hand (recommended in dungeon/map battles)'):
                    enemy_hp = convert_to_int(st.text_input('Please enter enemy hp'))
                enemy_i = convert_to_int(st.text_input('Please enter enemy intelligence:'))

                enemy_dmg = st.text_input("Please enter enemy's weapon damage in form 50-100 (Based on the visual look of the weapon, usually 1-2 for dungeon enemies)")
                
                if len(enemy_dmg) > 1: enemy_dmg_min, enemy_dmg_max = [int(x) for x in enemy_dmg.split('-')]
                enemy_block = st.text_input('Add enemy block chance in form 27% (Based on the visual look of the shield, usually, in dungeon: 5%)')
                enemy_block = int(enemy_block.replace('%',''))
                enemy_armor =  st.text_input('Add enemy armor')
                if enemy_armor.isdigit(): enemy_armor = int(enemy_armor)
            else:
                
                select_floor = st.text_input('Please provide floor of dungeon on which you are currently on.')
                
                if select_floor in dung_dict:
                    st.write(f"You picked floor {select_floor}, {dung_dict[select_floor]['name']}")
                    
                    oculus = st.checkbox('I have oculus!')
                    oposing_s = st.text_input('Sum of strength which your eq substract WITHOUT OCULUS')
                    oposing_d = st.text_input('Sum of dexterity which your eq substract WITHOUT OCULUS')
                    oposing_c = st.text_input('Sum of constitution which your eq substract WITHOUT OCULUS')
                    oposing_i = st.text_input('Sum of intelligence which your eq substract WITHOUT OCULUS')

                    oposing_s = int(oposing_s) if oposing_s.isdigit() else 0
                    oposing_d = int(oposing_d) if oposing_d.isdigit() else 0
                    oposing_c = int(oposing_c) if oposing_c.isdigit() else 0
                    oposing_i = int(oposing_i) if oposing_i.isdigit() else 0

                    if oculus: 
                        oculus = 1 
                    else: 
                        oculus = 0

                    enemy_lvl = dung_dict[select_floor]['level'] 
                    enemy_s = dung_dict[select_floor]['strengh'] - 1.5*your_lvl*oculus - oposing_s
                    enemy_d = dung_dict[select_floor]['dexterity']- 1.5*your_lvl*oculus - oposing_d
                    enemy_c = dung_dict[select_floor]['constitution']- 1.5*your_lvl*oculus - oposing_c
                    enemy_hp = int(dung_dict[select_floor]['hp'] * 1.65)

                    enemy_i = dung_dict[select_floor]['intelligence']- 1.5*your_lvl*oculus - oposing_i
                    enemy_dmg_min, enemy_dmg_max = 1,2
                    enemy_block = 5
                    enemy_armor =  dung_dict[select_floor]['armor']


                    hp_correct = st.checkbox('If you have any subtractive stats eq we strongly recommend to enter hp of your enemy by hand hence we do not have good aprox for hp of dung enemies yet.')

                    if hp_correct:
                        enemy_hp = st.text_input('Please provide hp of your enemy')
                        if enemy_hp.isdigit(): enemy_hp = int(int(enemy_hp)*1.65)
                else:
                    st.write('Sorry we do not support prepared data for your floor. Alternatively you enter you dungeon floor wrongly.')


            potion_translation = {'s':'strength','d':'dexterity','c':'constitution','i':'intelligence'}
            c = 0
            if fight_button:= st.button('Analyze fight'):
                progress_bar = st.progress(0)
                max_cnt = 0
                if type_of_fight == 'map/dung':
                    st.write('Fight is being analyzed')

                    #st.write(f'Info about your enemy: lvl: {enemy_lvl}, strength: {enemy_s}, hp: {enemy_hp}, damage: {enemy_dmg_min}-{enemy_dmg_max}')
                    uniq_comb_of_comp = sorted([tuple(sorted(comb)) for comb in itertools.combinations(d.keys(), num_companions)][:])


                    idx = uniq_comb_of_comp.index(tuple(sorted(selected_images)))

                    if active_potion:
                        active_potion_inf = 1 + 0.1*(1+rune_lvl) if active_potion_size == 'small' else 1 + 0.15*(1+rune_lvl) if active_potion_size == 'medium' else 1 + 0.25*(1+rune_lvl)
                        
                        if active_potion_type == 'str': 
                            char_s /= active_potion_inf 
                        elif active_potion_type == 'dex': 
                            char_d /= active_potion_inf
                        elif active_potion_type == 'con': 
                            char_c /= active_potion_inf
                        elif active_potion_type == 'int': 
                            char_i /= active_potion_inf
                    for i,comps in enumerate([list(uniq_comb_of_comp[idx])] + uniq_comb_of_comp):
                        for type_of_potion in ['s','d','c','i']:
                            comp_s = round((d[comps[0]][0] + d[comps[1]][0] + d[comps[2]][0])*your_lvl) 
                            comp_d = round((d[comps[0]][1] + d[comps[1]][1] + d[comps[2]][1])*your_lvl)
                            comp_c = round((d[comps[0]][2] + d[comps[1]][2] + d[comps[2]][2])*your_lvl)
                            comp_i = round((d[comps[0]][3] + d[comps[1]][3] + d[comps[2]][3])*your_lvl)

                            if type_of_potion == 's': 
                                char_s *= stat_potion_inf 
                            elif type_of_potion == 'd': 
                                char_d *= stat_potion_inf
                            elif type_of_potion == 'c': 
                                char_c *= stat_potion_inf
                            elif type_of_potion == 'i': 
                                char_i *= stat_potion_inf
                            additional_hp_from_poey_char = (1.25*your_lvl**2 + 24.4*char_c - 96.4*your_lvl -4948)*your_poey*(0.3*(1+rune_lvl))
                            additional_hp_from_poey_enemy = 0

                            p1 = [int(char_s + your_s_comps_eq + comp_s), 
                                int(char_d + your_d_comps_eq + comp_d), 
                                int(char_c + your_c_comps_eq + comp_c), 
                                int(char_i + your_i_comps_eq + comp_i), 
                                your_lvl, your_armor, your_dmg_min, your_dmg_max,
                                0, additional_hp_from_poey_char, your_block/100, 0.05+0.02*skull_lvl]
                            
                            p2 = [enemy_s, 
                                enemy_d, 
                                enemy_c, 
                                enemy_i, 
                                enemy_lvl, enemy_armor, enemy_dmg_min, enemy_dmg_max, 
                                enemy_hp, additional_hp_from_poey_enemy, enemy_block/100, 0.05]

                            fight_counter = 50
                            cnt = 100*sum(fight(p1,p2) for _ in range(fight_counter))/fight_counter

                            progress_bar.progress((i + 1) / (len(uniq_comb_of_comp)+1))

                            full_name_of_comps =  {
                                'galwin': "Sir Galwin",
                                'theo': "Theodore the Knight",
                                'melpheus': "Melpheus the Magician",
                                'paul': "Paul the Monk",
                                'rubus':"Rubus the Druid",
                                'etheria':"Etheria",
                                'lorica':'Lorica the Huntress',
                                'metrix':'Metrix the Enchantress',
                                'askar':'Askar the Axeman',
                                'thorax':'Thorax',
                                'aurum':"Thief's Aurum",
                                'forbis':'Forbis the Marksman',
                                'urk':'Urk ka the Warrior',
                                'ganuk':'Ganuk the Spy',
                                'dark knight':'The Dark Knight',
                                'tar':'Tar su the Orc Shaman',
                                'tim':'Tim the Vagabond',
                                'zor':'Zor the Troll Mage',
                                'caro':'Caro the Warrior',
                                'anja':'Anja the Assasin',
                                'sylvia':'Sylvia the Witch',
                                'eliane':'Princess Eliane'
                            }

                            if i == 0:

                                if cnt >= max_cnt:
                                    statement = f'This is your current pick: {", ".join(full_name_of_comps[x] for x in comps)}. And TFS calculate your chance to win as {cnt}. Best possible potion configuration: Potion of Eternal Youth: {"active" if your_poey == 1 else "not active"} and {potion_size} {potion_translation[type_of_potion]} potion.'
                                    c += 1
                                    max_cnt = 0
                                if c == 4:
                                    st.write(statement)
                            if cnt > max_cnt and i !=0:

                                st.write(f'TFS found a better configuration: Based on {fight_counter} simulation you have {cnt:.2f} relative points to win. Comps: {", ".join(full_name_of_comps[x] for x in comps)}. Potion: {potion_size} {potion_translation[type_of_potion]}  potion, Potion of the Eternal Youth: {"active" if your_poey == 1 else "not active"}')
                                max_cnt = cnt

                            if math.isclose(max_cnt, 100.0, abs_tol=0.01):
                                break

                            if type_of_potion == 's': 
                                char_s /= stat_potion_inf 
                            elif type_of_potion == 'd': 
                                char_d /= stat_potion_inf
                            elif type_of_potion == 'c': 
                                char_c /= stat_potion_inf
                            elif type_of_potion == 'i': 
                                char_i /= stat_potion_inf
                if i == len(uniq_comb_of_comp) or max_cnt == 100:
                    st.write('We hope that you find TFS usefull. If you find any problem or you have any suggestions do not hesitate to catch us on discord!')
                    st.write('If you appreciate our work there is an option to [buy some Bloodstones for us](https://buymeacoffee.com/all2). Thanks!')   
                                            