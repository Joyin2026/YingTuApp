#!/usr/bin/env python3
import os
import sys
import shutil
from PIL import Image
import xml.etree.ElementTree as ET

def resize_icon(src, dst, size):
    img = Image.open(src)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(dst)

def create_splash(src, dst, width, height, bg_color=(255,255,255)):
    img = Image.open(src)
    # 创建白色背景画布
    canvas = Image.new('RGB', (width, height), bg_color)
    # 计算缩放比例，使图片填满画布并居中裁剪
    img_ratio = img.width / img.height
    canvas_ratio = width / height
    if img_ratio > canvas_ratio:
        new_height = height
        new_width = int(new_height * img_ratio)
    else:
        new_width = width
        new_height = int(new_width / img_ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    # 居中粘贴
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    img = img.crop((left, top, left+width, top+height))
    canvas.paste(img, (0,0))
    canvas.save(dst)

def main():
    # 切换到webapp目录
    os.chdir('webapp')
    
    # 创建资源目录
    os.makedirs('res/icon/android', exist_ok=True)
    os.makedirs('res/screen/android', exist_ok=True)
    
    # 处理图标
    icon_src = '../logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少logo.png')
        sys.exit(1)
    icon_sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    for density, size in icon_sizes.items():
        dst = f'res/icon/android/icon-{density}.png'
        resize_icon(icon_src, dst, size)
        print(f'生成图标: {dst}')
    
    # 处理启动画面
    splash_src = '../splash.png'
    if not os.path.exists(splash_src):
        print('错误：缺少splash.png')
        sys.exit(1)
    splash_sizes = {
        'mdpi': (320, 480),
        'hdpi': (480, 800),
        'xhdpi': (720, 1280),
        'xxhdpi': (960, 1600),
        'xxxhdpi': (1280, 1920)
    }
    for density, (w, h) in splash_sizes.items():
        dst = f'res/screen/android/splash-{density}.png'
        create_splash(splash_src, dst, w, h)
        print(f'生成启动画面: {dst}')
    
    # 修改config.xml
    config_path = 'config.xml'
    # 备份
    shutil.copy(config_path, config_path + '.bak')
    
    # 解析XML（注意：Cordova的config.xml可能有命名空间，我们简单用字符串处理）
    with open(config_path, 'r') as f:
        content = f.read()
    
    # 在<platform name="android">后插入图标和启动画面配置
    platform_tag = '<platform name="android">'
    if platform_tag in content:
        # 构建要插入的配置块
        insert_lines = []
        for density in icon_sizes.keys():
            insert_lines.append(f'        <icon density="{density}" src="res/icon/android/icon-{density}.png" />')
        for density in splash_sizes.keys():
            insert_lines.append(f'        <splash density="{density}" src="res/screen/android/splash-{density}.png" />')
        insert_text = '\n' + '\n'.join(insert_lines)
        # 在platform标签后插入
        new_content = content.replace(platform_tag, platform_tag + insert_text)
        with open(config_path, 'w') as f:
            f.write(new_content)
        print('config.xml已更新')
    else:
        print('错误：未找到<platform name="android">')
        sys.exit(1)
    
    # 创建广告页面
    os.makedirs('www/img', exist_ok=True)
    ad_html_path = 'www/ad.html'
    with open(ad_html_path, 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>开屏广告</title>
    <style>
        body { margin: 0; padding: 0; background-color: #ffffff; font-family: sans-serif; }
        .container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; text-align: center; }
        .ad-image { max-width: 90%; max-height: 70vh; margin-bottom: 20px; }
        .countdown { font-size: 18px; color: #666; margin-top: 20px; }
        .skip-btn { margin-top: 30px; padding: 10px 30px; background-color: #007aff; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
    </style>
    <meta http-equiv="refresh" content="5;url=https://www.yingtux.cn">
</head>
<body>
    <div class="container">
        <img id="adImage" class="ad-image" style="display:none;" />
        <div id="adText" style="font-size:24px; font-weight:bold; color:#333;">🎉 精彩广告位 🎉</div>
        <p style="color:#888;">5秒后自动进入网站</p>
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
                // 使用meta refresh保证跳转，这里仅更新显示
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
    
    # 复制广告图片（如果有）
    if os.path.exists('../../ad.png'):
        shutil.copy('../../ad.png', 'www/img/ad.png')
        print('广告图片已复制')

if __name__ == '__main__':
    main()
