[app]

# (str) Title of your application
title = 影图空间

# (str) Package name
package.name = yingtu

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yingtux

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let everything)
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Application versioning (method 1: manually set)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pyjnius,android

# (str) Custom source folders for requirements
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/splash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# android.accept_sdk_license = False

# (str) Android entry point, default is 'org.kivy.android.PythonActivity'
# android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# android.add_src = libs/*.jar
# android.add_src =

# (list) Gradle dependencies to add
android.gradle_dependencies = 'org.kivy:android:1.0'

# (list) add java compile options
# android.java_compile_options = @(supportAnnotations)

# (bool) Indicate whether the application should be compiled with support for
# older Android versions (API level < 21). This currently breaks on new Gradle.
# android.ignore_old_apis = False

# (list) Java classes to add as activities to the manifest.
# android.extra_activities = org.example.ExampleActivity

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so symlink
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
# ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# ios.kivy_ios_branch = master

# (str) Path to iOS toolchain support folder
# ios.toolchain_dir = ../toolchain

# (list) Name of the machine models to emulate
# ios.models = iPhone6, iPad Air 2

#
# OSX / MacOSX specific
#

# (str) Path to a custom kivy-sdk-packager folder
# osx.sdk_dir = ../kivy-sdk-packager
# Alternately, specify the URL and branch of a git checkout:
# osx.kivy_sdk_url = https://github.com/kivy/kivy-sdk-packager
# osx.kivy_sdk_branch = master

# (str) Kivy version to use
# osx.kivy_version = stable

#
# Windows specific
#

# (bool) If True, build for Windows only with mingw (GCC cross compiler)
# windows.cross_mingw = False

# (str) Path to a MinGW environment
# windows.mingw_path =

#
# Requirements
#

# (str) Presplash of the application
presplash.filename = %(source.dir)s/splash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/logo.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
