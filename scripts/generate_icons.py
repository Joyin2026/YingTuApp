#!/usr/bin/env python3
import os
from PIL import Image

def resize_icon(src, dst, size):
    img = Image.open(src)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(dst)

def main():
    icon_src = 'logo.png'
    if not os.path.exists(icon_src):
        print('错误：缺少 logo.png')
        return

    # Android 图标目录
    base = 'android/app/src/main/res'
    sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192
    }
    for folder, size in sizes.items():
        os.makedirs(f'{base}/{folder}', exist_ok=True)
        dst = f'{base}/{folder}/ic_launcher.png'
        resize_icon(icon_src, dst, size)
        print(f'生成: {dst}')

if __name__ == '__main__':
    main()
