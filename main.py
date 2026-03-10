"""
Kivy 应用：启动画面 -> 开屏广告 (5秒) -> 加载网站
适配 1440x3200 分辨率，全屏显示
"""
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.utils import platform

# 如果是 Android 平台，导入 WebView
if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
    # WebView 相关 Java 类
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LinearLayout = autoclass('android.widget.LinearLayout')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    ColorJava = autoclass('android.graphics.Color')

# 设置窗口大小为全屏（在 Android 上会自动全屏，但可以强制隐藏标题栏）
Window.fullscreen = 'auto'
Window.size = (1440, 3200)  # 设计尺寸，实际会根据屏幕密度自动缩放

class AdScreen(BoxLayout):
    """开屏广告页面，5秒后自动跳转"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0

        # 背景颜色
        with self.canvas.before:
            Color(1, 1, 1, 1)  # 白色背景
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 广告图片（如果有 ad.png 则显示，否则显示文字）
        if self._file_exists('ad.png'):
            self.ad_image = Image(source='ad.png', allow_stretch=True, keep_ratio=True)
            self.add_widget(self.ad_image)
        else:
            self.add_widget(Label(
                text='🎉 精彩广告位 🎉',
                font_size='48sp',
                color=(0,0,0,1),
                size_hint=(1, 0.6)
            ))

        # 底部倒计时和跳过按钮
        bottom_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.countdown_label = Label(
            text='5 秒后自动进入网站',
            font_size='24sp',
            color=(0.5,0.5,0.5,1)
        )
        bottom_layout.add_widget(self.countdown_label)

        self.skip_btn = Button(
            text='立即跳过',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.5, 1, 1),
            color=(1,1,1,1)
        )
        self.skip_btn.bind(on_press=self.skip_ad)
        bottom_layout.add_widget(self.skip_btn)

        self.add_widget(bottom_layout)

        # 启动倒计时
        self.seconds = 5
        self.timer = Clock.schedule_interval(self.update_countdown, 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _file_exists(self, filename):
        from os.path import exists
        return exists(filename)

    def update_countdown(self, dt):
        self.seconds -= 1
        if self.seconds <= 0:
            self.timer.cancel()
            self.go_to_website()
        else:
            self.countdown_label.text = f'{self.seconds} 秒后自动进入网站'

    def skip_ad(self, instance):
        self.timer.cancel()
        self.go_to_website()

    def go_to_website(self):
        """跳转到主网站页面"""
        app = App.get_running_app()
        app.show_website()

class WebsiteScreen(BoxLayout):
    """WebView 显示网站"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        if platform == 'android':
            self._create_android_webview()
        else:
            # 桌面调试时显示提示
            self.add_widget(Label(
                text='WebView 仅在 Android 上可用。\n你的网站：https://www.yingtux.cn',
                halign='center'
            ))

    def _create_android_webview(self):
        """创建 Android WebView 并添加到布局"""
        @run_on_ui_thread
        def add_webview():
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity

            webview = WebView(activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.setWebViewClient(WebViewClient())
            webview.loadUrl('https://www.yingtux.cn')

            # 将 WebView 添加到 Activity 的根布局
            layout = LinearLayout(activity)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.addView(webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            activity.setContentView(layout)

        add_webview()
        # 由于 WebView 替换了 Activity 的 content view，此布局实际上不再需要，但保持结构
        self.add_widget(Label(text='加载中...'))

class YingTuApp(App):
    def build(self):
        # 先显示启动画面（这里简单展示 splash.png）
        if self._file_exists('splash.png'):
            splash = Image(source='splash.png', allow_stretch=True, keep_ratio=False)
            # 用 Clock 短暂延迟后切换到广告页
            Clock.schedule_once(lambda dt: self.show_ad(), 2)  # 显示2秒启动画面
            return splash
        else:
            # 如果没有 splash.png，直接进入广告页
            self.show_ad()
            return AdScreen()

    def _file_exists(self, filename):
        from os.path import exists
        return exists(filename)

    def show_ad(self):
        self.root.clear_widgets()
        self.root.add_widget(AdScreen())

    def show_website(self):
        self.root.clear_widgets()
        self.root.add_widget(WebsiteScreen())

if __name__ == '__main__':
    YingTuApp().run()
