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
    # 切换到 webapp 目录
    if not os.path.exists('webapp'):
        print('错误：未找到 webapp 目录，请先运行 cordova create')
        sys.exit(1)
    os.chdir('webapp')

    # 创建资源目录
    os.makedirs('res/icon/android', exist_ok=True)
    os.makedirs('res/screen/android', exist_ok=True)

    # 生成图标
    icon_src = '../logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少 logo.png')
        sys.exit(1)
    icon_sizes = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    for density, size in icon_sizes.items():
        dst = f'res/icon/android/icon-{density}.png'
        resize_icon(icon_src, dst, size)
        print(f'生成图标: {dst}')

    # 生成启动画面
    splash_src = '../splash.png'
    if not os.path.exists(splash_src):
        print('错误：缺少 splash.png')
        sys.exit(1)
    splash_sizes = {
        'mdpi': (320, 480), 'hdpi': (480, 800), 'xhdpi': (720, 1280),
        'xxhdpi': (960, 1600), 'xxxhdpi': (1280, 1920)
    }
    for density, (w, h) in splash_sizes.items():
        dst = f'res/screen/android/splash-{density}.png'
        create_splash(splash_src, dst, w, h)
        print(f'生成启动画面: {dst}')

    # 修改 config.xml
    config_path = 'config.xml'
    shutil.copy(config_path, config_path + '.bak')
    with open(config_path, 'r') as f:
        content = f.read()

    # 确保有 android platform 标签
    platform_tag = '<platform name="android">'
    if platform_tag not in content:
        # 在 </widget> 前插入
        closing_widget = '</widget>'
        if closing_widget not in content:
            print('错误：未找到 </widget>')
            sys.exit(1)
        platform_block = '\n    <platform name="android">\n    </platform>\n'
        content = content.replace(closing_widget, platform_block + closing_widget)
        with open(config_path, 'w') as f:
            f.write(content)
        with open(config_path, 'r') as f:
            content = f.read()

    # 插入图标和启动画面配置（避免重复插入，先检查是否已有）
    if '<icon density=' not in content:
        icon_lines = [f'        <icon density="{d}" src="res/icon/android/icon-{d}.png" />' for d in icon_sizes]
        splash_lines = [f'        <splash density="{d}" src="res/screen/android/splash-{d}.png" />' for d in splash_sizes]
        insert_text = '\n' + '\n'.join(icon_lines + splash_lines)
        new_content = content.replace(platform_tag, platform_tag + insert_text)
        with open(config_path, 'w') as f:
            f.write(new_content)
        print('config.xml 已更新（插入图标/启动画面）')
    else:
        print('config.xml 已有图标/启动画面配置，跳过插入')

    # 添加启动画面首选项（延迟显示）
    preferences = [
        '<preference name="SplashScreen" value="screen" />',
        '<preference name="SplashScreenDelay" value="5000" />',
        '<preference name="AutoHideSplashScreen" value="false" />',
        '<preference name="FadeSplashScreen" value="false" />',
        '<preference name="ShowSplashScreenSpinner" value="false" />'
    ]
    # 在 <widget> 内插入
    widget_end = content.find('>', content.find('<widget')) + 1
    pref_text = '\n    ' + '\n    '.join(preferences) + '\n'
    new_content = content[:widget_end] + pref_text + content[widget_end:]

    # 添加 allow-navigation
    allow_nav = '\n    <allow-navigation href="https://www.yingtux.cn/*" />\n'
    platform_index = new_content.find('<platform')
    new_content = new_content[:platform_index] + allow_nav + new_content[platform_index:]

    with open(config_path, 'w') as f:
        f.write(new_content)
    print('已添加启动画面首选项和 allow-navigation')

    # 创建广告页面（包含清晰提示）
    os.makedirs('www/img', exist_ok=True)
    with open('www/ad.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>开屏广告</title>
    <meta http-equiv="refresh" content="5;url=https://www.yingtux.cn">
    <style>
        body { margin:0; padding:20px; background:#f0f0f0; text-align:center; font-family:sans-serif; }
        .container { min-height:80vh; display:flex; flex-direction:column; justify-content:center; }
        .ad-image { max-width:90%; max-height:50vh; margin:20px auto; border:2px solid #ccc; }
        .countdown { font-size:24px; margin:20px; }
        .skip-btn { padding:15px 40px; background:#007aff; color:white; border:none; border-radius:8px; font-size:18px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 开屏广告</h1>
        <img id="adImage" class="ad-image" style="display:none;" />
        <div id="adText" style="font-size:28px; font-weight:bold;">🎉 精彩广告位 🎉</div>
        <p>5秒后自动进入网站</p>
        <div class="countdown" id="countdown">5 秒后跳转</div>
        <button class="skip-btn" onclick="skipAd()">立即跳过</button>
    </div>
    <script>
        var img = new Image();
        img.onload = function() {
            document.getElementById('adImage').src = 'img/ad.png';
            document.getElementById('adImage').style.display = 'block';
            document.getElementById('adText').style.display = 'none';
        };
        img.onerror = function() { };
        img.src = 'img/ad.png';

        var seconds = 5;
        var countdownEl = document.getElementById('countdown');
        var timer = setInterval(function() {
            seconds--;
            if (seconds <= 0) {
                clearInterval(timer);
            } else {
                countdownEl.innerText = seconds + ' 秒后跳转';
            }
        }, 1000);

        function skipAd() {
            clearInterval(timer);
            window.location.href = 'https://www.yingtux.cn';
        }
    </script>
</body>
</html>''')
    print('广告页面已生成')

    # 复制广告图片
    if os.path.exists('../../ad.png'):
        shutil.copy('../../ad.png', 'www/img/ad.png')
        print('广告图片已复制')

if __name__ == '__main__':
    main()
