[app]

title = Ronia Shop
package.name = roniashop
package.domain = org.roniashop

source.dir = .
source.include_exts = py,png,jpg,jpeg,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[app:android]

android.api = 35
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
