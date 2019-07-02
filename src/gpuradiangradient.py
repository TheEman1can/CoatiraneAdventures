from itertools import chain

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture


class MyWidget(Widget):
    def __init__(self, **args):
        super(MyWidget, self).__init__(**args)

        self.texture = Texture.create(size=(5, 1), colorfmt="rgb")
        pixels = bytes([int(v * 255) for v in chain((0, 0, 0, 1), (0, 0, 0, 1))])
        buf = ''.join(pixels)
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(pos=self.pos, size=self.size, texture=self.texture)


class TestApp(App):
    def build(self):
        return MyWidget(size=(368, 512))


if __name__ == '__main__':
    TestApp().run()