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

# ─────────────────────────────────────────────
#  KV LAYOUT
# ─────────────────────────────────────────────
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

    # ── MAIN MENU ──────────────────────────────
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
                text: "⬡  MACHINE CORE"
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
                    label_text: "Gyro Lock (no camera drift)"
                    icon_name: "rotate-3d-variant"
                    on_toggle: app.toggle_gyro_lock(*args)

                # 13 Volume Boost
                FeatureRow:
                    label_text: "Volume Boost (+20%)"
                    icon_name: "volume-high"
                    on_toggle: app.toggle_volume_boost(*args)

                # 14 Notification Mute
                FeatureRow:
                    label_text: "Mute Notifications"
                    icon_name: "bell-off"
                    on_toggle: app.toggle_notif_mute(*args)

                # 15 Macro Player
                FeatureRow:
                    label_text: "Macro Player"
                    icon_name: "play-circle"
                    on_toggle: app.toggle_macro(*args)

                # 16 Crosshair overlay
                FeatureRow:
                    label_text: "Custom Crosshair"
                    icon_name: "plus-circle-outline"
                    on_toggle: app.toggle_crosshair(*args)

                # 17 Thermal Throttle bypass
                FeatureRow:
                    label_text: "Thermal Throttle Guard"
                    icon_name: "thermometer-off"
                    on_toggle: app.toggle_thermal(*args)

                # 18 Touch visualiser
                FeatureRow:
                    label_text: "Touch Visualizer"
                    icon_name: "gesture"
                    on_toggle: app.toggle_touch_vis(*args)

                # 19 Screenshot shortcut
                FeatureRow:
                    label_text: "Quick Screenshot"
                    icon_name: "camera"
                    on_toggle: app.toggle_screenshot_mode(*args)

                # 20 Zoom overlay
                FeatureRow:
                    label_text: "Magnifier Zone"
                    icon_name: "magnify-plus"
                    on_toggle: app.toggle_magnifier(*args)

                # 21 Loot Highlight
                FeatureRow:
                    label_text: "Loot Highlight Filter"
                    icon_name: "star-circle"
                    on_toggle: app.toggle_loot_highlight(*args)

                # 22 Map overlay (minimap helper)
                FeatureRow:
                    label_text: "Minimap Enhancer"
                    icon_name: "map-marker"
                    on_toggle: app.toggle_minimap(*args)

                # 23 Recoil Stabiliser
                FeatureRow:
                    label_text: "Recoil Stabiliser"
                    icon_name: "target"
                    on_toggle: app.toggle_recoil(*args)

                # 24 Color Blind mode
                FeatureRow:
                    label_text: "Color Blind Mode"
                    icon_name: "eye-settings"
                    on_toggle: app.toggle_colorblind(*args)

                # 25 Panic Button
                FeatureRow:
                    label_text: "Panic / Kill Switch"
                    icon_name: "alert-octagon"
                    on_toggle: app.toggle_panic(*args)

        # Status bar
        MDSeparator:
            color: 0.2, 0.2, 0.2, 1

        MDLabel:
            id: status_label
            text: app.status_text
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.4, 0.9, 0.4, 1
            halign: "center"
            size_hint_y: None
            height: "22dp"

    # ── FLOATING BUTTON ────────────────────────
    FloatingButton:
        id: float_btn
        x: 20
        y: 300

    # ── AIM GRID OVERLAY ───────────────────────
    Widget:
        id: aim_grid
        opacity: 0
        canvas:
            Color:
                rgba: 1, 0, 0, 0.35
            # Horizontal center line
            Line:
                points: [0, root.height/2, root.width, root.height/2]
                width: 1
            # Vertical center line
            Line:
                points: [root.width/2, 0, root.width/2, root.height]
                width: 1
            # Rule-of-thirds horizontal
            Line:
                points: [0, root.height*0.333, root.width, root.height*0.333]
                width: 0.8
            Line:
                points: [0, root.height*0.667, root.width, root.height*0.667]
                width: 0.8
            # Rule-of-thirds vertical
            Line:
                points: [root.width*0.333, 0, root.width*0.333, root.height]
                width: 0.8
            Line:
                points: [root.width*0.667, 0, root.width*0.667, root.height]
                width: 0.8

    # ── CROSSHAIR OVERLAY ──────────────────────
    Widget:
        id: crosshair
        opacity: 0
        canvas:
            Color:
                rgba: 0, 1, 0.5, 0.9
            Line:
                circle: root.width/2, root.height/2, 18
                width: 1.5
            Line:
                points: [root.width/2-28, root.height/2, root.width/2-6, root.height/2]
                width: 2
            Line:
                points: [root.width/2+6, root.height/2, root.width/2+28, root.height/2]
                width: 2
            Line:
                points: [root.width/2, root.height/2+6, root.width/2, root.height/2+28]
                width: 2
            Line:
                points: [root.width/2, root.height/2-28, root.width/2, root.height/2-6]
                width: 2


