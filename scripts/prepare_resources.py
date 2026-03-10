#!/usr/bin/env python3
import os
import sys
import shutil
from PIL import Image

def resize_icon(src, dst, size):
    img = Image.open(src)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(dst)
    print(f'生成图标: {dst}')

def create_splash(src, dst, width, height, bg_color=(255,255,255)):
    img = Image.open(src)
    canvas = Image.new('RGB', (width, height), bg_color)
    img_ratio = img.width / img.height
    canvas_ratio = width / height
    if img_ratio > canvas_ratio:
        new_height = height
        new_width = int(new_height * img_ratio)
    else:
        new_width = width
        new_height = int(new_width / img_ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    img = img.crop((left, top, left+width, top+height))
    canvas.paste(img, (0,0))
    canvas.save(dst)
    print(f'生成启动画面: {dst}')

def main():
    os.chdir('webapp')
    os.makedirs('res/icon/android', exist_ok=True)
    os.makedirs('res/screen/android', exist_ok=True)

    # 图标
    icon_src = '../logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少根目录 logo.png')
        sys.exit(1)
    icon_sizes = {'mdpi':48, 'hdpi':72, 'xhdpi':96, 'xxhdpi':144, 'xxxhdpi':192}
    for density, size in icon_sizes.items():
        resize_icon(icon_src, f'res/icon/android/icon-{density}.png', size)

    # 启动画面
    splash_src = '../img/splash.png'
    if not os.path.exists(splash_src):
        print('错误：缺少 img/splash.png')
        sys.exit(1)
    splash_sizes = {
        'mdpi': (320,480), 'hdpi': (480,800), 'xhdpi': (720,1280),
        'xxhdpi': (960,1600), 'xxxhdpi': (1280,1920)
    }
    for density, (w, h) in splash_sizes.items():
        create_splash(splash_src, f'res/screen/android/splash-{density}.png', w, h)

    # 修改 config.xml（仅添加图标和启动画面配置，不修改 content）
    config_path = 'config.xml'
    shutil.copy(config_path, config_path + '.bak')
    with open(config_path, 'r') as f:
        content = f.read()

    # 确保有 android platform 标签
    platform_tag = '<platform name="android">'
    if platform_tag not in content:
        closing_widget = '</widget>'
        if closing_widget not in content:
            print('错误：未找到 </widget>')
            sys.exit(1)
        platform_block = '\n    <platform name="android">\n    </platform>\n'
        content = content.replace(closing_widget, platform_block + closing_widget)

    # 插入图标配置
    if '<icon density=' not in content:
        icon_lines = [f'        <icon density="{d}" src="res/icon/android/icon-{d}.png" />' for d in icon_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(icon_lines))

    # 插入启动画面配置
    if '<splash density=' not in content:
        splash_lines = [f'        <splash density="{d}" src="res/screen/android/splash-{d}.png" />' for d in splash_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(splash_lines))

    # 添加启动画面首选项
    preferences = [
        '<preference name="SplashScreen" value="screen" />',
        '<preference name="SplashScreenDelay" value="3000" />',
        '<preference name="AutoHideSplashScreen" value="true" />',
        '<preference name="FadeSplashScreen" value="false" />',
        '<preference name="ShowSplashScreenSpinner" value="false" />'
    ]
    widget_end = content.find('>', content.find('<widget')) + 1
    pref_text = '\n    ' + '\n    '.join(preferences) + '\n'
    content = content[:widget_end] + pref_text + content[widget_end:]

    # 添加 allow-navigation（workflow 已加，这里可保留）
    allow_nav = '\n    <allow-navigation href="https://www.yingtux.cn/*" />\n'
    platform_index = content.find('<platform')
    content = content[:platform_index] + allow_nav + content[platform_index:]

    # 添加资源文件复制指令
    resource_files = [
        '<resource-file src="res/screen/android/splash-mdpi.png" target="res/drawable-port-mdpi/splash.png" />',
        '<resource-file src="res/screen/android/splash-hdpi.png" target="res/drawable-port-hdpi/splash.png" />',
        '<resource-file src="res/screen/android/splash-xhdpi.png" target="res/drawable-port-xhdpi/splash.png" />',
        '<resource-file src="res/screen/android/splash-xxhdpi.png" target="res/drawable-port-xxhdpi/splash.png" />',
        '<resource-file src="res/screen/android/splash-xxxhdpi.png" target="res/drawable-port-xxxhdpi/splash.png" />'
    ]
    resource_text = '\n'.join(resource_files) + '\n'
    platform_end = content.find('</platform>', content.find(platform_tag))
    content = content[:platform_end] + resource_text + content[platform_end:]

    with open(config_path, 'w') as f:
        f.write(content)
    print('config.xml 更新完成')

if __name__ == '__main__':
    main()
