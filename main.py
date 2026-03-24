from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.card import MDCard
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
import os
import subprocess
import threading
import time
import json
import random

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
#  KV LAYOUT
# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
KV = '''
#:import MDRaisedButton kivymd.uix.button.MDRaisedButton
#:import MDFlatButton  kivymd.uix.button.MDFlatButton

<FloatingButton>:
    size_hint: None, None
    size: "56dp", "56dp"
    md_bg_color: app.accent
    radius: [28,]
    elevation: 8
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10_000_000
    on_release: app.open_menu()

    MDIcon:
        icon: "hexagon-outline"
        pos_hint: {"center_x": .5, "center_y": .5}
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_size: "26sp"

MDScreen:
    md_bg_color: 0, 0, 0, 0

    # \u2500\u2500 MAIN MENU \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    MDCard:
        id: main_menu
        orientation: "vertical"
        size_hint: None, None
        size: "320dp", "560dp"
        pos_hint: {"center_x": .5, "center_y": -2}
        md_bg_color: 0.08, 0.08, 0.12, 0.97
        radius: [24,]
        padding: "16dp"
        spacing: "6dp"
        elevation: 12

        # Header
        MDBoxLayout:
            adaptive_height: True
            padding: "4dp", "0dp"

            MDLabel:
                text: "\u2b21  MACHINE CORE"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: app.accent
                size_hint_x: 1

            MDIconButton:
                icon: "close"
                theme_text_color: "Custom"
                text_color: 0.5, 0.5, 0.5, 1
                on_release: app.close_menu()

        MDSeparator:
            color: app.accent

        # Scrollable feature list
        ScrollView:
            do_scroll_x: False
            size_hint_y: 1

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "4dp"
                padding: "4dp", "4dp"

                # 1 AdBlock
                FeatureRow:
                    label_text: "System AdBlock"
                    icon_name: "shield-check"
                    on_toggle: app.toggle_adblock(*args)

                # 2 Screen translator
                FeatureRow:
                    label_text: "Screen Translator (OCR)"
                    icon_name: "translate"
                    on_toggle: app.toggle_translator(*args)

                # 3 FPS Boost
                FeatureRow:
                    label_text: "FPS Boost (Governor)"
                    icon_name: "speedometer"
                    on_toggle: app.toggle_fps_boost(*args)

                # 4 No-Clip mode (overlay)
                FeatureRow:
                    label_text: "Always on Top"
                    icon_name: "layers-triple"
                    on_toggle: app.toggle_always_on_top(*args)

                # 5 Auto-Clicker
                FeatureRow:
                    label_text: "Auto Clicker"
                    icon_name: "gesture-tap"
                    on_toggle: app.toggle_auto_clicker(*args)

                # 6 Touch Grid (aim grid)
                FeatureRow:
                    label_text: "Aim Grid Overlay"
                    icon_name: "crosshairs-gps"
                    on_toggle: app.toggle_aim_grid(*args)

                # 7 DPI Changer
                FeatureRow:
                    label_text: "High DPI Mode"
                    icon_name: "dots-grid"
                    on_toggle: app.toggle_dpi(*args)

                # 8 RAM Cleaner
                FeatureRow:
                    label_text: "RAM Cleaner (Auto)"
                    icon_name: "memory"
                    on_toggle: app.toggle_ram_cleaner(*args)

                # 9 Battery Saver
                FeatureRow:
                    label_text: "Battery Saver Mode"
                    icon_name: "battery-heart"
                    on_toggle: app.toggle_battery_saver(*args)

                # 10 Network Spoof
                FeatureRow:
                    label_text: "Network Ping Reducer"
                    icon_name: "wifi-strength-4"
                    on_toggle: app.toggle_ping_reducer(*args)

                # 11 Screen Recorder
                FeatureRow:
                    label_text: "Screen Recorder"
                    icon_name: "record-circle"
                    on_toggle: app.toggle_screen_recorder(*args)

                # 12 Gyroscope Lock
                FeatureRow:
                    label_text: "Gyro