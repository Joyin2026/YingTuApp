#!/bin/bash
set -e
cd webapp
cp config.xml config.xml.bak

sed -i '/<platform name="android">/a \        <icon density="mdpi" src="res/icon/android/icon-mdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <icon density="hdpi" src="res/icon/android/icon-hdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <icon density="xhdpi" src="res/icon/android/icon-xhdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <icon density="xxhdpi" src="res/icon/android/icon-xxhdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <icon density="xxxhdpi" src="res/icon/android/icon-xxxhdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <splash density="mdpi" src="res/screen/android/splash-mdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <splash density="hdpi" src="res/screen/android/splash-hdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <splash density="xhdpi" src="res/screen/android/splash-xhdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <splash density="xxhdpi" src="res/screen/android/splash-xxhdpi.png" />' config.xml
sed -i '/<platform name="android">/a \        <splash density="xxxhdpi" src="res/screen/android/splash-xxxhdpi.png" />' config.xml

echo "config.xml 已更新"
