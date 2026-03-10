#!/usr/bin/env python3
import os
import sys
import shutil
from PIL import Image

def resize_icon(src, dst, size):
    img = Image.open(src)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(dst)

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

def main():
    print("===== 开始资源准备 =====")
    cwd = os.getcwd()
    print(f"当前工作目录: {cwd}")

    if not os.path.exists('webapp'):
        print('错误：未找到 webapp 目录')
        sys.exit(1)
    os.chdir('webapp')
    print(f"进入 webapp 目录: {os.getcwd()}")

    os.makedirs('res/icon/android', exist_ok=True)
    os.makedirs('res/screen/android', exist_ok=True)

    # 图标
    icon_src = '../logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少 ../logo.png')
        sys.exit(1)
    print(f"处理图标: {icon_src}")
    icon_sizes = {'mdpi':48, 'hdpi':72, 'xhdpi':96, 'xxhdpi':144, 'xxxhdpi':192}
    for d, s in icon_sizes.items():
        dst = f'res/icon/android/icon-{d}.png'
        resize_icon(icon_src, dst, s)
        print(f'生成图标: {dst}')

    # 启动画面
    splash_src = '../img/splash.png'
    if not os.path.exists(splash_src):
        print('错误：缺少 ../img/splash.png')
        sys.exit(1)
    print(f"处理启动画面: {splash_src}")
    splash_sizes = {
        'mdpi': (320,480), 'hdpi': (480,800), 'xhdpi': (720,1280),
        'xxhdpi': (960,1600), 'xxxhdpi': (1280,1920)
    }
    for d, (w,h) in splash_sizes.items():
        dst = f'res/screen/android/splash-{d}.png'
        create_splash(splash_src, dst, w, h)
        print(f'生成启动画面: {dst}')

    # 修改 config.xml
    config_path = 'config.xml'
    shutil.copy(config_path, config_path + '.bak')
    with open(config_path, 'r') as f:
        content = f.read()

    # 强制设置起始页为 ad.html
    content = content.replace('<content src="index.html" />', '<content src="ad.html" />')
    if '<content src="ad.html"' not in content:
        # 如果没有 content 标签，插入一个
        widget_end = content.find('>', content.find('<widget')) + 1
        content = content[:widget_end] + '\n    <content src="ad.html" />' + content[widget_end:]

    platform_tag = '<platform name="android">'
    if platform_tag not in content:
        closing_widget = '</widget>'
        if closing_widget not in content:
            print('错误：找不到 </widget>')
            sys.exit(1)
        platform_block = '\n    <platform name="android">\n    </platform>\n'
        content = content.replace(closing_widget, platform_block + closing_widget)
        print('已创建 <platform name="android">')

    # 插入图标配置
    if '<icon density=' not in content:
        icon_lines = [f'        <icon density="{d}" src="res/icon/android/icon-{d}.png" />' for d in icon_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(icon_lines))
        print('插入图标配置')

    # 插入启动画面配置
    if '<splash density=' not in content:
        splash_lines = [f'        <splash density="{d}" src="res/screen/android/splash-{d}.png" />' for d in splash_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(splash_lines))
        print('插入启动画面配置')

    # 添加启动画面首选项
    preferences = [
        '<preference name="SplashScreen" value="screen" />',
        '<preference name="SplashScreenDelay" value="5000" />',
        '<preference name="AutoHideSplashScreen" value="false" />',
        '<preference name="FadeSplashScreen" value="false" />',
        '<preference name="ShowSplashScreenSpinner" value="false" />'
    ]
    widget_end = content.find('>', content.find('<widget')) + 1
    pref_text = '\n    ' + '\n    '.join(preferences) + '\n'
    content = content[:widget_end] + pref_text + content[widget_end:]

    # 添加 allow-navigation
    allow_nav = '\n    <allow-navigation href="https://www.yingtux.cn/*" />\n'
    platform_index = content.find('<platform')
    content = content[:platform_index] + allow_nav + content[platform_index:]

    # 资源文件复制指令
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
    print("config.xml 已更新")

    # 创建极简广告页面（不依赖图片）
    os.makedirs('www', exist_ok=True)
    ad_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Debug Ad</title>
    <style>
        body { background: red; color: white; font-size: 40px; text-align: center; padding: 50px; }
    </style>
</head>
<body>
    <h1>广告页加载成功！</h1>
    <p id="countdown">5</p>
    <script src="cordova.js"></script>
    <script>
        // 立即尝试隐藏启动画面
        if (navigator.splashscreen) {
            navigator.splashscreen.hide();
            console.log('立即隐藏');
        }
        document.addEventListener('deviceready', function() {
            console.log('deviceready');
            if (navigator.splashscreen) {
                navigator.splashscreen.hide();
                console.log('deviceready 隐藏');
            }
        }, false);
        // 倒计时跳转
        var sec = 5;
        var count = document.getElementById('countdown');
        var timer = setInterval(function() {
            sec--;
            count.innerText = sec;
            if (sec <= 0) {
                clearInterval(timer);
                window.location.href = 'https://www.yingtux.cn';
            }
        }, 1000);
        // 超时强制隐藏启动画面
        setTimeout(function() {
            if (navigator.splashscreen) navigator.splashscreen.hide();
        }, 2000);
    </script>
</body>
</html>"""
    with open('www/ad.html', 'w') as f:
        f.write(ad_html)
    print("极简广告页面已生成")

    # 复制广告图片（可选，但这里不要求）
    # 输出 config.xml 前20行
    with open(config_path, 'r') as f:
        head = ''.join(f.readlines()[:20])
    print("config.xml 头部:\n", head)

    print("===== 资源准备完成 =====")

if __name__ == '__main__':
    main()
