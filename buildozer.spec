[app]
title = 影图空间
package.name = yingtu
package.domain = com.yingtux

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 0.1

requirements = python3,kivy==2.3.0,pyjnius==1.7.0,android

android.permissions = INTERNET,ACCESS_NETWORK_STATE

orientation = portrait
fullscreen = 1

android.gradle_dependencies = 'org.kivy:android:1.0'
android.add_src = .

android.minapi = 21
android.api = 33
android.ndk = 25b
android.sdk = 33

android.icon.filename = %(source.dir)s/logo.png

android.bootstrap_build_pre = pip install cython==0.29.36

[buildozer]
log_level = 2
warn_on_root = 1
