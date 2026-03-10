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
    print(f"当前工作目录: {os.getcwd()}")

    if not os.path.exists('webapp'):
        print('错误：未找到 webapp 目录，请先运行 cordova create')
        sys.exit(1)
    os.chdir('webapp')
    print(f"切换到 webapp 目录: {os.getcwd()}")

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

    # 修改 config.xml
    config_path = 'config.xml'
    shutil.copy(config_path, config_path + '.bak')
    with open(config_path, 'r') as f:
        content = f.read()

    # 确保起始页为 ad.html
    content = content.replace('<content src="index.html" />', '<content src="ad.html" />')
    if '<content src="ad.html"' not in content:
        # 如果没有找到 index.html 的 content，直接插入一个
        print("未找到 content 标签，手动插入...")
        widget_end = content.find('>', content.find('<widget')) + 1
        content = content[:widget_end] + '\n    <content src="ad.html" />' + content[widget_end:]

    platform_tag = '<platform name="android">'
    if platform_tag not in content:
        closing_widget = '</widget>'
        if closing_widget not in content:
            print('错误：未找到 </widget>')
            sys.exit(1)
        platform_block = '\n    <platform name="android">\n    </platform>\n'
        content = content.replace(closing_widget, platform_block + closing_widget)
        print('已创建 <platform name="android">')

    # 插入图标配置（避免重复）
    if '<icon density=' not in content:
        icon_lines = [f'        <icon density="{d}" src="res/icon/android/icon-{d}.png" />' for d in icon_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(icon_lines))
        print('已插入图标配置')
    else:
        print('图标配置已存在，跳过')

    # 插入启动画面配置（避免重复）
    if '<splash density=' not in content:
        splash_lines = [f'        <splash density="{d}" src="res/screen/android/splash-{d}.png" />' for d in splash_sizes]
        content = content.replace(platform_tag, platform_tag + '\n' + '\n'.join(splash_lines))
        print('已插入启动画面配置')
    else:
        print('启动画面配置已存在，跳过')

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
    print('config.xml 更新完成。')

    # 创建广告页面（增强版）
    os.makedirs('www/img', exist_ok=True)
    ad_html_path = 'www/ad.html'
    with open(ad_html_path, 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>开屏广告</title>
    <script src="cordova.js"></script>
    <style>
        body { margin:0; padding:20px; background:#f0f0f0; color:#333; font-family:sans-serif; text-align:center; }
        .container { min-height:80vh; display:flex; flex-direction:column; justify-content:center; }
        .ad-image { max-width:90%; max-height:50vh; margin:20px auto; border:2px solid #007aff; }
        .countdown { font-size:24px; margin:20px; }
        .skip-btn { padding:15px 40px; background:#007aff; color:white; border:none; border-radius:8px; font-size:18px; cursor:pointer; }
        .debug { color:red; font-size:14px; margin-top:20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="color:#007aff;">🔥 开屏广告已加载 🔥</h1>
        <img id="adImage" class="ad-image" src="img/ad.png" onerror="this.style.display='none'; document.getElementById('adText').style.display='block';" style="display:block;" />
        <div id="adText" style="font-size:28px; font-weight:bold; display:none;">🎉 精彩广告位 🎉</div>
        <p>5秒后自动进入网站</p>
        <div class="countdown" id="countdown">5 秒后跳转</div>
        <button class="skip-btn" onclick="skipAd()">立即跳过</button>
        <button class="skip-btn" onclick="hideSplash()" style="background:#34c759;">隐藏启动画面</button>
        <div class="debug" id="debugMsg"></div>
    </div>
    <script>
        function log(msg) {
            var d = document.getElementById('debugMsg');
            d.innerText += msg + '\\n';
        }

        // 尝试立即隐藏启动画面（如果可用）
        if (navigator.splashscreen) {
            navigator.splashscreen.hide();
            log('立即隐藏启动画面');
        }

        document.addEventListener('deviceready', function() {
            log('deviceready 事件触发');
            if (navigator.splashscreen) {
                navigator.splashscreen.hide();
                log('deviceready 中隐藏启动画面');
            }
        }, false);

        // 广告图片处理
        var img = new Image();
        img.onload = function() {
            document.getElementById('adImage').src = 'img/ad.png';
            document.getElementById('adImage').style.display = 'block';
            document.getElementById('adText').style.display = 'none';
            log('广告图片加载成功');
        };
        img.onerror = function() {
            log('广告图片加载失败');
        };
        img.src = 'img/ad.png';

        var seconds = 5;
        var countdownEl = document.getElementById('countdown');
        var timer = setInterval(function() {
            seconds--;
            if (seconds <= 0) {
                clearInterval(timer);
                log('倒计时结束，跳转网站');
                window.location.href = 'https://www.yingtux.cn';
            } else {
                countdownEl.innerText = seconds + ' 秒后跳转';
            }
        }, 1000);

        function skipAd() {
            clearInterval(timer);
            log('用户点击跳过');
            window.location.href = 'https://www.yingtux.cn';
        }

        function hideSplash() {
            if (navigator.splashscreen) {
                navigator.splashscreen.hide();
                log('手动隐藏启动画面');
            } else {
                log('navigator.splashscreen 不可用');
            }
        }

        // 超时保护：5秒后强制隐藏启动画面（如果页面卡住）
        setTimeout(function() {
            if (navigator.splashscreen) {
                navigator.splashscreen.hide();
                log('超时强制隐藏启动画面');
            }
        }, 3000);
    </script>
</body>
</html>''')
    print(f'广告页面已生成: {os.path.abspath(ad_html_path)}')

    # 复制广告图片（使用绝对路径确保准确）
    repo_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
    ad_src = os.path.join(repo_root, 'img', 'ad.png')
    print(f"广告图片源路径: {ad_src}")
    if os.path.exists(ad_src):
        shutil.copy(ad_src, 'www/img/ad.png')
        print(f'广告图片已从 {ad_src} 复制到 www/img/ad.png')
    else:
        print(f'错误：找不到 {ad_src}')
        # 列出 img 目录下的文件
        img_dir = os.path.join(repo_root, 'img')
        if os.path.exists(img_dir):
            print(f"img 目录内容: {os.listdir(img_dir)}")
        else:
            print(f"img 目录不存在: {img_dir}")
        sys.exit(1)

    # 输出 config.xml 开头部分以供检查
    with open(config_path, 'r') as f:
        first_lines = ''.join(f.readlines()[:20])
    print("config.xml 开头部分:\n", first_lines)

if __name__ == '__main__':
    main()
