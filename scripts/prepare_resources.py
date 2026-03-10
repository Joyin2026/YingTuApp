#!/usr/bin/env python3
import os
import sys
import shutil
from PIL import Image

def resize_icon(src, dst, size):
    try:
        img = Image.open(src)
    except Exception as e:
        print(f"错误：无法打开图标文件 {src}，请确保它是有效的 PNG 格式。详情：{e}")
        sys.exit(1)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(dst)

def create_splash(src, dst, width, height, bg_color=(255,255,255)):
    try:
        img = Image.open(src)
    except Exception as e:
        print(f"错误：无法打开启动画面文件 {src}，请确保它是有效的 PNG 格式。详情：{e}")
        sys.exit(1)
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
    if not os.path.exists('webapp'):
        print('错误：未找到 webapp 目录，请先运行 cordova create')
        sys.exit(1)
    os.chdir('webapp')

    os.makedirs('res/icon/android', exist_ok=True)
    os.makedirs('res/screen/android', exist_ok=True)

    # 生成图标（使用根目录下的 logo.png）
    icon_src = '../logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少根目录下的 logo.png')
        sys.exit(1)
    print(f"处理图标: {icon_src}")
    icon_sizes = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
    for density, size in icon_sizes.items():
        dst = f'res/icon/android/icon-{density}.png'
        resize_icon(icon_src, dst, size)
        print(f'生成图标: {dst}')

    # 生成启动画面（使用 img 目录下的 splash.png）
    splash_src = '../img/splash.png'
    if not os.path.exists(splash_src):
        print('错误：缺少 img/splash.png')
        sys.exit(1)
    print(f"处理启动画面: {splash_src}")
    splash_sizes = {
        'mdpi': (320, 480), 'hdpi': (480, 800), 'xhdpi': (720, 1280),
        'xxhdpi': (960, 1600), 'xxxhdpi': (1280, 1920)
    }
    for density, (w, h) in splash_sizes.items():
        dst = f'res/screen/android/splash-{density}.png'
        create_splash(splash_src, dst, w, h)
        print(f'生成启动画面: {dst}')

    # 修改 config.xml（此处省略，与之前相同，但确保缩进正确）
    # ...（为节省篇幅，省略 config.xml 修改部分，保持与之前相同）
    # 请确保 config.xml 部分完整保留，下面给出简写示意，实际需完整复制之前的内容

    # 以下为 config.xml 修改的完整代码（与之前最后一次提供的完全相同）
    config_path = 'config.xml'
    shutil.copy(config_path, config_path + '.bak')
    with open(config_path, 'r') as f:
        content = f.read()

    platform_tag = '<platform name="android">'
    if platform_tag not in content:
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

    if '<icon density=' not in content:
        icon_lines = [f'        <icon density="{d}" src="res/icon/android/icon-{d}.png" />' for d in icon_sizes]
        new_content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(icon_lines))
        with open(config_path, 'w') as f:
            f.write(new_content)
        with open(config_path, 'r') as f:
            content = f.read()
        print('已插入图标配置')
    else:
        print('图标配置已存在，跳过')

    if '<splash density=' not in content:
        splash_lines = [f'        <splash density="{d}" src="res/screen/android/splash-{d}.png" />' for d in splash_sizes]
        new_content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(splash_lines))
        with open(config_path, 'w') as f:
            f.write(new_content)
        with open(config_path, 'r') as f:
            content = f.read()
        print('已插入启动画面配置')
    else:
        print('启动画面配置已存在，跳过')

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

    allow_nav = '\n    <allow-navigation href="https://www.yingtux.cn/*" />\n'
    platform_index = content.find('<platform')
    content = content[:platform_index] + allow_nav + content[platform_index:]

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
    print('已添加启动画面首选项、allow-navigation 和资源文件复制指令')

    # 创建广告页面
    os.makedirs('www/img', exist_ok=True)
    with open('www/ad.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>开屏广告</title>
    <script src="cordova.js"></script>
    <style>
        body { margin:0; padding:0; background:#000; color:#fff; font-family:sans-serif; text-align:center; }
        .container { display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; }
        .ad-image { max-width:90%; max-height:70vh; border:2px solid #fff; }
        .countdown { font-size:24px; margin:20px; }
        .skip-btn { padding:15px 40px; background:#007aff; color:white; border:none; border-radius:8px; font-size:18px; }
    </style>
</head>
<body>
    <div class="container">
        <img id="adImage" class="ad-image" src="img/ad.png" onerror="this.style.display='none'; document.getElementById('adText').style.display='block';" style="display:block;" />
        <div id="adText" style="font-size:28px; font-weight:bold; display:none;">🎉 精彩广告位 🎉</div>
        <p>5秒后自动进入网站</p>
        <div class="countdown" id="countdown">5 秒后跳转</div>
        <button class="skip-btn" onclick="skipAd()">立即跳过</button>
    </div>
    <script>
        document.addEventListener('deviceready', function() {
            if (navigator.splashscreen) {
                navigator.splashscreen.hide();
                console.log('启动画面已隐藏');
            }
        }, false);

        var seconds = 5;
        var countdownEl = document.getElementById('countdown');
        var timer = setInterval(function() {
            seconds--;
            if (seconds <= 0) {
                clearInterval(timer);
                window.location.href = 'https://www.yingtux.cn';
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

    # 复制广告图片（从 img 目录复制到 www/img/）
    ad_src = '../../img/ad.png'
    if os.path.exists(ad_src):
        shutil.copy(ad_src, 'www/img/ad.png')
        print(f'广告图片已从 {ad_src} 复制到 www/img/ad.png')
    else:
        print('错误：缺少 img/ad.png')
        sys.exit(1)

if __name__ == '__main__':
    main()
