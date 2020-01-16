from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty
from src.modules.Screens.SinglePreview import SinglePreview
from src.modules.Screens.ScrollPreview import ScrollPreview
from src.modules.Screens.GridPreview import GridPreview
from src.modules.HTButton import HTButton
from src.modules.Sortable import SortWidget
from src.modules.Filterable import FilterWidget

class CharacterSelector(Screen):
    toggle = BooleanProperty(False)  # When False, Is Slots
    def __init__(self, main_screen, preview, isSupport, **kwargs):
        size = main_screen.size
        super().__init__(size=size)
        self.name = 'select_char'
        self.background = Image(source="../res/screens/backgrounds/background.png", size=self.size, pos=self.pos, keep_ratio=True, allow_stretch=True)
        with self.background.canvas:
            Color(0, 0, 0, .1)
            Rectangle(size=(self.size[0], self.size[1] * 0.15), pos=(self.pos[0], self.size[1] * 0.85))

        if not isSupport:
            characters = main_screen.obtained_characters_a.copy()
        else:
            characters = main_screen.obtained_characters_s.copy()

        for x in range(len(characters)):
            characters[x] = main_screen.characters[characters[x]]

        has_left = preview.char is not None and not isSupport or isSupport and preview.support is not None
        self.slot_size = (size[1] * .6 * (250 / 935), size[1] * .6)
        self.grid_size = (self.slot_size[0], self.slot_size[0])
        if has_left:
            self.single_window_size = size[0] * .15, self.size[1] * .85
            self.single_window_pos = (0, 0)
            self.multi_window_size = size[0] - self.single_window_size[0], self.single_window_size[1]
            self.multi_window_pos = self.single_window_size[0], 0
            if isSupport:
                char = preview.support
            else:
                char = preview.char
            self.single = SinglePreview(main_screen, preview, self.single_window_size, self.single_window_pos, self.slot_size, char, isSupport)
        else:
            self.single_window_size = (0, 0)
            self.single = None
            self.multi_window_size = size[0], size[1] * .85
            self.multi_window_pos = 0, 0

        self.scroll = ScrollPreview(main_screen, preview, self.multi_window_size, self.multi_window_pos, self.slot_size, characters, isSupport)
        self.grid = GridPreview(main_screen, preview, self.multi_window_size, self.multi_window_pos, self.grid_size, characters, isSupport)

        self.sort = SortWidget(size=self.size, pos=self.pos)
        self.sort.ascending.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Ascending'))
        self.sort.descending.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Descending'))
        self.sort.strength.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Strength'))
        self.sort.magic.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Magic'))
        self.sort.endurance.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Endurance'))
        self.sort.dexterity.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Dexterity'))
        self.sort.agility.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Agility'))
        self.sort.health.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Health'))
        self.sort.mana.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Mana'))
        self.sort.phyatk.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Phy. Atk'))
        self.sort.magatk.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Mag. Atk'))
        self.sort.defense.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Defense'))
        self.sort.party.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Party'))
        self.sort.rank.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Rank'))
        self.sort.name.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Name'))
        self.sort.score.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Score'))
        self.sort.worth.bind(on_touch_down=lambda instance, touch: self.do_sort(instance, touch, 'Worth'))

        self.filter = FilterWidget(size=self.size, pos=self.pos)

        self.filter.filter_button.bind(on_touch_down=self.do_filter)
        self.filter.magical.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_magical'))
        self.filter.physical.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_physical'))
        self.filter.balanced.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_balanced'))
        self.filter.defensive.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_defensive'))
        self.filter.healing.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_healing'))
        self.filter.light.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_light'))
        self.filter.dark.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_dark'))
        self.filter.earth.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_earth'))
        self.filter.wind.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_wind'))
        self.filter.thunder.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_thunder'))
        self.filter.fire.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_fire'))
        self.filter.water.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'type_water'))
        self.filter.rank_1.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_1'))
        self.filter.rank_2.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_2'))
        self.filter.rank_3.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_3'))
        self.filter.rank_4.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_4'))
        self.filter.rank_5.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_5'))
        self.filter.rank_6.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_6'))
        self.filter.rank_7.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_7'))
        self.filter.rank_8.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_8'))
        self.filter.rank_9.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_9'))
        self.filter.rank_10.bind(on_touch_down=lambda instance, touch: self.modify_filter(instance, touch, 'rank_10'))

        button_size = size[0] * 0.075 * 570 / 215, size[1] * 0.075
        self.toggle_button = HTButton(size=button_size, pos=((size[0] - button_size[0] * 3) * 3 / 4 + button_size[0] * 2, size[1] * 0.8875), size_hint=(None, None), color=(0,0,0,1), border=[0, 0, 0, 0], text="Switch Display", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", path='../res/screens/buttons/long_stat', toggle_enabled=True, on_state_one=self.on_scroll, on_state_two=self.on_grid, background_disabled_normal_use=True)
        self.sort_button = HTButton(size=button_size, pos=((size[0] - button_size[0] * 3) * 1 / 4, size[1] * 0.8875), size_hint=(None, None), color=(0,0,0,1), border=[0, 0, 0, 0], text=self.grid.sort_type, font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", path='../res/screens/buttons/long_stat', on_touch_down=self.on_sort)
        self.filter_button = HTButton(size=button_size, pos=((size[0] - button_size[0] * 3) * 2 / 4 + button_size[0], size[1] * 0.8875), size_hint=(None, None), color=(0,0,0,1), border=[0,0,0,0], text="Filter", font_size=button_size[1] * 0.5, font_name="../res/fnt/Gabriola.ttf", path="../res/screens/buttons/long_stat", on_touch_down=self.on_filter)

        self.add_widget(self.background)
        if has_left:
            self.add_widget(self.single)

        if self.toggle:
            self.add_widget(self.grid)
        else:
            self.add_widget(self.scroll)

        self.add_widget(self.sort_button)
        self.add_widget(self.filter_button)
        self.add_widget(self.toggle_button)

        if self.single is not None:
            self.single.reload()

    def reload(self):
        pass

    def on_scroll(self, instance):
        if not instance.disabled:
            self.remove_widget(self.grid)
            self.add_widget(self.scroll)

    def on_grid(self, instance):
        if not instance.disabled:
            self.remove_widget(self.scroll)
            self.add_widget(self.grid)

    def on_sort(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.toggle_button.do_hover = False
            self.toggle_button.disabled = True
            for preview in self.grid.previews_sort:
                preview.char_button.do_hover = False
            for preview in self.scroll.previews_sort:
                preview.char_button.do_hover = False
            self.add_widget(self.sort)

    def do_sort(self, instance, touch, type):
        if instance.collide_point(*touch.pos):
            if type == 'Ascending':
                self.grid.ascending = True
                self.scroll.ascending = True
            elif type == 'Descending':
                self.grid.ascending = False
                self.scroll.ascending = False
            else:
                self.sort_button.text = type
                self.grid.sort_type = type
                self.scroll.sort_type = type
            self.toggle_button.do_hover = True
            self.toggle_button.disabled = False
            for preview in self.grid.previews_sort:
                preview.char_button.do_hover = True
            for preview in self.scroll.previews_sort:
                preview.char_button.do_hover = True
            self.remove_widget(self.sort)

    def on_filter(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.toggle_button.do_hover = False
            self.toggle_button.disabled = True
            for preview in self.grid.previews_sort:
                preview.char_button.do_hover = False
            for preview in self.scroll.previews_sort:
                preview.char_button.do_hover = False
            self.add_widget(self.filter)

    def modify_filter(self, instance, touch, filter):
        if instance.collide_point(*touch.pos):
            if filter in self.grid.filters_applied:
                self.grid.filters_applied.remove(filter)
                self.scroll.filters_applied.remove(filter)
            else:
                self.grid.filters_applied.append(filter)
                self.scroll.filters_applied.append(filter)

    def do_filter(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.grid.filter()
            self.scroll.filter()
            self.toggle_button.do_hover = True
            self.toggle_button.disabled = False
            for preview in self.grid.previews_sort:
                preview.char_button.do_hover = True
            for preview in self.scroll.previews_sort:
                preview.char_button.do_hover = True
            self.remove_widget(self.filter)