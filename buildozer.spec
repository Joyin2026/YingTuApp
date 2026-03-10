[app]
# 应用基本元数据
title = 影图空间
package.name = yingtu
package.domain = com.yingtux

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 0.1
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# 依赖库 - 使用兼容 Python 3 的版本
requirements = python3,kivy==2.3.0,pyjnius==1.6.0,android

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# 全屏、方向等
orientation = portrait
fullscreen = 1

# 图标和启动画面
android.gradle_dependencies = 'org.kivy:android:1.0'
android.add_src = .

# 如果有自定义的 AndroidManifest.xml 可以添加
# android.manifest = AndroidManifest.xml

# 指定最低 SDK 版本
android.minapi = 21
android.api = 33
android.ndk = 25b
android.sdk = 33

# 应用图标
android.icon.filename = %(source.dir)s/logo.png

[buildozer]
log_level = 2
warn_on_root = 1
