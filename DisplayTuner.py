import sys
import screen_brightness_control as sbc
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QComboBox
from PyQt6.QtCore import Qt

class MonitorSettingsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.monitors = sbc.list_monitors()  # 연결된 모니터 목록 가져오기
        if not self.monitors:
            self.monitors = ['디스플레이 없음']
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('모니터 설정')
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.monitor_label = QLabel('모니터 선택')
        self.monitor_select = QComboBox()
        self.monitor_select.addItems(self.monitors)
        self.monitor_select.currentIndexChanged.connect(self.update_monitor)

        self.brightness_label = QLabel('밝기: 50')
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        try:
            initial_brightness = sbc.get_brightness(display=self.monitors[0])[0]
        except Exception:
            initial_brightness = 50  # 기본값
        self.brightness_slider.setValue(initial_brightness)
        self.brightness_slider.valueChanged.connect(self.update_brightness)

        # self.contrast_label = QLabel('명암 (소프트웨어 기반 조절)')
        # self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        # self.contrast_slider.setRange(0, 100)
        # self.contrast_slider.setValue(50)
        # self.contrast_slider.valueChanged.connect(self.update_contrast)

        self.apply_button = QPushButton('설정 적용')
        self.apply_button.clicked.connect(self.apply_settings)

        layout.addWidget(self.monitor_label)
        layout.addWidget(self.monitor_select)
        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)
        # layout.addWidget(self.contrast_label)
        # layout.addWidget(self.contrast_slider)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)
        self.selected_monitor = self.monitors[0]

    def update_monitor(self, index):
        self.selected_monitor = self.monitors[index]
        try:
            brightness = sbc.get_brightness(display=self.selected_monitor)[0]
        except Exception:
            brightness = 50  # 기본값 유지
        self.brightness_slider.setValue(brightness)

    def update_brightness(self, value):
        self.brightness_label.setText(f'밝기: {value}')

    def update_contrast(self, value):
        self.contrast_label.setText(f'명암 (소프트웨어 조절): {value}')

    def apply_settings(self):
        if self.selected_monitor == '디스플레이 없음':
            print('설정 적용 실패: 연결된 모니터 없음')
            return
        brightness = self.brightness_slider.value()
        try:
            sbc.set_brightness(brightness, display=self.selected_monitor)
            print(f'설정 적용: 모니터 {self.selected_monitor}, 밝기 {brightness}')
        except Exception as e:
            print(f'설정 적용 실패: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonitorSettingsApp()
    window.show()
    sys.exit(app.exec())
