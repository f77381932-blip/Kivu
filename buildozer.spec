[app]
title = Machine Core
package.name = com.sys.machine.core
package.domain = org.machine
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf

android.permissions = INTERNET,SYSTEM_ALERT_WINDOW,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE,REQUEST_INSTALL_PACKAGES

android.api = 33
android.build_tools_version = 33.0.2
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.ndk_api = 26
android.archs = arm64-v8a

android.entrypoint = main.py
android.orientation = portrait

# Splash & icon (put your files next to buildozer.spec)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

android.release_artifact = apk
android.on_device_build = False

p4a.branch = master
p4a.bootstrap = sdl2

log_level = 2
warn_on_root = 1
