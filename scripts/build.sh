#!/bin/bash
set -e  # 遇到错误立即退出

echo "===== 开始构建 APK ====="

# 进入工作目录
cd webapp || { echo "错误：webapp 目录不存在"; exit 1; }

# 1. 生成图标和启动画面
echo "生成图标和启动画面..."
sudo apt-get update && sudo apt-get install -y imagemagick
mkdir -p res/icon/android res/screen/android

# 图标
if [ -f "../logo.png" ]; then
    for size in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
        case $size in
            mdpi) res=48 ;;
            hdpi) res=72 ;;
            xhdpi) res=96 ;;
            xxhdpi) res=144 ;;
            xxxhdpi) res=192 ;;
        esac
        convert ../logo.png -resize ${res}x${res} res/icon/android/icon-$size.png
    done
else
    echo "错误：缺少 logo.png"
    exit 1
fi

# 启动画面
if [ -f "../splash.png" ]; then
    for size in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
        case $size in
            mdpi) width=320; height=480 ;;
            hdpi) width=480; height=800 ;;
            xhdpi) width=720; height=1280 ;;
            xxhdpi) width=960; height=1600 ;;
            xxxhdpi) width=1280; height=1920 ;;
        esac
        convert ../splash.png -resize ${width}x${height}^ -gravity center -background white -extent ${width}x${height} res/screen/android/splash-$size.png
    done
else
    echo "错误：缺少 splash.png"
    exit 1
fi

# 2. 修改 config.xml
echo "修改 config.xml..."
cp config.xml config.xml.bak

# 使用 echo 和 sed 的组合来插入配置，避免复杂的 sed 脚本问题
# 首先确保 platform android 块存在（通常已存在）
# 在 platform 标签后插入图标和启动画面配置
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

# 3. 创建广告页面
echo "创建广告页面..."
cd www || { echo "错误：www 目录不存在"; exit 1; }
cat > ad.html << 'EOF'
<!DOCTYPE html>
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
</html>
EOF

mkdir -p img
if [ -f "../../ad.png" ]; then
    cp ../../ad.png img/ad.png
fi

cd ../..

# 4. 构建 APK
echo "构建 APK..."
BUILD_TYPE=${1:-debug}  # 第一个参数指定构建类型，默认为 debug
echo "构建类型: $BUILD_TYPE"
cordova build android --$BUILD_TYPE --verbose

# 输出 APK 路径供后续步骤使用
if [ "$BUILD_TYPE" = "debug" ]; then
    APK_PATH="webapp/platforms/android/app/build/outputs/apk/debug/app-debug.apk"
else
    APK_PATH="webapp/platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk"
fi
echo "APK 生成于: $APK_PATH"
echo "apk_path=$APK_PATH" >> $GITHUB_OUTPUT
