from kivy.config import Config
# Важно: эти настройки должны быть в самом верху
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'multisamples', '0')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.card import MDCard
from kivy.properties import BooleanProperty
from kivy.animation import Animation
from kivy.core.window import Window
import os

# Пытаемся сделать фон прозрачным на уровне движка
Window.clearcolor = (0, 0, 0, 0)

KV = '''
<FloatingButton>:
    size_hint: None, None
    size: "56dp", "56dp"
    md_bg_color: 0, 0.5, 1, 1
    radius: [28, ]
    elevation: 4
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    on_release: app.open_menu()
    
    MDIcon:
        icon: "cpu-64-bit"
        pos_hint: {"center_x": .5, "center_y": .5}
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1

MDScreen:
    md_bg_color: 0, 0, 0, 0 

    # Миниатюрное Меню
    MDCard:
        id: main_menu
        orientation: "vertical"
        size_hint: None, None
        size: "240dp", "280dp"
        pos_hint: {"center_x": .5, "center_y": -1} 
        md_bg_color: 0.05, 0.05, 0.05, 0.95
        radius: [24, ]
        padding: "12dp"
        spacing: "8dp"
        line_color: 0, 0.5, 1, 0.3
        line_width: 1.2
        elevation: 8

        MDLabel:
            text: "MACHINE"
            font_style: "Button"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0.6, 1, 1
            adaptive_height: True

        MDSeparator:
            color: 0, 0.5, 1, 0.2

        # Пункты меню стали компактнее
        MDBoxLayout:
            adaptive_height: True
            padding: [10, 0]
            MDLabel:
                text: "AdBlock Core"
                font_style: "Caption"
                theme_text_color: "Secondary"
            MDSwitch:
                width: "40dp"
                on_active: app.toggle_adblock(*args)

        MDBoxLayout:
            adaptive_height: True
            padding: [10, 0]
            MDLabel:
                text: "Live Translate"
                font_style: "Caption"
                theme_text_color: "Secondary"
            MDSwitch:
                width: "40dp"
                on_active: app.toggle_translator(*args)

        Widget: # Распорка

        MDRoundFlatButton:
            text: "CLOSE"
            text_color: 1, 1, 1, 0.8
            line_color: 0, 0.5, 1, 0.5
            pos_hint: {"center_x": .5}
            on_release: app.close_menu()

    # Плавающая кнопка
    FloatingButton:
        id: float_btn
        x: 20
        y: 400
'''

class FloatingButton(DragBehavior, MDCard):
    pass

class MachineApp(MDApp):
    menu_open = BooleanProperty(False)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def open_menu(self):
        if not self.menu_open:
            # Плавное появление из центра
            anim = Animation(pos_hint={"center_x": .5, "center_y": .5}, duration=0.4, t='out_expo')
            anim_btn = Animation(opacity=0, scale=0.5, duration=0.2)
            anim.start(self.root.ids.main_menu)
            anim_btn.start(self.root.ids.float_btn)
            self.menu_open = True

    def close_menu(self):
        if self.menu_open:
            # Уход вниз
            anim = Animation(pos_hint={"center_x": .5, "center_y": -1}, duration=0.3, t='in_back')
            anim_btn = Animation(opacity=1, scale=1, duration=0.2)
            anim.start(self.root.ids.main_menu)
            anim_btn.start(self.root.ids.float_btn)
            self.menu_open = False

    def toggle_adblock(self, sw, val):
        # Добавил проверку, чтобы приложение не падало, если su недоступен
        try:
            if val: os.system("su -c 'echo \"0.0.0.0 ads.google.com\" >> /etc/hosts'")
            else: os.system("su -c 'sed -i \"/ads.google.com/d\" /etc/hosts'")
        except Exception as e:
            print(f"Root error: {e}")

    def toggle_translator(self, sw, val):
        pass

if __name__ == '__main__':
    MachineApp().run()
