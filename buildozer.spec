[app]
title = Machine
package.name = com.sys.service.ovl
package.domain = org.machine
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Добавил явное указание версий для стабильности на GitHub
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pillow

# Важные разрешения для оверлея и работы с файлами
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACTION_MANAGE_OVERLAY_PERMISSION

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.archs = arm64-v8a
android.entrypoint = main.py

# Отключаем сборку на устройстве, так как делаем через GitHub
android.on_device_build = False
p4a.branch = master

# Для оверлеев часто полезно:
android.window_orientation = portrait
