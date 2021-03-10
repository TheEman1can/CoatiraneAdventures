from game.character import CHARACTER_TYPE_INDEX_TO_STRING
from game.skill import ATTACK_TYPE_INDEX_TO_STRING, ELEMENT_INDEX_TO_STRING
from refs import Refs
from text.screens.dungeon_main import box_to_string

BOX_WIDTH = 13


def center_stat(char, index):
    if char is None:
        if index == 6:
            return '-'.center(BOX_WIDTH)
        return ''.center(BOX_WIDTH)
    element = ELEMENT_INDEX_TO_STRING[char.get_element()]
    attack = CHARACTER_TYPE_INDEX_TO_STRING[char.get_attack_type()]
    stat = [char.get_name(), char.get_current_rank(), element, attack, char.get_health(), char.get_mana(), char.get_physical_attack(), char.get_magical_attack(),
            char.get_defense(), char.get_strength(), char.get_magic(), char.get_endurance(), char.get_agility(), char.get_dexterity()]
    stat_labels = ['', 'Rank', '', '', 'HP', 'MP', 'P.Atk.', 'M.Atk.', 'Def.', 'Str.', 'Mag.', 'End.', 'Agi.', 'Dex.']
    if index == 0 or index == 2 or index == 3:
        if ' ' in stat[index]:
            stat[index] = stat[index].split(' ')[0]
        return f'{stat[index]}'.center(BOX_WIDTH)
    return f"{stat_labels[index]}{f'{stat[index]}'.rjust(BOX_WIDTH - 2 - len(stat_labels[index]))}".center(BOX_WIDTH)


def create_bar(left, right, middle, divider, size):
    if size == 0:
        return ''
    string = ''
    for x in range(size):
        if x == 0:
            string += left
        else:
            string += middle
        for _ in range(BOX_WIDTH):
            string += divider
    return string + right


def create_box(size):
    # TODO - Add Selected Labels to box
    box = ['\n\t' + create_bar('┌', '┐', '┬', '─', 1) + '   ' + create_bar('┌', '┐', '┬', '─', size)]
    for stat in range(12):
        box.append('\n\t│')
        box.append('')
        if stat == 6:
            if size == 0:
                box.append('│ ← No Characters obtained')
            else:
                box.append('│ ← │')
        else:
            if size == 0:
                box.append('│')
            else:
                box.append('│   │')
        for _ in range(size):
            box.append('')
            box.append('│')
        # box.append('\t')
    box.append('\n\t│')
    if size == 0:
        box.append('0'.center(BOX_WIDTH) + '│')
    else:
        box.append('0'.center(BOX_WIDTH) + '│   │')
    for index in range(size):
        box.append(f'{1 + index}'.center(BOX_WIDTH))
        box.append('│')
    box.append('\n\t' + create_bar('└', '┘', '┴', '─', 1) + '   ' + create_bar('└', '┘', '┴', '─', size))
    # print(box)
    return box


def populate_box(box, single_char, party, size):
    string = ''.center(BOX_WIDTH)
    gap = 3 + size * 2
    for stat in range(12): # 2 → 9 → 16  7 7
        if single_char is not None:
            box[2 + gap * stat] = center_stat(single_char, stat)
        else:
            if stat == 6:
                box[2 + gap * stat] = '-'.center(BOX_WIDTH)
            else:
                box[2 + gap * stat] = string
        for x in range(size):
            char = party[x]
            if char is not None:
                box[(2 * x + 4) + gap * stat] = center_stat(char, stat)
            else:
                if stat == 6:
                    box[(2 * x + 4) + gap * stat] = '-'.center(BOX_WIDTH)
                else:
                    box[(2 * x + 4) + gap * stat] = string
    return box


def select_screen_char(console):
    char_id_and_index = console._current_screen[len('select_screen_char_'):]
    index = int(char_id_and_index[:char_id_and_index.index('_')])
    single_char = Refs.gc.get_char_by_id(char_id_and_index[char_id_and_index.index('_') + 1:])

    # single_char = None
    # if char_id != 'none':
    #     party = Refs.gc.get_current_party()
    #     for pchar in party:
    #         if pchar is None:
    #             continue
    #         if pchar.get_id() == char_id:
    #             single_char = pchar
    #             break
    obtained_chars = Refs.gc.get_obtained_characters(index >= 8)
    if single_char is not None:
        obtained_chars.remove(single_char)
    display_text = '\n\tChoose a character to put in this slot\n\n'

    if console.memory.select_box is None:
        console.memory.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
        console.memory.select_box = create_box(console.memory.select_box_size)
    else:
        if len(obtained_chars) < console.memory.select_box_size or (console.memory.select_box_size < 8 and len(obtained_chars) > console.memory.select_box_size):
            console.memory.select_box_size = len(obtained_chars) if len(obtained_chars) < 9 else 8
            console.memory.select_box = create_box(console.memory.select_box_size)

    display_text += box_to_string(populate_box(console.memory.select_box, single_char, obtained_chars, console.memory.select_box_size))
    _options = {'0': 'back'}
    if single_char is not None:
        display_text += f'\n\n\t{console.memory.select_box_size + 1}: Remove character\n'
        _options[str(console.memory.select_box_size + 1)] = f'set_char_{index}_none'
    else:
        display_text += '\n'
    for char_index in range(len(obtained_chars)):
        _options[str(char_index + 1)] = f'set_char_{index}_' + obtained_chars[char_index].get_id()
    return display_text, _options
