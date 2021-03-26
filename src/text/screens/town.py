from random import randint

from refs import END_OPT_C, OPT_C, RED_C, Refs


def get_town_header():
    # Return a string that contains Name, Varenth and current Renown
    # 165 is the width of the screen, approximately
    name = Refs.gc.get_name()
    domain = Refs.gc.get_domain()
    renown = Refs.gc.get_renown()
    varenth = Refs.gc.format_number(int(Refs.gc.get_varenth()))
    skill_level = Refs.gc.get_skill_level()
    if Refs.gc.get_inventory().has_item('pocket_watch'):
        time = Refs.gc.get_time()
        return '\n\t' + f'{name} - {domain} - Perks Unlocked {skill_level}'.rjust(40).ljust(100) + f'{time} - {varenth} Varenth - Renown {renown}'.ljust(30).rjust(55) + '\n'
    else:
        return '\n\t' + f'{name} - {domain} - Perks Unlocked {skill_level}'.rjust(40).ljust(100) + f'{varenth} Varenth - Renown {renown}'.ljust(30).rjust(55) + '\n'


def town_main(console):
    console.header_callback = get_town_header
    display_text = '\n\tYou are currently in the town center.\n\tWhere would you like to go?\n'
    if Refs.gc.get_housing().get_bill_due() < 0:
        display_text += f'\n\t{RED_C}Your housing bill is overdue!{END_OPT_C}\n'
    elif Refs.gc.get_housing().get_bill_due() < 5:
        display_text += f'\n\t{RED_C}Your housing bill is due in {Refs.gc.get_housing().bill_due()} days.{END_OPT_C}\n'
    display_text += f'\n\t{OPT_C}0:{END_OPT_C} Tavern'
    if Refs.gc.is_tavern_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Shop'
    display_text += f'\n\t{OPT_C}2:{END_OPT_C} Quests'
    display_text += f'\n\t{OPT_C}3:{END_OPT_C} Crafting'
    if Refs.gc.is_crafting_locked():
        display_text += ' - LOCKED'
    display_text += f'\n\t{OPT_C}4:{END_OPT_C} Inventory'
    display_text += f'\n\t{OPT_C}5:{END_OPT_C} Your profile'
    display_text += f'\n\t{OPT_C}6:{END_OPT_C} Housing'
    display_text += f'\n\t{OPT_C}7:{END_OPT_C} Almanac\n'
    display_text += f'\n\t{OPT_C}8:{END_OPT_C} Dungeon\n'
    display_text += f'\n\n\t{OPT_C}9:{END_OPT_C} Save Game\n'
    display_text += f'\t{OPT_C}10:{END_OPT_C} Exit to Main Menu\n'
    _options = {
        '0': 'tavern_main',
        '1': 'shop_main',
        '2': 'quests_main',
        '3': 'crafting_main',
        '4': 'inventory*0',
        '5': 'profile_main',
        '6': 'housing_main',
        '7': 'almanac_main',
        '8': 'dungeon_main',
        '9': 'save_game',
        '10': 'goto_new_game'
    }
    return display_text, _options


def profile_main(console):
    console.header_callback = None
    display_text = f'\n\n\n\t{Refs.gc.get_name()}'
    display_text += f'\n\t{Refs.gc.get_domain()} {Refs.gc.get_gender()}'
    domain = Refs.gc.get_domain_info()
    domain_desc = domain.get_large_description().replace('\n', '\n\t')
    display_text += f'\n\t{domain.get_title()}\n\t{domain_desc}\n'
    display_text += f'\n\tRenown - {Refs.gc.get_renown()}'
    display_text += f'\n\tCurrent Perk Points - {Refs.gc.get_perk_points()}'
    display_text += f'\n\tPerks Unlocked {Refs.gc.get_skill_level()}'
    display_text += f'\n\tYou have {Refs.gc.format_number(Refs.gc.get_varenth())} Varenth'
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Skill Trees'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    _options = {'0': 'back', '1': 'skill_tree_main'}
    return display_text, _options


def tavern_main(console):
    console.header_callback = get_town_header
    display_text = '\n\tWelcome to the tavern!\n\tWhat would you like to do?\n'

    display_text += f'\n\t{OPT_C}1:{END_OPT_C} Relax\n'
    display_text += f'\t{OPT_C}2:{END_OPT_C} Chat with others\n'
    display_text += f'\t{OPT_C}3:{END_OPT_C} Throw a recruitment party'

    _options = {
        '0': 'back',
        '1': 'tavern_relax',
        #'2': 'tavern_chat',  # Randomly unlock something in the almanac
        '3': 'tavern_recruit'
    }

    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def tavern_relax(console):
    console.header_callback = get_town_header
    display_text = ''

    texts = ['You enjoy a hearty ale and relax among the crowd.',
             'Good thing you aren\'t lactose intolerent, as you love cheese.',
             'Sitting in the corner like a weirdo, you devour a chicken leg.',
             'Om nom nom. Glug, glug, glug. *sigh*',
             'Yum. You love the food in Gekkai.',
             'Your family hates you because you spend all their money on booze.',
             'You get hit in the face by a wild skrimp!',
             'You catch up with an old friend.',
             'You watch as someone dips a fry in blood and then eats it. Gross.',
             'You run into the god of posterity. You hate that dude.',
             'Your friend introduces you to a new wine. You get very drunk.',
             'Blonde, brunette, where are all the redheads?',
             'Someone dropped their sandwich. Poor sandwich.',
             'Coffee or booze? Why not both? Welcome to irish coffee.',
             'The only way to ignore the annoying goddess of gems is to drink more.',
             'You get chased by a cross-dressing shrimp in a fedora. Oh, wait. You were asleep.',
             'You run into a wild cannibalistic penguin. They\'re a great drinking buddy.',
             'Dodo birds are the long lost cousin of the Jack Bird. I wonder if they pooped gold too?',
             'Ow! You got nailed by a smiling orange.']

    cost = randint(100, 300)
    if cost > Refs.gc.get_varenth():
        display_text += '\n\tYou don\'t have enough money to buy any refreshments!'
    else:
        Refs.gc.update_varenth(-cost)
        text = texts[randint(0, len(texts) - 1)]
        point = randint(1, 100) > 95
        point_text = 'You gain 1 skill point.' if point else ''
        if point:
            Refs.gc.add_skill_point()
        display_text += f'\n\t{text}\n\t{point_text}'

    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, _options


