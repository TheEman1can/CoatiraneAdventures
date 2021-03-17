__all__ = ('CALoader',)

from kivy.resources import resource_find
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher

from loading.char import load_char_chunk
from loading.data import load_screen_chunk
from loading.enemy import load_enemy_chunk
from loading.family import load_family_chunk
from loading.housing import load_housing_chunk
from loading.floor import load_floor_chunk
from loading.move import load_move_chunk
from loading.save import load_save_chunk
from loading.shop import load_shop_item_chunk
from refs import Refs
from modules.builder import Builder

CURRENT_INDEX = 0
TRANSPARENT = 0
STARTING_TOTAL_INDEX = 1
STARTING_CURRENT_INDEX = 0

OPAQUE = 1


class CALoader(Widget):
    max_values = ListProperty([])
    curr_values = ListProperty([])
    messages = ListProperty([])

    def __init__(self, program_type, **kwargs):
        Builder.load_file(resource_find('loading_screen.kv'))
        self.program_type = program_type
        self.layers = {'skills': {}, 'abilities': {}, 'enemies': {}, 'families': {}, 'chars': {}, 'floors': {}, 'shop_items': {}, 'drop_items': {}, 'save': None, 'housing': {}}
        super().__init__(**kwargs)

    def load_base_values(self):
        file = open(resource_find('data/loading_' + self.program_type + '.txt'), "r")
        index = 0
        for x in file:
            if index == 0:
                opt = x[:-1].split(',')
                self.max_values.append(int(opt[CURRENT_INDEX]))
                self.curr_values.append(STARTING_TOTAL_INDEX)
                for y in range(STARTING_TOTAL_INDEX, int(opt[CURRENT_INDEX]) + STARTING_TOTAL_INDEX):
                    self.messages.append(opt[y])
            else:
                if x.startswith('#'):
                    break
                self.max_values.append(int(x))
                self.curr_values.append(STARTING_CURRENT_INDEX)
            index += 1
        self.ids.outer_progress.opacity = TRANSPARENT
        self.ids.inner_progress.opacity = TRANSPARENT
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
        self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def reset(self):
        self.curr_values = []
        self.layers = {'skills': {}, 'abilities': {}, 'enemies': {}, 'families': {}, 'chars': {}, 'floors': {}, 'shop_items': {}, 'drop_items': {}, 'save': None, 'housing': {}}
        self.messages = []
        self.max_values = []
        self.load_base_values()

    def show_bars(self):
        self.ids.outer_progress.opacity = OPAQUE
        self.ids.inner_progress.opacity = OPAQUE

    def update_outer(self):
        self.ids.outer_label.text = f'Loading Data {self.curr_values[CURRENT_INDEX]} / {self.max_values[CURRENT_INDEX]}'
        self.ids.outer_progress.max = self.max_values[CURRENT_INDEX]
        self.ids.outer_progress.value = self.curr_values[CURRENT_INDEX]
        self.update_inner()

    def update_inner(self):
        if self.curr_values[CURRENT_INDEX] <= self.max_values[CURRENT_INDEX]:
            self.ids.inner_label.text = f'{self.messages[self.curr_values[CURRENT_INDEX] - STARTING_TOTAL_INDEX]} {self.curr_values[self.curr_values[CURRENT_INDEX]]} / {self.max_values[self.curr_values[CURRENT_INDEX]]}'
            self.ids.inner_progress.max = self.max_values[self.curr_values[CURRENT_INDEX]]
            self.ids.inner_progress.value = self.curr_values[self.curr_values[CURRENT_INDEX]]

    def increase_total(self, *args):
        self.curr_values[CURRENT_INDEX] += 1
        self.update_outer()
        self.update_inner()

    def increase_current(self, *args):
        self.curr_values[self.curr_values[CURRENT_INDEX]] += 1
        self.update_inner()

    def done_loading(self, loader):
        Refs.log(f"{loader.triggers_finished} / {loader.triggers_total}")
        if loader.triggers_finished == loader.triggers_total:
            Refs.app.finished_loading()

    def load_ratios(self):
        return JsonStore('uix/ratios.json')

    def get(self, layer):
        return self.layers[layer]

    def append(self, layer, key, value):
        self.layers[layer][key] = value

    def set(self, layer, value):
        self.layers[layer] = value

    def load_game(self, save_slot):
        #Show 1 & 0 on the first screen
        self.show_bars()
        self.update_outer()
        self.update_inner()

        #Define a finished "Block"
        def finished_block(sub_loader, callbacks):
            if sub_loader.triggers_finished == sub_loader.triggers_total:
                for callback in callbacks:
                    if callback is not None:
                        callback()


        def load_block(block_loader, isfile, filename, callbacks):
            triggers = []
            if isfile:
                delimiters = ['\n', '\n', '\n', '#', '\n', '#\n', '\n', '#\n', '\n\n', '\n']
                file = open(resource_find(filename), 'r', encoding='utf-8')
                if file.mode == 'r':
                    data = file.read()
                    lines = data.split(delimiters[self.curr_values[CURRENT_INDEX]])
                    if len(lines) != self.max_values[self.curr_values[CURRENT_INDEX]]:
                        raise Exception(f"Wrong initialization numbers! {filename} {delimiters[self.curr_values[CURRENT_INDEX]]} {len(lines)} != {self.max_values[self.curr_values[CURRENT_INDEX]]}")
                else:
                    raise Exception(f"Failed to open {filename}!")

                for line in lines:
                    triggers.append(Clock.create_trigger(lambda dt, l=line: block_loader(l, self, self.program_type, [self.increase_current, sub_loader.inc_triggers, lambda: sub_loader.start(), lambda: finished_block(sub_loader, callbacks)])))
            else:
                triggers.append(Clock.create_trigger(lambda dt: block_loader(self, self.program_type, filename, [self.increase_current, sub_loader.inc_triggers, lambda: sub_loader.start(), lambda: finished_block(sub_loader, callbacks)])))
            sub_loader = GameLoader(triggers)
            sub_loader.triggers_total = len(triggers)
            sub_loader.start()

        triggers = [
            Clock.create_trigger(lambda dt: load_block(load_save_chunk, False, f"{save_slot}", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_move_chunk, True, f"data/char_load_data/{self.program_type}/SA.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_enemy_chunk, True, f"data/enemy_load_data/{self.program_type}/Enemies.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_family_chunk, True, f"data/family_load_data/{self.program_type}/Families.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_housing_chunk, True, f"data/family_load_data/{self.program_type}/Housing.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_char_chunk, True, f"data/char_load_data/{self.program_type}/CharacterDefinitions.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(
                loader)])),
            Clock.create_trigger(lambda dt: load_block(load_floor_chunk, True, f"data/floor_load_data/{self.program_type}/Floors.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_shop_item_chunk, True, f"data/shop_load_data/{self.program_type}/items.txt", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)])),
            Clock.create_trigger(lambda dt: load_block(load_screen_chunk, False, "", [self.increase_total, loader.inc_triggers, lambda: loader.start(), lambda: self.done_loading(loader)]))
        ]
        loader = GameLoader(triggers)
        loader.triggers_total = len(triggers)
        loader.start()


class GameLoader(EventDispatcher):
    def __init__(self, triggers, **kwargs):
        self.triggers = triggers
        self.triggers_finished = 0
        self.triggers_total = 0
        super().__init__(**kwargs)

    def inc_triggers(self):
        self.triggers_finished += 1

    def start(self):
        if len(self.triggers) > 0:
            trigger = self.triggers.pop(0)
            trigger()