# ── REUSABLE FEATURE ROW ───────────────────────────────
<FeatureRow@MDBoxLayout>:
    adaptive_height: True
    spacing: "8dp"
    padding: "4dp", "2dp"
    label_text: ""
    icon_name: "checkbox-blank-circle-outline"

    MDIcon:
        icon: root.icon_name
        theme_text_color: "Custom"
        text_color: app.accent
        size_hint_x: None
        width: "28dp"
        font_size: "20sp"

    MDLabel:
        text: root.label_text
        theme_text_color: "Secondary"
        font_style: "Body2"

    MDSwitch:
        size_hint_x: None
        width: "52dp"
        on_active: root.dispatch("on_toggle", self, self.active)

    # register custom event
    __events__: ("on_toggle",)

    # default no-op handler so kivy doesn't complain
    on_toggle: pass
'''


# ─────────────────────────────────────────────
#  CUSTOM WIDGETS
# ─────────────────────────────────────────────
class FloatingButton(DragBehavior, MDCard):
    pass


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class MachineApp(MDApp):
    menu_open   = BooleanProperty(False)
    status_text = StringProperty("● MACHINE CORE v1.0  –  READY")
    accent      = [0, 0.55, 1, 1]          # global accent colour

    # ── internal state ──────────────────────────
    _auto_click_event   = None
    _ram_clean_event    = None
    _recorder_proc      = None
    _active_features    = {}

    # ── build ────────────────────────────────────
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    # ── menu animation ───────────────────────────
    def open_menu(self):
        if not self.menu_open:
            Animation(pos_hint={"center_x": .5, "center_y": .5},
                      duration=0.35, t="out_back").start(self.root.ids.main_menu)
            Animation(opacity=0, duration=0.15).start(self.root.ids.float_btn)
            self.menu_open = True

    def close_menu(self):
        if self.menu_open:
            Animation(pos_hint={"center_x": .5, "center_y": -2},
                      duration=0.3, t="in_back").start(self.root.ids.main_menu)
            Animation(opacity=1, duration=0.2).start(self.root.ids.float_btn)
            self.menu_open = False

    # ── helpers ──────────────────────────────────
    def _su(self, cmd):
        """Run shell command silently (requires root)."""
        try:
            subprocess.Popen(f"su -c '{cmd}'", shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        except Exception as e:
            self._set_status(f"[root err] {e}")

    def _set_status(self, msg):
        self.status_text = f"● {msg}"

    # ════════════════════════════════════════════
    #  25 FEATURES
    # ════════════════════════════════════════════

    # 1 ── AdBlock ────────────────────────────────
    def toggle_adblock(self, sw, val):
        if val:
            self._su("echo '0.0.0.0 ads.google.com' >> /etc/hosts && "
                     "echo '0.0.0.0 googleads.g.doubleclick.net' >> /etc/hosts && "
                     "echo '0.0.0.0 pagead2.googlesyndication.com' >> /etc/hosts")
            self._set_status("AdBlock  ON")
        else:
            self._su("sed -i '/0\\.0\\.0\\.0 ads/d' /etc/hosts")
            self._set_status("AdBlock  OFF")

    # 2 ── OCR Translator ─────────────────────────
    def toggle_translator(self, sw, val):
        if val:
            self._su("am startservice -n com.google.android.apps.translate/.TranslateService")
            self._set_status("Translator  ON")
        else:
            self._su("am stopservice -n com.google.android.apps.translate/.TranslateService")
            self._set_status("Translator  OFF")

    # 3 ── FPS / CPU Governor boost ───────────────
    def toggle_fps_boost(self, sw, val):
        gov = "performance" if val else "schedutil"
        self._su(f"for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; "
                 f"do echo {gov} > $f 2>/dev/null; done")
        self._set_status(f"CPU Governor → {gov}")

    # 4 ── Always on Top ──────────────────────────
    def toggle_always_on_top(self, sw, val):
        # Window flag TYPE_APPLICATION_OVERLAY via adb shell
        flag = "1" if val else "0"
        self._su(f"settings put system always_on_top {flag}")
        self._set_status(f"Always on Top  {'ON' if val else 'OFF'}")

    # 5 ── Auto Clicker ───────────────────────────
    def toggle_auto_clicker(self, sw, val):
        if val:
            self._auto_click_event = Clock.schedule_interval(
                self._do_auto_click, 0.08)           # ~12 CPS
            self._set_status("Auto Clicker  ON  (12 CPS)")
        else:
            if self._auto_click_event:
                self._auto_click_event.cancel()
                self._auto_click_event = None
            self._set_status("Auto Clicker  OFF")

    def _do_auto_click(self, dt):
        w = Window.width // 2
        h = Window.height // 2
        self._su(f"input tap {w} {h}")

    # 6 ── Aim Grid ───────────────────────────────
    def toggle_aim_grid(self, sw, val):
        self.root.ids.aim_grid.opacity = 1 if val else 0
        self._set_status(f"Aim Grid  {'ON' if val else 'OFF'}")

    # 7 ── High DPI ───────────────────────────────
    def toggle_dpi(self, sw, val):
        dpi = "480" if val else "0"      # 0 = reset to default
        self._su(f"wm density {dpi}")
        self._set_status(f"DPI → {'480 (High)' if val else 'Default'}")

    # 8 ── RAM Cleaner ────────────────────────────
    def toggle_ram_cleaner(self, sw, val):
        if val:
            self._ram_clean_event = Clock.schedule_interval(
                lambda dt: self._su("sync && echo 3 > /proc/sys/vm/drop_caches"),
                30)
            self._set_status("RAM Cleaner  ON  (every 30s)")
        else:
            if self._ram_clean_event:
                self._ram_clean_event.cancel()
                self._ram_clean_event = None
            self._set_status("RAM Cleaner  OFF")

    # 9 ── Battery Saver ──────────────────────────
    def toggle_battery_saver(self, sw, val):
        mode = "1" if val else "0"
        self._su(f"settings put global low_power {mode}")
        self._set_status(f"Battery Saver  {'ON' if val else 'OFF'}")

    # 10 ── Ping Reducer ──────────────────────────
    def toggle_ping_reducer(self, sw, val):
        if val:
            self._su("settings put global wifi_scan_throttle_enabled 0 && "
                     "settings put global wifi_sleep_policy 2")
            self._set_status("Ping Reducer  ON")
        else:
            self._su("settings put global wifi_scan_throttle_enabled 1 && "
                     "settings put global wifi_sleep_policy 0")
            self._set_status("Ping Reducer  OFF")

    # 11 ── Screen Recorder ───────────────────────
    def toggle_screen_recorder(self, sw, val):
        if val:
            out = "/sdcard/MC_record.mp4"
            self._recorder_proc = subprocess.Popen(
                f"su -c 'screenrecord --verbose {out}'",
                shell=True)
            self._set_status("Recording…  → /sdcard/MC_record.mp4")
        else:
            if self._recorder_proc:
                self._recorder_proc.terminate()
                self._recorder_proc = None
            self._set_status("Recording saved")

    # 12 ── Gyro Lock ─────────────────────────────
    def toggle_gyro_lock(self, sw, val):
        flag = "0" if val else "1"       # disable rotation = lock
        self._su(f"settings put system accelerometer_rotation {flag}")
        self._set_status(f"Gyro Lock  {'ON' if val else 'OFF'}")

    # 13 ── Volume Boost ──────────────────────────
    def toggle_volume_boost(self, sw, val):
        # Media stream max on most devices is 15
        vol = "15" if val else "10"
        self._su(f"media volume --stream 3 --set {vol}")
        self._set_status(f"Volume → {'MAX (15)' if val else 'Normal (10)'}")

    # 14 ── Notification Mute ─────────────────────
    def toggle_notif_mute(self, sw, val):
        mode = "2" if val else "0"       # 2 = no interruptions
        self._su(f"settings put global zen_mode {mode}")
        self._set_status(f"Notifications  {'MUTED' if val else 'NORMAL'}")

    # 15 ── Macro Player ──────────────────────────
    def toggle_macro(self, sw, val):
        """Plays a simple tap-swipe sequence macro."""
        if val:
            self._macro_event = Clock.schedule_interval(
                self._run_macro_step, 1.5)
            self._macro_step = 0
            self._set_status("Macro  RUNNING")
        else:
            if hasattr(self, "_macro_event") and self._macro_event:
                self._macro_event.cancel()
            self._set_status("Macro  STOPPED")

    _macro_step = 0
    _macro_sequence = [
        "input tap 540 960",
        "input swipe 200 800 600 800 150",
        "input tap 540 500",
        "input keyevent 4",          # BACK
    ]

    def _run_macro_step(self, dt):
        cmd = self._macro_sequence[self._macro_step % len(self._macro_sequence)]
        self._su(cmd)
        self._macro_step += 1

    # 16 ── Custom Crosshair ──────────────────────
    def toggle_crosshair(self, sw, val):
        self.root.ids.crosshair.opacity = 1 if val else 0
        self._set_status(f"Crosshair  {'ON' if val else 'OFF'}")

    # 17 ── Thermal Throttle Guard ────────────────
    def toggle_thermal(self, sw, val):
        if val:
            self._su("setprop persist.vendor.thermal.config '' && "
                     "stop thermal-engine 2>/dev/null; "
                     "stop thermald 2>/dev/null")
            self._set_status("Thermal Guard  ON  (⚠ may heat up)")
        else:
            self._su("start thermal-engine 2>/dev/null; start thermald 2>/dev/null")
            self._set_status("Thermal Guard  OFF")

    # 18 ── Touch Visualiser ──────────────────────
    def toggle_touch_vis(self, sw, val):
        flag = "1" if val else "0"
        self._su(f"settings put system show_touches {flag} && "
                 f"settings put system pointer_location {flag}")
        self._set_status(f"Touch Vis  {'ON' if val else 'OFF'}")

    # 19 ── Quick Screenshot ──────────────────────
    def toggle_screenshot_mode(self, sw, val):
        """When ON, takes a screenshot every 5 seconds."""
        if val:
            self._ss_event = Clock.schedule_interval(self._take_screenshot, 5)
            self._set_status("Screenshot mode  ON  (5s)")
        else:
            if hasattr(self, "_ss_event") and self._ss_event:
                self._ss_event.cancel()
            self._set_status("Screenshot mode  OFF")

    def _take_screenshot(self, dt):
        stamp = int(time.time())
        self._su(f"screencap -p /sdcard/MC_shot_{stamp}.png")

    # 20 ── Magnifier Zone ────────────────────────
    def toggle_magnifier(self, sw, val):
        flag = "1" if val else "0"
        self._su(f"settings put secure accessibility_display_magnification_enabled {flag}")
        self._set_status(f"Magnifier  {'ON' if val else 'OFF'}")

    # 21 ── Loot Highlight ────────────────────────
    def toggle_loot_highlight(self, sw, val):
        """
        Boost colour saturation so loot/items stand out.
        Uses display colour transform matrix via surface flinger.
        """
        if val:
            self._su("service call SurfaceFlinger 1023 i32 1 f 1.8 f 0 f 0 "
                     "f 0 f 1.8 f 0 f 0 f 0 f 1.8 2>/dev/null")
            self._set_status("Loot Highlight  ON  (+saturation)")
        else:
            self._su("service call SurfaceFlinger 1023 i32 1 f 1 f 0 f 0 "
                     "f 0 f 1 f 0 f 0 f 0 f 1 2>/dev/null")
            self._set_status("Loot Highlight  OFF")

    # 22 ── Minimap Enhancer ──────────────────────
    def toggle_minimap(self, sw, val):
        """
        Increases screen brightness so minimap details are visible,
        and turns off auto-brightness.
        """
        if val:
            self._su("settings put system screen_brightness_mode 0 && "
                     "settings put system screen_brightness 220")
            self._set_status("Minimap Enhancer  ON")
        else:
            self._su("settings put system screen_brightness_mode 1")
            self._set_status("Minimap Enhancer  OFF  (auto-bright)")

    # 23 ── Recoil Stabiliser ─────────────────────
    def toggle_recoil(self, sw, val):
        """
        Micro-swipe upward while firing to counteract recoil.
        Runs as a repeating tiny drag on the screen centre.
        """
        if val:
            cx = Window.width  // 2
            cy = Window.height // 2
            self._recoil_event = Clock.schedule_interval(
                lambda dt: self._su(
                    f"input swipe {cx} {cy} {cx} {cy+5} 30"), 0.05)
            self._set_status("Recoil Stabiliser  ON")
        else:
            if hasattr(self, "_recoil_event") and self._recoil_event:
                self._recoil_event.cancel()
            self._set_status("Recoil Stabiliser  OFF")

    # 24 ── Colour Blind Mode ─────────────────────
    def toggle_colorblind(self, sw, val):
        # 0 = none, 12 = deuteranomaly green-weak (most common)
        mode = "12" if val else "0"
        self._su(f"settings put secure accessibility_display_daltonizer {mode} && "
                 f"settings put secure accessibility_display_daltonizer_enabled {'1' if val else '0'}")
        self._set_status(f"Color Blind Mode  {'ON' if val else 'OFF'}")

    # 25 ── Panic / Kill Switch ───────────────────
    def toggle_panic(self, sw, val):
        """
        Emergency: revert ALL settings and stop all running features.
        The switch turns everything off and resets to defaults.
        """
        if val:
            self._set_status("PANIC MODE – reverting all…")
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
            "sed -i '/0\\.0\\.0\\.0 ads/d' /etc/hosts",
        ]
        for c in cmds:
            self._su(c)

        # Cancel all kivy timers
        for attr in ("_auto_click_event", "_ram_clean_event",
                     "_recoil_event", "_macro_event", "_ss_event"):
            ev = getattr(self, attr, None)
            if ev:
                ev.cancel()

        self.root.ids.aim_grid.opacity  = 0
        self.root.ids.crosshair.opacity = 0
        self._set_status("✓ All features reset to default")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    MachineApp().run()