def tavern_recruit(console):
    console.header_callback = get_town_header

    display_text = '\n\tThrowing a party for recruitment will cost 25,000V.\n\tAre you sure you would like to throw a party?'

    _options = {'0': 'back', '1': 'tavern_recruit_start'}
    display_text += f'\n\n\t{OPT_C}1:{END_OPT_C} Yes! Party time!'
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Back\n'
    return display_text, _options


def get_character_string(character):
    string = f'\n\t\t{character.get_display_name()} - {character.get_name()} - {character.get_age()} - {character.get_gender()} - {character.get_race()}'
    if not character.is_support():
        string += f'\n\t\tFavorite Weapons: {character.get_favorite_weapon()}'
        sub_weapon = character.get_favorite_sub_weapon()
        if sub_weapon is not None:
            string += f', {sub_weapon}'
    string += f'\n\t\t{character.get_description()}'
    if not character.is_support():
        string += f'\n\n\t\tAdventurer - {character.get_attack_type_string()} - {character.get_element_string()}'
    else:
        string += f'\n\n\t\tSupporter'
    string += f'\n\n\t\tHealth    - {character.get_health()}'
    string += f'\n\t\tMana      - {character.get_mana()}'
    string += f'\n\t\tStrength  - {character.get_strength()}'
    string += f'\n\t\tMagic     - {character.get_magic()}'
    string += f'\n\t\tEndurance - {character.get_endurance()}'
    string += f'\n\t\tAgility   - {character.get_agility()}'
    string += f'\n\t\tDexterity - {character.get_dexterity()}\n'
    return string


def tavern_recruit_show(console):
    character_ids = console.get_current_screen()[len('tavern_recruit_show'):].split('#')
    text = character_ids.pop(0)

    fail_texts = ['Lots of people showed up! They only came for the food though.',
                  'You talked to many people, but they all found you boring.',
                  'Next time, try increasing your charm.',
                  'You get slapped in the face after you "flirt" with the locals.',
                  'You got so drunk, you passed out before talking to anybody.',
                  'The shame of explaining the boot print on your face will last a lifetime.',
                  'You were amazing! Wonderful! Still nobody liked you.',
                  'Your as interesting as a rock.',
                  'If I had been at your party, I would have cried.',
                  'Here, have some tissues.',
                  'You call that a party? You only had two chicken wings.',
                  'Next time, order more booze!',
                  'You suck. Go home.',
                  'A cute girl liked you. Sadly she already has a family.',
                  'The buffest guy vibed with you. He\'s already in a family.']

    success_texts = ['They loved your hair!',
                     'You are so cool!',
                     'Foooooooooooood!',
                     'Your party will be the talk of the town for the next month!',
                     'You forgot to mention it was a casual party, but people still loved you.',
                     'When you next throw a party, everybody will be interested.',
                     '*dance*, *dance*, *dance*']
    _options = {'0': 'back'}
    if text == '':
        if 'failure' in character_ids:
            text = fail_texts[randint(0, len(fail_texts) - 1)] + '\n\tBetter luck next time!\n'
        else:
            text = success_texts[randint(0, len(success_texts) - 1)] + '\n\tYou got a potential recruit!\n'

    display_text = f'\n\t{text}\n\t'
    if 'failure' not in character_ids:
        character_id = character_ids[0]
        character = Refs.gc.get_char_by_id(character_id)

        display_text += get_character_string(character)
        display_text += f'\n\tIt will cost you '

        recruitment_items = character.get_recruitment_items()
        list = len(recruitment_items) >= 3
        for index, (item_id, count) in enumerate(recruitment_items.items()):
            print(item_id, count)
            if index == len(recruitment_items) - 1:
                if not list:
                    display_text += ' '
                display_text += 'and '
            if item_id == 'varenth':
                display_text += f'{count} Varenth'
            else:
                item = Refs.gc.find_item(item_id)
                if item is None:
                    continue
                display_text += f'{count} {item.get_name()}'
            if list and index != len(recruitment_items) - 1:
                display_text += ', '

        display_text += f' to convince this person to join your family.\n'

        next_screen = f'tavern_recruit_show{text}#'
        _options['1'] = f'tavern_recruit_end#{character_id}'
        for char_id in character_ids[1:]:
            next_screen += char_id + '#'
        display_text += f'\n\t{OPT_C}1:{END_OPT_C} Recruit this person\n'
        if len(character_ids) > 1:
            display_text += f'\t{OPT_C}2:{END_OPT_C} Continue the party'
            _options['2'] = next_screen[:-1]
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Cancel\n'
    else:
        display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} Continue\n'
    return display_text, _options


def quests_main(console):
    console.header_callback = get_town_header
    display_text = 'Not yet Implemented.\n'
    _options = {'0': 'back'}
    display_text += f'\n\n\t{OPT_C}0:{END_OPT_C} back\n'
    return display_text, _options
