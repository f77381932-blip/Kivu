import os
import subprocess
import threading
import time
import random

from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.card import MDCard
from kivy.properties import (BooleanProperty, StringProperty,
                              NumericProperty, ListProperty, ObjectProperty)
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, RoundedRectangle, Ellipse


# ─────────────────────────────────────────────────────────────────────────────
#  KV LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
KV = '''
#:import Animation kivy.animation.Animation

# ── Draggable FAB ─────────────────────────────────────────────────────────────
<FloatingButton>:
    size_hint: None, None
    size: "60dp", "60dp"
    md_bg_color: app.accent
    radius: [30,]
    elevation: 16
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10_000_000
    on_release: app.open_menu()

    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: None, None
        size: "40dp", "40dp"

        MDIcon:
            id: fab_icon
            icon: "hexagon-outline"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_size: "28sp"
            halign: "center"

# ── Category header ──────────────────────────────────────────────────────────
<CatHeader@MDBoxLayout>:
    cat_label: ""
    cat_icon: "label"
    adaptive_height: True
    padding: "4dp", "8dp", "4dp", "2dp"
    spacing: "6dp"

    MDIcon:
        icon: root.cat_icon
        theme_text_color: "Custom"
        text_color: app.accent[0], app.accent[1], app.accent[2], 0.7
        font_size: "16sp"
        size_hint_x: None
        width: "20dp"

    MDLabel:
        text: root.cat_label.upper()
        font_style: "Overline"
        theme_text_color: "Custom"
        text_color: app.accent[0], app.accent[1], app.accent[2], 0.7
        size_hint_x: 1

    MDSeparator:
        color: app.accent[0], app.accent[1], app.accent[2], 0.2

# ── Feature row ───────────────────────────────────────────────────────────────
<FeatureRow@MDBoxLayout>:
    adaptive_height: True
    spacing: "10dp"
    padding: "6dp", "5dp"
    label_text: ""
    icon_name: "checkbox-blank-circle-outline"
    __events__: ("on_toggle",)
    on_toggle: pass

    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.03
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8,]

    MDIcon:
        icon: root.icon_name
        theme_text_color: "Custom"
        text_color: app.accent
        size_hint_x: None
        width: "28dp"
        font_size: "20sp"

    MDLabel:
        text: root.label_text
        theme_text_color: "Custom"
        text_color: 0.88, 0.88, 0.95, 1
        font_style: "Body2"
        size_hint_x: 1

    MDSwitch:
        size_hint_x: None
        width: "52dp"
        on_active: root.dispatch("on_toggle", self.active)
        thumb_color_active: app.accent
        track_color_active: app.accent[0]*0.4, app.accent[1]*0.4, app.accent[2]*0.4, 1

# ─────────────────────────────────────────────────────────────────────────────
MDScreen:
    md_bg_color: 0, 0, 0, 0

    # ── MAIN PANEL ──────────────────────────────────────────────────────────
    MDCard:
        id: main_menu
        orientation: "vertical"
        size_hint: None, None
        size: "340dp", "600dp"
        pos_hint: {"center_x": .5, "center_y": -2}
        md_bg_color: 0.05, 0.05, 0.09, 0.97
        radius: [28,]
        padding: "14dp", "14dp", "14dp", "10dp"
        spacing: "4dp"
        elevation: 20

        # ── HEADER ──────────────────────────────────────────────────────────
        MDBoxLayout:
            adaptive_height: True
            padding: "2dp", "0dp"
            spacing: "8dp"

            # Neon hex icon
            MDBoxLayout:
                size_hint: None, None
                size: "36dp", "36dp"
                md_bg_color: app.accent[0]*0.15, app.accent[1]*0.15, app.accent[2]*0.15, 1
                radius: [10,]

                MDIcon:
                    icon: "hexagon-slice-6"
                    theme_text_color: "Custom"
                    text_color: app.accent
                    font_size: "22sp"
                    pos_hint: {"center_x": .5, "center_y": .5}

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                size_hint_x: 1
                spacing: "0dp"
                padding: "2dp", "0dp"

                MDLabel:
                    text: "MACHINE CORE"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: app.accent
                    bold: True

                MDLabel:
                    id: version_lbl
                    text: "v2.0  ·  25 modules"
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0.4, 0.4, 0.5, 1

            MDIconButton:
                icon: "close-circle-outline"
                theme_text_color: "Custom"
                text_color: 0.4, 0.4, 0.5, 1
                on_release: app.close_menu()

        # thin neon divider
        MDBoxLayout:
            size_hint_y: None
            height: "2dp"
            md_bg_color: app.accent[0], app.accent[1], app.accent[2], 0.6
            radius: [1,]

        # ── SCROLL AREA ─────────────────────────────────────────────────────
        ScrollView:
            do_scroll_x: False
            size_hint_y: 1
            bar_width: "3dp"
            bar_color: app.accent[0], app.accent[1], app.accent[2], 0.5

            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                spacing: "2dp"
                padding: "2dp", "4dp"

                # ── PERFORMANCE ─────────────────────────────────────────────
                CatHeader:
                    cat_label: "Performance"
                    cat_icon: "rocket-launch"

                FeatureRow:
                    label_text: "FPS Boost (CPU Governor)"
                    icon_name: "speedometer"
                    on_toggle: app.toggle_fps_boost(*args)

                FeatureRow:
                    label_text: "RAM Cleaner (Auto 30s)"
                    icon_name: "memory"
                    on_toggle: app.toggle_ram_cleaner(*args)

                FeatureRow:
                    label_text: "Thermal Throttle Guard"
                    icon_name: "thermometer-off"
                    on_toggle: app.toggle_thermal(*args)

                FeatureRow:
                    label_text: "High DPI Mode"
                    icon_name: "dots-grid"
                    on_toggle: app.toggle_dpi(*args)

                # ── GAMING ──────────────────────────────────────────────────
                CatHeader:
                    cat_label: "Gaming"
                    cat_icon: "gamepad-variant"

                FeatureRow:
                    label_text: "Auto Clicker (12 CPS)"
                    icon_name: "gesture-tap"
                    on_toggle: app.toggle_auto_clicker(*args)

                FeatureRow:
                    label_text: "Aim Grid Overlay"
                    icon_name: "crosshairs-gps"
                    on_toggle: app.toggle_aim_grid(*args)

                FeatureRow:
                    label_text: "Custom Crosshair"
                    icon_name: "plus-circle-outline"
                    on_toggle: app.toggle_crosshair(*args)

                FeatureRow:
                    label_text: "Recoil Stabiliser"
                    icon_name: "target"
                    on_toggle: app.toggle_recoil(*args)

                FeatureRow:
                    label_text: "Loot Highlight Filter"
                    icon_name: "star-circle"
                    on_toggle: app.toggle_loot_highlight(*args)

                FeatureRow:
                    label_text: "Minimap Enhancer"
                    icon_name: "map-marker"
                    on_toggle: app.toggle_minimap(*args)

                FeatureRow:
                    label_text: "Macro Player"
                    icon_name: "play-circle"
                    on_toggle: app.toggle_macro(*args)

                FeatureRow:
                    label_text: "Magnifier Zone"
                    icon_name: "magnify-plus"
                    on_toggle: app.toggle_magnifier(*args)

                # ── DISPLAY ─────────────────────────────────────────────────
                CatHeader:
                    cat_label: "Display"
                    cat_icon: "monitor-eye"

                FeatureRow:
                    label_text: "Color Blind Mode"
                    icon_name: "eye-settings"
                    on_toggle: app.toggle_colorblind(*args)

                FeatureRow:
                    label_text: "Touch Visualizer"
                    icon_name: "gesture"
                    on_toggle: app.toggle_touch_vis(*args)

                FeatureRow:
                    label_text: "Always on Top"
                    icon_name: "layers-triple"
                    on_toggle: app.toggle_always_on_top(*args)

                # ── SYSTEM ──────────────────────────────────────────────────
                CatHeader:
                    cat_label: "System"
                    cat_icon: "cog-outline"

                FeatureRow:
                    label_text: "System AdBlock"
                    icon_name: "shield-check"
                    on_toggle: app.toggle_adblock(*args)

                FeatureRow:
                    label_text: "Network Ping Reducer"
                    icon_name: "wifi-strength-4"
                    on_toggle: app.toggle_ping_reducer(*args)

                FeatureRow:
                    label_text: "Battery Saver Mode"
                    icon_name: "battery-heart"
                    on_toggle: app.toggle_battery_saver(*args)

                FeatureRow:
                    label_text: "Mute Notifications"
                    icon_name: "bell-off"
                    on_toggle: app.toggle_notif_mute(*args)

                FeatureRow:
                    label_text: "Gyro Lock (no drift)"
                    icon_name: "rotate-3d-variant"
                    on_toggle: app.toggle_gyro_lock(*args)

                FeatureRow:
                    label_text: "Volume Boost (+20%)"
                    icon_name: "volume-high"
                    on_toggle: app.toggle_volume_boost(*args)

                FeatureRow:
                    label_text: "Screen Translator (OCR)"
                    icon_name: "translate"
                    on_toggle: app.toggle_translator(*args)

                # ── CAPTURE ─────────────────────────────────────────────────
                CatHeader:
                    cat_label: "Capture"
                    cat_icon: "camera-outline"

                FeatureRow:
                    label_text: "Screen Recorder"
                    icon_name: "record-circle"
                    on_toggle: app.toggle_screen_recorder(*args)

                FeatureRow:
                    label_text: "Quick Screenshot (5s)"
                    icon_name: "camera"
                    on_toggle: app.toggle_screenshot_mode(*args)

                # ── EMERGENCY ───────────────────────────────────────────────
                CatHeader:
                    cat_label: "Emergency"
                    cat_icon: "alert-octagon"

                FeatureRow:
                    label_text: "PANIC / Kill Switch"
                    icon_name: "alert-octagon"
                    on_toggle: app.toggle_panic(*args)

        # ── STATUS BAR ──────────────────────────────────────────────────────
        MDBoxLayout:
            size_hint_y: None
            height: "2dp"
            md_bg_color: 0.1, 0.1, 0.15, 1

        MDBoxLayout:
            adaptive_height: True
            padding: "6dp", "4dp"
            spacing: "6dp"

            MDIcon:
                id: status_icon
                icon: "circle-medium"
                theme_text_color: "Custom"
                text_color: app.status_color
                font_size: "18sp"
                size_hint_x: None
                width: "20dp"

            MDLabel:
                id: status_label
                text: app.status_text
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: app.status_color
                size_hint_x: 1

    # ── FAB ─────────────────────────────────────────────────────────────────
    FloatingButton:
        id: float_btn
        x: dp(20)
        y: dp(300)

    # ── AIM GRID ────────────────────────────────────────────────────────────
    Widget:
        id: aim_grid
        opacity: 0
        canvas:
            Color:
                rgba: 1, 0.1, 0.1, 0.4
            Line:
                points: [0, root.height/2, root.width, root.height/2]
                width: 1.2
            Line:
                points: [root.width/2, 0, root.width/2, root.height]
                width: 1.2
            Color:
                rgba: 1, 0.1, 0.1, 0.18
            Line:
                points: [0, root.height*0.333, root.width, root.height*0.333]
                width: 0.8
            Line:
                points: [0, root.height*0.667, root.width, root.height*0.667]
                width: 0.8
            Line:
                points: [root.width*0.333, 0, root.width*0.333, root.height]
                width: 0.8
            Line:
                points: [root.width*0.667, 0, root.width*0.667, root.height]
                width: 0.8

    # ── CROSSHAIR ───────────────────────────────────────────────────────────
    Widget:
        id: crosshair
        opacity: 0
        canvas:
            Color:
                rgba: 0, 1, 0.5, 0.95
            Line:
                circle: root.width/2, root.height/2, 20
                width: 1.8
            Line:
                circle: root.width/2, root.height/2, 4
                width: 1.2
            Color:
                rgba: 0, 1, 0.5, 0.85
            Line:
                points: [root.width/2-32, root.height/2, root.width/2-8, root.height/2]
                width: 2
            Line:
                points: [root.width/2+8, root.height/2, root.width/2+32, root.height/2]
                width: 2
            Line:
                points: [root.width/2, root.height/2+8, root.width/2, root.height/2+32]
                width: 2
            Line:
                points: [root.width/2, root.height/2-32, root.width/2, root.height/2-8]
                width: 2
'''


