[app]
# 应用基本元数据
title = 影图空间
package.name = yingtu
package.domain = com.yingtux

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 0.1
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# 依赖库
requirements = python3,kivy,pyjnius,android

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# 全屏、方向等
orientation = portrait
fullscreen = 1

# 图标和启动画面（Kivy 默认不处理启动画面，但我们可以通过 splash 图片实现）
# 这里只是把图片打包进 APK，实际启动画面由我们的 Python 代码控制
android.gradle_dependencies = 'org.kivy:android:1.0'
android.add_src = .

# 如果有自定义的 AndroidManifest.xml 可以添加
# android.manifest = AndroidManifest.xml

# 指定最低 SDK 版本
android.minapi = 21
android.api = 33
android.ndk = 25b
android.sdk = 33

# 应用图标 (48x48, 72x72, 96x96, 144x144, 192x192)
android.icon.filename = %(source.dir)s/logo.png
# 注意：Buildozer 会根据这个图标自动生成多密度图标，但需要原始图片至少 192x192

# 启动画面（Kivy 的加载画面，但我们用自己的 splash.png，所以可以省略或保留）
# android.presplash.filename = splash.png   # 如果使用 Kivy 内置的启动画面，这里可以指定

[buildozer]
log_level = 2
warn_on_root = 1