# ─────────────────────────────────────────────────────────────────────────────
#  CUSTOM WIDGETS
# ─────────────────────────────────────────────────────────────────────────────
class FloatingButton(DragBehavior, MDCard):
    pass


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class MachineApp(MDApp):
    menu_open    = BooleanProperty(False)
    status_text  = StringProperty("MACHINE CORE  ·  READY")
    status_color = ListProperty([0.25, 0.9, 0.5, 1])
    accent       = ListProperty([0.0, 0.6, 1.0, 1])

    _auto_click_event = None
    _ram_clean_event  = None
    _recorder_proc    = None
    _recoil_event     = None
    _macro_event      = None
    _ss_event         = None
    _pulse_event      = None
    _macro_step       = 0
    _macro_sequence   = [
        "input tap 540 960",
        "input swipe 200 800 600 800 150",
        "input tap 540 500",
        "input keyevent 4",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

    # ── build ────────────────────────────────────────────────────────────────
    def build(self):
        root = Builder.load_string(KV)
        # Start FAB pulse animation
        Clock.schedule_once(self._start_fab_pulse, 1)
        return root

    # ── FAB pulse ────────────────────────────────────────────────────────────
    def _start_fab_pulse(self, dt):
        self._pulse_event = Clock.schedule_interval(self._pulse_fab, 2.5)

    def _pulse_fab(self, dt):
        btn = self.root.ids.float_btn
        (Animation(md_bg_color=[0.1, 0.7, 1, 1], duration=0.4, t="out_sine") +
         Animation(md_bg_color=self.accent,        duration=0.4, t="in_sine")
         ).start(btn)

    # ── menu animation ───────────────────────────────────────────────────────
    def open_menu(self):
        if not self.menu_open:
            Animation(
                pos_hint={"center_x": .5, "center_y": .5},
                duration=0.4, t="out_back"
            ).start(self.root.ids.main_menu)
            Animation(opacity=0, duration=0.15).start(self.root.ids.float_btn)
            self.menu_open = True

    def close_menu(self):
        if self.menu_open:
            Animation(
                pos_hint={"center_x": .5, "center_y": -2},
                duration=0.3, t="in_back"
            ).start(self.root.ids.main_menu)
            Animation(opacity=1, duration=0.25).start(self.root.ids.float_btn)
            self.menu_open = False

    # ── helpers ──────────────────────────────────────────────────────────────
    def _su(self, cmd):
        try:
            subprocess.Popen(
                f"su -c '{cmd}'", shell=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception as e:
            self._set_status(f"root err: {e}", error=True)

    def _set_status(self, msg, error=False, warn=False):
        self.status_text = msg
        if error:
            self.status_color = [1.0, 0.3, 0.3, 1]
        elif warn:
            self.status_color = [1.0, 0.75, 0.1, 1]
        else:
            self.status_color = [0.25, 0.9, 0.5, 1]

    # ═══════════════════════════════════════════════════════════════════════
    #  25 FEATURES
    # ═══════════════════════════════════════════════════════════════════════

    # 1 ── AdBlock ─────────────────────────────────────────────────────────
    def toggle_adblock(self, val):
        if val:
            self._su(
                "echo '0.0.0.0 ads.google.com' >> /etc/hosts && "
                "echo '0.0.0.0 googleads.g.doubleclick.net' >> /etc/hosts && "
                "echo '0.0.0.0 pagead2.googlesyndication.com' >> /etc/hosts && "
                "echo '0.0.0.0 doubleclick.net' >> /etc/hosts"
            )
            self._set_status("AdBlock  ▶  ON")
        else:
            self._su("sed -i '/0\\.0\\.0\\.0/d' /etc/hosts")
            self._set_status("AdBlock  ■  OFF")

    # 2 ── OCR Translator ──────────────────────────────────────────────────
    def toggle_translator(self, val):
        if val:
            self._su("am startservice -n com.google.android.apps.translate/.TranslateService")
            self._set_status("Translator  ▶  ON")
        else:
            self._su("am stopservice -n com.google.android.apps.translate/.TranslateService")
            self._set_status("Translator  ■  OFF")

    # 3 ── FPS / CPU Governor ──────────────────────────────────────────────
    def toggle_fps_boost(self, val):
        gov = "performance" if val else "schedutil"
        self._su(
            f"for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; "
            f"do echo {gov} > $f 2>/dev/null; done"
        )
        self._set_status(f"CPU → {gov.upper()}", warn=val)

    # 4 ── Always on Top ───────────────────────────────────────────────────
    def toggle_always_on_top(self, val):
        self._su(f"settings put system always_on_top {'1' if val else '0'}")
        self._set_status(f"Always on Top  {'▶  ON' if val else '■  OFF'}")

    # 5 ── Auto Clicker ────────────────────────────────────────────────────
    def toggle_auto_clicker(self, val):
        if val:
            self._auto_click_event = Clock.schedule_interval(
                self._do_auto_click, 0.083)
            self._set_status("Auto Clicker  ▶  12 CPS", warn=True)
        else:
            if self._auto_click_event:
                self._auto_click_event.cancel()
                self._auto_click_event = None
            self._set_status("Auto Clicker  ■  OFF")

    def _do_auto_click(self, dt):
        w = Window.width  // 2
        h = Window.height // 2
        self._su(f"input tap {w} {h}")

    # 6 ── Aim Grid ────────────────────────────────────────────────────────
    def toggle_aim_grid(self, val):
        target_op = 1 if val else 0
        Animation(opacity=target_op, duration=0.25).start(self.root.ids.aim_grid)
        self._set_status(f"Aim Grid  {'▶  ON' if val else '■  OFF'}")

    # 7 ── High DPI ────────────────────────────────────────────────────────
    def toggle_dpi(self, val):
        self._su(f"wm density {'480' if val else '0'}")
        self._set_status(f"DPI  →  {'480 (High)' if val else 'Default'}", warn=val)

    # 8 ── RAM Cleaner ─────────────────────────────────────────────────────
    def toggle_ram_cleaner(self, val):
        if val:
            self._ram_clean_event = Clock.schedule_interval(
                lambda dt: self._su("sync && echo 3 > /proc/sys/vm/drop_caches"), 30)
            self._set_status("RAM Cleaner  ▶  every 30s")
        else:
            if self._ram_clean_event:
                self._ram_clean_event.cancel()
                self._ram_clean_event = None
            self._set_status("RAM Cleaner  ■  OFF")

    # 9 ── Battery Saver ───────────────────────────────────────────────────
    def toggle_battery_saver(self, val):
        self._su(f"settings put global low_power {'1' if val else '0'}")
        self._set_status(f"Battery Saver  {'▶  ON' if val else '■  OFF'}")

    # 10 ── Ping Reducer ───────────────────────────────────────────────────
    def toggle_ping_reducer(self, val):
        if val:
            self._su(
                "settings put global wifi_scan_throttle_enabled 0 && "
                "settings put global wifi_sleep_policy 2"
            )
            self._set_status("Ping Reducer  ▶  ON")
        else:
            self._su(
                "settings put global wifi_scan_throttle_enabled 1 && "
                "settings put global wifi_sleep_policy 0"
            )
            self._set_status("Ping Reducer  ■  OFF")

    # 11 ── Screen Recorder ────────────────────────────────────────────────
    def toggle_screen_recorder(self, val):
        if val:
            out = "/sdcard/MC_record.mp4"
            self._recorder_proc = subprocess.Popen(
                f"su -c 'screenrecord --verbose {out}'", shell=True)
            self._set_status("● REC  →  /sdcard/MC_record.mp4", warn=True)
        else:
            if self._recorder_proc:
                self._recorder_proc.terminate()
                self._recorder_proc = None
            self._set_status("Recording saved  ✓")

    # 12 ── Gyro Lock ──────────────────────────────────────────────────────
    def toggle_gyro_lock(self, val):
        self._su(f"settings put system accelerometer_rotation {'0' if val else '1'}")
        self._set_status(f"Gyro Lock  {'▶  ON' if val else '■  OFF'}")

    # 13 ── Volume Boost ───────────────────────────────────────────────────
    def toggle_volume_boost(self, val):
        self._su(f"media volume --stream 3 --set {'15' if val else '10'}")
        self._set_status(f"Volume  →  {'MAX (15)' if val else 'Normal (10)'}", warn=val)

    # 14 ── Notification Mute ─────────────────────────────────────────────
    def toggle_notif_mute(self, val):
        self._su(f"settings put global zen_mode {'2' if val else '0'}")
        self._set_status(f"Notifications  {'MUTED ▶' if val else 'NORMAL ■'}")

    # 15 ── Macro Player ───────────────────────────────────────────────────
    def toggle_macro(self, val):
        if val:
            self._macro_event = Clock.schedule_interval(self._run_macro_step, 1.5)
            self._macro_step = 0
            self._set_status("Macro  ▶  RUNNING", warn=True)
        else:
            if self._macro_event:
                self._macro_event.cancel()
                self._macro_event = None
            self._set_status("Macro  ■  STOPPED")

    def _run_macro_step(self, dt):
        cmd = self._macro_sequence[self._macro_step % len(self._macro_sequence)]
        self._su(cmd)
        self._macro_step += 1

    # 16 ── Custom Crosshair ──────────────────────────────────────────────
    def toggle_crosshair(self, val):
        target_op = 1 if val else 0
        Animation(opacity=target_op, duration=0.2).start(self.root.ids.crosshair)
        self._set_status(f"Crosshair  {'▶  ON' if val else '■  OFF'}")

    # 17 ── Thermal Throttle Guard ─────────────────────────────────────────
    def toggle_thermal(self, val):
        if val:
            self._su(
                "setprop persist.vendor.thermal.config '' && "
                "stop thermal-engine 2>/dev/null; stop thermald 2>/dev/null"
            )
            self._set_status("Thermal Guard  ▶  ON  ⚠ may heat", warn=True)
        else:
            self._su("start thermal-engine 2>/dev/null; start thermald 2>/dev/null")
            self._set_status("Thermal Guard  ■  OFF")

    # 18 ── Touch Visualiser ───────────────────────────────────────────────
    def toggle_touch_vis(self, val):
        f = "1" if val else "0"
        self._su(
            f"settings put system show_touches {f} && "
            f"settings put system pointer_location {f}"
        )
        self._set_status(f"Touch Vis  {'▶  ON' if val else '■  OFF'}")

    # 19 ── Quick Screenshot ───────────────────────────────────────────────
    def toggle_screenshot_mode(self, val):
        if val:
            self._ss_event = Clock.schedule_interval(self._take_screenshot, 5)
            self._set_status("Screenshot  ▶  every 5s", warn=True)
        else:
            if self._ss_event:
                self._ss_event.cancel()
                self._ss_event = None
            self._set_status("Screenshot mode  ■  OFF")

    def _take_screenshot(self, dt):
        stamp = int(time.time())
        self._su(f"screencap -p /sdcard/MC_shot_{stamp}.png")

    # 20 ── Magnifier Zone ─────────────────────────────────────────────────
    def toggle_magnifier(self, val):
        self._su(
            f"settings put secure "
            f"accessibility_display_magnification_enabled {'1' if val else '0'}"
        )
        self._set_status(f"Magnifier  {'▶  ON' if val else '■  OFF'}")

    # 21 ── Loot Highlight ─────────────────────────────────────────────────
    def toggle_loot_highlight(self, val):
        if val:
            self._su(
                "service call SurfaceFlinger 1023 i32 1 "
                "f 1.8 f 0 f 0 f 0 f 1.8 f 0 f 0 f 0 f 1.8 2>/dev/null"
            )
            self._set_status("Loot Highlight  ▶  +saturation", warn=True)
        else:
            self._su(
                "service call SurfaceFlinger 1023 i32 1 "
                "f 1 f 0 f 0 f 0 f 1 f 0 f 0 f 0 f 1 2>/dev/null"
            )
            self._set_status("Loot Highlight  ■  OFF")

    # 22 ── Minimap Enhancer ───────────────────────────────────────────────
    def toggle_minimap(self, val):
        if val:
            self._su(
                "settings put system screen_brightness_mode 0 && "
                "settings put system screen_brightness 220"
            )
            self._set_status("Minimap Enhancer  ▶  ON")
        else:
            self._su("settings put system screen_brightness_mode 1")
            self._set_status("Minimap Enhancer  ■  auto-bright")

    # 23 ── Recoil Stabiliser ──────────────────────────────────────────────
    def toggle_recoil(self, val):
        if val:
            cx = Window.width  // 2
            cy = Window.height // 2
            self._recoil_event = Clock.schedule_interval(
                lambda dt: self._su(
                    f"input swipe {cx} {cy} {cx} {cy+5} 30"), 0.05)
            self._set_status("Recoil Stabiliser  ▶  ON", warn=True)
        else:
            if self._recoil_event:
                self._recoil_event.cancel()
                self._recoil_event = None
            self._set_status("Recoil Stabiliser  ■  OFF")

    # 24 ── Color Blind Mode ───────────────────────────────────────────────
    def toggle_colorblind(self, val):
        self._su(
            f"settings put secure accessibility_display_daltonizer {'12' if val else '0'} && "
            f"settings put secure accessibility_display_daltonizer_enabled {'1' if val else '0'}"
        )
        self._set_status(f"Color Blind Mode  {'▶  ON' if val else '■  OFF'}")

    # 25 ── PANIC / Kill Switch ────────────────────────────────────────────
    def toggle_panic(self, val):
        if val:
            self._set_status("⚠  PANIC  —  reverting all modules…", error=True)
            Clock.schedule_once(self._panic_execute, 0.5)

    def _panic_execute(self, dt):
        cmds = [
            "settings put system accelerometer_rotation 1",
            "settings put global low_power 0",
            "settings put global zen_mode 0",
            "settings put system screen_brightness_mode 1",
            "settings put system show_touches 0",
            "settings put system pointer_location 0",
            "settings put secure accessibility_display_magnification_enabled 0",
            "settings put secure accessibility_display_daltonizer_enabled 0",
            "wm density 0",
            "for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; "
            "do echo schedutil > $f 2>/dev/null; done",
            "sed -i '/0\\.0\\.0\\.0/d' /etc/hosts",
            "service call SurfaceFlinger 1023 i32 1 "
            "f 1 f 0 f 0 f 0 f 1 f 0 f 0 f 0 f 1 2>/dev/null",
            "start thermal-engine 2>/dev/null; start thermald 2>/dev/null",
            "settings put global wifi_scan_throttle_enabled 1",
        ]
        for c in cmds:
            self._su(c)

        for attr in ("_auto_click_event", "_ram_clean_event",
                     "_recoil_event", "_macro_event", "_ss_event"):
            ev = getattr(self, attr, None)
            if ev:
                ev.cancel()
                setattr(self, attr, None)

        if self._recorder_proc:
            self._recorder_proc.terminate()
            self._recorder_proc = None

        Animation(opacity=0, duration=0.3).start(self.root.ids.aim_grid)
        Animation(opacity=0, duration=0.3).start(self.root.ids.crosshair)
        self._set_status("✓  All modules reset to default")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    MachineApp().run()
